import dspy

from app.ai.agents import Management as AgentManagement, Metadata as AgentMetadata
from app.ai.nodes.agents.base import ReasoningNode

class AdvisorNode(dspy.Signature):
    """Finance advisor node for providing advice"""

    query: str = dspy.InputField(desc="The advice to be provided")
    keywords: list[str] = dspy.InputField(
        desc="Keywords related to the query"
    )
    reasoning: str = dspy.InputField(desc="The thought process made")
    advice: str = dspy.OutputField(desc="The advice provided")

class AdvisorAgent(dspy.Module):
    """Finance advisor agent for providing advice"""

    def __init__(self, metadata: AgentMetadata):
        self.metadata = metadata
        self.lm = AgentManagement(metadata=self.metadata).get_lm()
        self.reasoner = dspy.ChainOfThought(ReasoningNode)
        self.advisor = dspy.Predict(AdvisorNode)

    async def forward(self, query: str):
        enhancements = await self.reasoner.acall(query)
        advice = await self.advisor.acall(
            query=query,
            keywords=enhancements.keywords,
            reasoning=enhancements.reasoning,
        ).advice
        return advice

class AdvisorAgentSync(dspy.Module):
    """Finance advisor agent for providing advice"""

    def __init__(self, metadata: AgentMetadata):
        self.metadata = metadata
        self.lm = AgentManagement(metadata=self.metadata).get_lm()
        self.reasoner = dspy.ChainOfThought(ReasoningNode)
        self.advisor = dspy.Predict(AdvisorNode)

    def forward(self, query: str):
        enhancements = self.reasoner(query)
        advice = self.advisor(
            query=query,
            keywords=enhancements.keywords,
            reasoning=enhancements.reasoning,
        ).advice
        return advice
