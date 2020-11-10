import ast
from typing import Any


class PrintNodeVisitor(ast.NodeVisitor):
    def __init__(self):
        self.name = None

    def visit(self, node):
        print(node)
        return super().visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        print("-------")
        # print(ast.dump(node))
        print(node.name)
        print(len(node.body))
        for fs in node.body:
            if isinstance(fs, ast.FunctionDef):
                print(fs.name)
        print("-------")
        self.generic_visit(node)
        return node

    def visit_Name(self, node: ast.Name) -> Any:
        print("-------")
        print("name: ", ast.dump(node))
        print("-------")
        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.name = node.name
        self.generic_visit(node)
        return node

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        print("Method : ", self.name)
        print(node.value.id, " <------> ", node.attr)
        self.generic_visit(node)
        return node

    def visit_Call(self, node: ast.Call) -> Any:
        print(ast.dump(node))
        if isinstance(node.func, ast.Attribute):
            print("here!")
            print("-----", node.func.value.id, " ", node.func.attr, "-------")
        elif isinstance(node.func, ast.Name):
            print("-----", node.func.id, "-------")
        return node



source = """
class A():
    pass

class B():
    pass
"""

tree = ast.parse(source)
PrintNodeVisitor().visit(tree)
