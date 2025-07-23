import dspy

from app.ai.agents import Management as AgentManagement, Metadata as AgentMetadata
from app.ai.nodes.agents.base import ReasoningNode

class CreativeNode(dspy.Signature):
    """Creative node for generating creative content"""

    query: str = dspy.InputField(desc="The creative task to be performed")
    keywords: list[str] = dspy.InputField(
        desc="Keywords related to the query"
    )
    reasoning: str = dspy.InputField(desc="The thought process made")
    creative_output: str = dspy.OutputField(
        desc="The creative output generated"
    )

class CreativeAgent(dspy.Module):
    """Creative agent for generating creative content"""

    def __init__(self, metadata: AgentMetadata):
        self.metadata = metadata
        self.lm = AgentManagement(metadata=self.metadata).get_lm()
        self.reasoner = dspy.ChainOfThought(ReasoningNode)
        self.creative_generator = dspy.Predict(CreativeNode)

    async def forward(self, query: str):
        enhancements = await self.reasoner.acall(query)
        creative_output = await self.creative_generator.acall(
            query=query,
            keywords=enhancements.keywords,
            reasoning=enhancements.reasoning,
        ).creative_output
        return creative_output

class CreativeAgentSync(dspy.Module):
    """Creative agent for generating creative content"""

    def __init__(self, metadata: AgentMetadata):
        self.metadata = metadata
        self.lm = AgentManagement(metadata=self.metadata).get_lm()
        self.reasoner = dspy.ChainOfThought(ReasoningNode)
        self.creative_generator = dspy.Predict(CreativeNode)

    def forward(self, query: str):
        enhancements = self.reasoner(query)
        creative_output = self.creative_generator(
            query=query,
            keywords=enhancements.keywords,
            reasoning=enhancements.reasoning,
        ).creative_output
        return creative_output
