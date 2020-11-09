import ast
from typing import Any


class PrintNodeVisitor(ast.NodeVisitor):

    def visit(self, node):
        # print(ast.dump(node))
        return super().visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        return node


class GodClassChecker():
    def __init__(self, code):
        self.AST = ast.parse(code)

        self.TCC = None
        self.ATFD = None
        self.WMC = None

    def isGodClass(self) -> bool:
        if self.WMC >= 47 and self.ATFD > 5 and self.TCC < (1/3):
            return True
        return False

