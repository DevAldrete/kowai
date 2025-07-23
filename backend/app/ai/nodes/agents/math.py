import dspy
from app.ai.agents import Metadata as AgentMetadata, Management as AgentManagement
from app.ai.nodes.agents.base import ReasoningNode, QANode

class MathNode(dspy.Signature):
    """Math node for solving math problems"""

    query: str = dspy.InputField(desc="The math problem to be solved")
    reasoning: str = dspy.InputField(desc="Reasoning behind the math problem")
    result: str = dspy.OutputField(desc="The answer to the math problem")

class MathAgent(dspy.Module):
    def __init__(self, metadata: AgentMetadata):
        self.lm = AgentManagement(metadata=metadata).get_lm()
        self.reasoner = dspy.ChainOfThought(ReasoningNode)
        self.solve = dspy.Predict(MathNode)

    async def forward(self, query: str):
        enhancements = await self.reasoner.acall(query)
        result = await self.solve.acall(query=query, reasoning=enhancements.reasoning).result
        return result

class MathAgentSync(dspy.Module):
    def __init__(self, metadata: AgentMetadata):
        self.lm = AgentManagement(metadata=metadata).get_lm()
        self.reasoner = dspy.ChainOfThought(ReasoningNode)
        self.solve = dspy.Predict(MathNode)

    def forward(self, query: str):
        enhancements = self.reasoner(query)
        result = self.solve(query=query, reasoning=enhancements.reasoning).result
        return result
