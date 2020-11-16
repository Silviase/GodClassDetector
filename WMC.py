import ast
from typing import Any


class WMCCounter(ast.NodeVisitor):
    def __init__(self):
        self.cmp_dict = {}
        self.now = None

    def visit(self, node):
        # print(ast.dump(node))
        return super().visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.now = node.name
        self.cmp_dict[self.now] = 0
        self.generic_visit(node)
        return node

    def generic_visit(self, node):
        if isinstance(node, (ast.FunctionDef,
                             ast.For,
                             ast.AsyncFor,
                             ast.While,
                             ast.If,
                             ast.IfExp,
                             ast.BoolOp,
                             ast.ExceptHandler)):
            self.cmp_dict[self.now] += 1
        # generic_visitを行う
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item)
            elif isinstance(value, ast.AST):
                self.visit(value)
        return node

    def get_cmp_list(self) -> dict:
        return self.cmp_dict

    def calc_wmc(self) -> int:
        print("WMC :", str(self.cmp_dict))
        return sum(self.cmp_dict.values())


def main():
    source = ""
    tree = ast.parse(source)
    counter = WMCCounter()
    counter.visit(tree)
    print(counter.get_cmp_list())
    print(counter.calc_wmc())


if __name__ == "__main__":
    main()
