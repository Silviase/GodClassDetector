import ast
from typing import Any, Dict
import itertools
import networkx as nx
import matplotlib.pyplot as plt


class TCCCalculator(ast.NodeVisitor):
    def __init__(self):
        self.class_name = None
        self.method_name = None
        self.call_access_graph = nx.DiGraph()
        self.class_set = set()

        # Dict["class_name": {methods, member}]
        self.class_methods_map = {}
        self.class_member_map = {}

    def calc_TCC(self) -> Dict[Any, float]:
        direct_connected_method_pairs = {}  # {"class": int}
        tcc = {}
        for each_class in self.class_methods_map.keys():
            # 各クラスについてDCなメソッドの組を数える
            direct_connected_method_pairs[each_class] = self.count_dc_method_pairs(each_class)
            # 各クラスについてメソッドの数を数える
            total_methods = self.count_total_methods(each_class)
            total_method_pairs = total_methods * (total_methods - 1) / 2.0
            # それぞれのTCCを計算する
            tcc[each_class] = direct_connected_method_pairs[each_class] / total_method_pairs if total_method_pairs > 0 else 0
            print("dc_pair" ":", direct_connected_method_pairs[each_class])
            print("TCC of", each_class, "=", tcc[each_class])

        nx.draw_networkx(calc.call_access_graph, font_size=8)
        plt.show()
        return tcc

    def count_dc_method_pairs(self, each_class) -> int:
        print("class_methods_map", str(self.class_methods_map))
        print("member_set", str(self.class_member_map))

        pairs = 0
        method_pairs = list(itertools.combinations(self.class_methods_map[each_class], 2))

        # 各メソッドの組合せについて考える
        for method_pair in method_pairs:
            method_fir = (each_class, method_pair[0])
            method_sec = (each_class, method_pair[1])
            print("method pair", str(method_pair))
            flag = False
            for member in self.class_member_map[each_class]:
                reachable = nx.single_target_shortest_path(self.call_access_graph, (each_class, member))
                print("reachable", str(reachable))
                print(str((each_class, member)))
                if method_fir in reachable and method_sec in reachable:
                    flag = True
                    break
            if flag:
                pairs += 1
        return pairs

    # classごとのメソッド数をreturn
    def count_total_methods(self, class_name) -> int:
        return len(self.class_methods_map[class_name])

    def visit_FunctionDef(self, node: ast.FunctionDef) -> Any:
        self.method_name = node.name
        self.class_methods_map.setdefault(self.class_name, set())
        self.class_methods_map[self.class_name].add(self.method_name)
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
            self.class_member_map.setdefault(member_class, set())
            self.class_member_map[member_class].add(node.attr)
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
