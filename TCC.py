import ast
from typing import Any
import itertools


class TCCCalculator(ast.NodeVisitor):
    def __init__(self):
        self.method_attr_access = {}
        self.name = None

    def calc_TCC(self) -> float:
        direct_connected_method_pairs = self.count_dc_method_pairs()
        total_methods = self.count_total_methods()
        total_method_pairs = total_methods * (total_methods - 1) / 2.0
        tcc = direct_connected_method_pairs / total_method_pairs
        print(tcc)
        return tcc

    def count_dc_method_pairs(self) -> int:
        method_pairs = list(itertools.combinations(self.method_attr_access.keys(), 2))
        pairs = 0
        for method_pair in method_pairs:
            acc_fir = self.method_attr_access[method_pair[0]]
            acc_sec = self.method_attr_access[method_pair[1]]
            if len(acc_fir & acc_sec) > 0:
                pairs += 1

        return pairs

    def count_total_methods(self) -> int:
        return len(self.method_attr_access)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.name = node.name
        self.method_attr_access.setdefault(self.name, set())
        self.generic_visit(node)
        return node

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        print("Method : ", self.name)
        print(node.value.id, " <------> ", node.attr)
        access_set = self.method_attr_access[self.name]
        access_set.add((node.value.id, node.attr))
        self.generic_visit(node)
        return node


source = """
class Calc():
    val = 0

    def assign(self, x):
        self.val=x

    def add(self, x):
        self.val+=x

    def ret(self, x):
        return 0


"""

tree = ast.parse(source)
calc = TCCCalculator()
calc.visit(tree)
calc.calc_TCC()
print(str(calc.method_attr_access))