import ast
from typing import Any
import itertools
import networkx as nx
import matplotlib.pyplot as plt


class TCCCalculator(ast.NodeVisitor):
    def __init__(self):
        self.class_name = None
        self.method_name = None
        self.call_access_graph = nx.DiGraph()
        self.class_set = set()
        self.member_set = set()
        self.method_set = set()

    def calc_TCC(self) -> float:
        direct_connected_method_pairs = self.count_dc_method_pairs()
        total_methods = self.count_total_methods()
        total_method_pairs = total_methods * (total_methods - 1) / 2.0
        tcc = direct_connected_method_pairs / total_method_pairs
        print("method pair :", total_method_pairs)
        print("dc_pair :", direct_connected_method_pairs)
        print("TCC :", tcc)
        nx.draw_networkx(calc.call_access_graph,  font_size=8)
        plt.show()
        return tcc

    # TODO 各クラスにおいて計算するようにする
    def count_dc_method_pairs(self) -> int:
        print("method_set", str(self.method_set))
        print("member_set", str(self.member_set))
        method_pairs = list(itertools.combinations(self.method_set, 2))
        pairs = 0
        for method_pair in method_pairs:
            method_fir = method_pair[0]
            method_sec = method_pair[1]
            print("method pair", str(method_pair))
            flag = False
            for member in self.member_set:
                reachable = nx.single_target_shortest_path(self.call_access_graph, member)
                print(reachable)
                if method_fir in reachable and method_sec in reachable:
                    flag = True
                    break
            if flag:
                pairs += 1
        return pairs

    def count_total_methods(self) -> int:
        return len(self.method_set)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.method_name = node.name
        self.method_set.add((self.class_name, self.method_name))
        self.generic_visit(node)
        return node

    def visit_ClassDef(self, node: ast.ClassDef) -> Any:
        self.class_name = node.name
        self.class_set.add(node.name)
        self.generic_visit(node)
        return node

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        # print("Method : ", self.name)
        # print(node.value.id, " <------> ", node.attr)
        member_class = node.value.id
        if member_class == "self":
            member_class = self.class_name

        if not self.method_name.startswith("__"):
            self.member_set.add((member_class, node.attr))
            self.call_access_graph.add_edge((member_class, self.method_name),
                                            (member_class, node.attr))
        self.generic_visit(node)
        return node

    def visit_Call(self, node: ast.Call) -> Any:
        if isinstance(node.func, ast.Attribute):
            call_class = node.func.value.id
            if call_class == "self":
                call_class = self.class_name
            self.call_access_graph.add_edge((self.class_name, self.method_name),
                                            (call_class, node.func.attr))
        elif isinstance(node.func, ast.Name):
            self.call_access_graph.add_edge((self.class_name, self.method_name),
                                            node.func.id)
        return node


source = """
class Calc():
    def __init__():
        self.m1 = 0
        self.m2 = 0
        self.m3 = 0
        self.m4 = 0
        self.m5 = 0
        
    def f1():
        self.m1 = 1
        self.m2 = 2
    
    def f2():
        self.f1()
        self.f3()
        self.m4 = 4
    
    def f3():
        while(False):
            self.f3()
        self.m5 = 5
        
    def f4():
        Math.gcd(1, 2)
        self.m5 = 5

class Math():
    def gcd(x, y):
        return 0
"""

tree = ast.parse(source)
calc = TCCCalculator()
calc.visit(tree)
calc.calc_TCC()


