import dspy
from haystack import Pipeline  # AsyncPipeline in production
from haystack.components.preprocessors import HierarchicalDocumentSplitter
from haystack.components.retrievers import AutoMergingRetriever
from haystack.document_stores.in_memory import InMemoryDocumentStore

# Lack of a memory store
document_store = InMemoryDocumentStore()
splitter = HierarchicalDocumentSplitter(block_sizes={1000, 500, 100})
retriever = AutoMergingRetriever(document_store=document_store)


rag = Pipeline()
rag.add_component("splitter", splitter)
rag.add_component("retriever", retriever)

rag_tool = dspy.Tool(
    func=rag.run,
    name="rag_tool",
    desc="Retrieve and process documents using RAG pipeline",
)
