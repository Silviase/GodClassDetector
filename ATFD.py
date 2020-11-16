import ast
from typing import Any


class ATFDCalculator(ast.NodeVisitor):
    def __init__(self):
        self.method_name = None
        self.class_set = set()
        self.class_name = None
        self.name = None
        self.foreign_access_methods_dict = {}
        self.atfd_dict = {}

    def calc_ATFD(self):
        for key in self.foreign_access_methods_dict.keys():
            self.atfd_dict[key] = len(self.foreign_access_methods_dict[key])
        print("ATFD :", str(self.atfd_dict))

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        if self.method_name is None:
            # 継承するスーパークラスを表す。ここは無視
            self.generic_visit(node)
            return node

        attr_belonging = node.value
        if isinstance(attr_belonging, ast.Name):
            member_class = attr_belonging.id
            if node.value.id != "self":
                # self.foreign_access_methods.add(node.name)
                self.foreign_access_methods_dict.setdefault(self.class_name, set())
                self.foreign_access_methods_dict[self.class_name].add(self.method_name)

            return member_class
        else:
            self.generic_visit(node)
        return node

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.class_name = node.name
        self.class_set.add(node.name)
        self.generic_visit(node)
        return node

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.method_name = node.name
        self.generic_visit(node)
        return node


if __name__ == '__main__':
    source = ""
    tree = ast.parse(source)
    atfd = ATFDCalculator()
    atfd.visit(tree)
    print(atfd.calc_ATFD())
