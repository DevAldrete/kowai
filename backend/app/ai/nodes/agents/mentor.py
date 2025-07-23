import dspy

from app.ai.agents import Management as AgentManagement, Metadata as AgentMetadata
from app.ai.nodes.agents.base import ReasoningNode

class MentorNode(dspy.Signature):
    """Mentor node for providing guidance"""

    query: str = dspy.InputField(desc="The guidance to be provided")
    keywords: list[str] = dspy.InputField(
        desc="Keywords related to the query"
    )
    reasoning: str = dspy.InputField(desc="The thought process made")
    guidance: str = dspy.OutputField(desc="The guidance provided")

class MentorAgent(dspy.Module):

    def __init__(self, metadata: AgentMetadata):
        self.lm = AgentManagement(metadata=metadata).get_lm()
        self.reasoner = dspy.ChainOfThought(ReasoningNode)
        self.mentor = dspy.Predict(MentorNode)

    async def forward(self, query: str):
        enhancements = await self.reasoner.acall(query)
        guidance = await self.mentor.acall(
            query=query,
            keywords=enhancements.keywords,
            reasoning=enhancements.reasoning,
        ).guidance

        return guidance

class MentorAgentSync(dspy.Module):

    def __init__(self, metadata: AgentMetadata):
        self.lm = AgentManagement(metadata=metadata).get_lm()
        self.reasoner = dspy.ChainOfThought(ReasoningNode)
        self.mentor = dspy.Predict(MentorNode)

    def forward(self, query: str):
        enhancements = self.reasoner(query)
        guidance = self.mentor(
            query=query,
            keywords=enhancements.keywords,
            reasoning=enhancements.reasoning,
        ).guidance

        return guidance

