"""
DSPy-based node based approach for developing AI Worflows
"""

from enum import Enum

import dspy

from app.ai.agents import Management as AgentManagement
from app.ai.agents import Metadata as AgentMetadata
from app.core.logging.config import get_logger

logger = get_logger(__name__)


class PersonaType(str, Enum):
    """Available persona types"""

    ANALYST = "analyst"
    CREATIVE = "creative"
    RESEARCHER = "researcher"
    ADVISOR = "advisor"
    MENTOR = "mentor"


class ReasoningNode(dspy.Signature):
    """Reason step by step through the query for getting the correct outputs"""

    query: str = dspy.InputField()
    keywords: list[str] = dspy.OutputField(
        desc="Keywords generated according to the query"
    )
    reasoning: str = dspy.OutputField(desc="The though process made")


class EnhanceQueryNode(dspy.Signature):
    """Enhance the query with additional information"""

    query: str = dspy.InputField(desc="Original query")
    keywords: list[str] = dspy.InputField(desc="Keywords generated from the query")
    reasoning: str = dspy.InputField(desc="Reasoning behind the query")
    enhanced_query: str = dspy.OutputField(
        desc="Enhanced query with additional information"
    )


class QANode(dspy.Signature):
    """Signature for question-answering tasks"""

    question: str = dspy.InputField(desc="The question to be answered")
    context: str = dspy.InputField(
        desc="Context or background information for the question"
    )
    answer: str = dspy.OutputField(desc="The answer to the question")


class BaseAgent(dspy.Module):
    """Base class for AI agents"""

    def __init__(self, metadata: AgentMetadata):
        self.metadata = metadata
        self.lm = AgentManagement(metadata=self.metadata).get_lm()
        self.reasoner = dspy.ChainOfThought(ReasoningNode)
        self.enhance_query = dspy.ChainOfThought(EnhanceQueryNode)
        self.get_answer = dspy.Predict(QANode)

    async def forward(self, query: str):
        """Process the query and return the answer"""
        logger.info(f"Processing query: {query}")
        with dspy.context(lm=self.lm):
            enhancements = await self.reasoner.acall(query=query)
            enhanced_query = await self.enhance_query.acall(
                query=query,
                keywords=enhancements.keywords,
                reasoning=enhancements.reasoning,
            )
            answer = await self.get_answer.acall(
                question=enhanced_query.enhanced_query,
                context=enhancements.reasoning,
            )
            return answer.answer

class BaseAgentSync(dspy.Module):
    """Base class for AI agents"""

    def __init__(self, metadata: AgentMetadata):
        self.metadata = metadata
        self.lm = AgentManagement(metadata=self.metadata).get_lm()
        self.reasoner = dspy.ChainOfThought(ReasoningNode)
        self.enhance_query = dspy.ChainOfThought(EnhanceQueryNode)
        self.get_answer = dspy.Predict(QANode)

    def forward(self, query: str):
        """Process the query and return the answer"""
        logger.info(f"Processing query: {query}")
        enhancements = self.reasoner(query=query)
        enhanced_query = self.enhance_query(
            query=query,
            keywords=enhancements.keywords,
            reasoning=enhancements.reasoning,
        )
        answer = self.get_answer(
            question=enhanced_query.enhanced_query,
            context=enhancements.reasoning,
        )
        return answer.answer
