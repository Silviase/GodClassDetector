import ast
from typing import Any


class PrintNodeVisitor(ast.NodeVisitor):
    def visit(self, node):
        print(ast.dump(node))
        return super().visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        print("-------")
        print(ast.dump(node))
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
        return node


source = """
class Calc():
    val = 0
    
    def assign(self, x):
        self.val=x
        
    def add(self, x):
        self.val+=x

class Nothing():
    def do_nothing(self):
        return True and Truee
        
"""

tree = ast.parse(source)
PrintNodeVisitor().visit(tree)
