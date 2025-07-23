from pprint import pprint
from app.ai.agents import Metadata as AgentMetadata, ProviderType
from app.ai.nodes.agents.base import BaseAgent
from app.core.config import get_settings
import asyncio

settings = get_settings()

async def main():
    query = input("Enter your search query: ")
    metadata = AgentMetadata(
        model="gpt-4o-mini",
        tokens=1000,
        temperature=0.2,
        max_tokens=1000,
        provider=ProviderType.OPENAI,
        api_key=settings.openai_api_key,
    )
    agent = BaseAgent(metadata=metadata)
    result = await agent(query=query)
    pprint(result)


if __name__ == "__main__":
    asyncio.run(main())
