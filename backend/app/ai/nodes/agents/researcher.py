import dspy

from app.ai.agents import Management as AgentManagement
from app.ai.agents import Metadata as AgentMetadata
from app.ai.nodes.agents import base
from app.ai.nodes.tools.search import search_tool


class Researcher(dspy.Module):
    """Node for research tasks"""

    def __init__(self, metadata: AgentMetadata):
        self.metadata = metadata
        self.lm = AgentManagement(metadata=self.metadata).get_lm()
        self.enhance_query = dspy.ChainOfThought(base.EnhanceQueryNode)
        self.reasoner = dspy.ChainOfThought(base.ReasoningNode)
        self.search_tool = search_tool
        self.researcher = dspy.ReAct(base.QANode, tools=[self.search_tool])

    async def forward(self, query: str):
        enhancements = await self.reasoner.acall(query)
        enhanced_query = await self.enhance_query.acall(
            query=query,
            keywords=enhancements.keywords,
            reasoning=enhancements.reasoning,
        ).enhanced_query
        search_results = await self.researcher.acall(
            question=enhanced_query,
            context="Search for the answer. There's no context available yet.",
        ).answer
        return search_results

class ResearcherSync(Researcher):
    def __init__(self, metadata: AgentMetadata):
        super().__init__(metadata)

    def forward(self, query: str):
        enhancements = self.reasoner(query)
        enhanced_query = self.enhance_query(
            query=query,
            keywords=enhancements.keywords,
            reasoning=enhancements.reasoning,
        ).enhanced_query
        search_results = self.researcher(
            question=enhanced_query,
            context="Search for the answer. There's no context available yet.",
        ).answer
        return search_results
