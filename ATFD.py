import ast
from typing import Any

class ATFDCalculator(ast.NodeVisitor):
    def __init__(self):
        self.foreign_access_methods = set()
        self.name = None

    def calc_ATFD(self) -> float:
        return len(self.foreign_access_methods)

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        if node.value.id != "self":
            self.foreign_access_methods.add(self.name)
        self.generic_visit(node)
        return node


source = """
class Calc():
    val = 0

    def assign(self, x):
        self.val=x

    def add(self, x):
        self.val+=x

    def gcd(a, b):
        return math.gcd(a,b)
        

"""

tree = ast.parse(source)
atfd = ATFDCalculator()
atfd.visit(tree)
print(atfd.calc_ATFD())
