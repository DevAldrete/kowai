import dspy
from haystack import Pipeline  # Use AsyncPipeline in production!
from haystack.components.converters import HTMLToDocument
from haystack.components.fetchers import LinkContentFetcher
from haystack.components.joiners import DocumentJoiner
from haystack.components.websearch import SerperDevWebSearch
from haystack.utils import Secret

from app.core.config import get_settings

settings = get_settings()

serper = SerperDevWebSearch(api_key=Secret.from_token(settings.serper_api_key))
converter = HTMLToDocument()
fetcher = LinkContentFetcher()

joiner = DocumentJoiner()

search = Pipeline()

search.add_component("serper", serper)
search.add_component("converter", converter)
search.add_component("fetcher", fetcher)
search.add_component("joiner", joiner)

search.connect("serper.links", "fetcher.urls")
search.connect("fetcher.streams", "converter.sources")
search.connect("converter.documents", "joiner.documents")

search_tool = dspy.Tool(
    func=search.run,
    name="search_tool",
    desc="Search the web for information using Serper and return relevant documents",
)

