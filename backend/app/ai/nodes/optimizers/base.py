import dspy
from dspy.evaluate import SemanticF1
from dspy.teleprompt import BootstrapFewShot
from dspy import Example

metric = SemanticF1()
teleprompt = BootstrapFewShot(metric=metric, max_rounds=2)

def optimize_program(program: dspy.Module, trainset: list[Example]) -> dspy.Module:
    """Optimize the prompt for the given program"""
    return teleprompt.compile(student=program, trainset=trainset)


