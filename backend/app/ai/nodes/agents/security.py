import dspy
from typing import Literal
from app.ai.agents import Management as AgentManagement, Metadata as AgentMetadata

class SecurityNode(dspy.Signature):
    """Security node for checking security"""

    query: str = dspy.InputField(desc="The security check to be performed")
    security_check: Literal["passed", "failed"] = dspy.OutputField(desc="The security check result")

class SecurityAgent(dspy.Module):
    """Security agent for checking security"""

    def __init__(self, metadata: AgentMetadata):
        self.metadata = metadata
        self.lm = AgentManagement(metadata=self.metadata).get_lm()
        self.security_checker = dspy.Predict(SecurityNode)

    async def forward(self, query: str) -> Literal["passed", "failed"]:
        with dspy.context(lm=self.lm):
            security_check = await self.security_checker.acall(query=query)
            return security_check.security_check
