import ast
import TCC
import ATFD
import WMC

source = """
class Calc():
    def __init__():
        self.m1 = 0
        self.m2 = 0
        self.m3 = 0
        self.m4 = 0
        self.m5 = 0

    def f1():
        if True:
            if False:
                pass
            else:
                pass
        self.m1 = 1
        self.m2 = 2

    def f2():
        self.f1()
        self.f3()
        self.m4 = 4
        print("hoge")

    def f3():
        while(False):
            self.f3()
        self.m5 = 5

    def f4():
        Math.gcd(1, 2)
        self.m5 = 5
        self.marray[1] = 1
        ClassA.member1.method()


class Math():
    def gcd(x, y):
        return 0
"""

source2 = """
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
            tcc[each_class] = direct_connected_method_pairs[
                                  each_class] / total_method_pairs if total_method_pairs > 0 else 0
            # print("dc_pair" ":", direct_connected_method_pairs[each_class])
            # print("TCC of", each_class, "=", tcc[each_class])
        nx.draw_networkx(self.call_access_graph, font_size=8)
        plt.show()
        print("TCC :", str(tcc))
        return tcc

    def count_dc_method_pairs(self, each_class) -> int:
        # print("class_methods_map", str(self.class_methods_map))
        # print("member_set", str(self.class_member_map))

        pairs = 0
        method_pairs = list(itertools.combinations(self.class_methods_map[each_class], 2))

        # 各メソッドの組合せについて考える
        for method_pair in method_pairs:
            method_fir = (each_class, method_pair[0])
            method_sec = (each_class, method_pair[1])
            # print("method pair", str(method_pair))
            flag = False
            for member in self.class_member_map[each_class]:
                reachable = nx.single_target_shortest_path(self.call_access_graph, (each_class, member))
                # print("reachable", str(reachable))
                # print(str((each_class, member)))
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
        self.method_name = None
        self.class_set.add(node.name)
        self.generic_visit(node)
        return node

    def visit_Attribute(self, node: ast.Attribute) -> Any:
        if self.method_name is None:
            # 継承するスーパークラスを表す。ここは無視
            self.generic_visit(node)
            return node

        attr_belonging = node.value
        if isinstance(attr_belonging, ast.Name):
            member_class = attr_belonging.id
            if member_class == "self":
                member_class = self.class_name

            # magic_methodは無視する
            if not self.method_name.startswith("__"):
                self.class_member_map.setdefault(member_class, set())
                self.class_member_map[member_class].add(node.attr)
                print("Attr:", str((member_class, self.method_name)), str((member_class, node.attr)))
                self.call_access_graph.add_edge((self.class_name, self.method_name), (member_class, node.attr))

            return member_class
        else:
            self.generic_visit(node)
        return node

    def visit_Call(self, node: ast.Call) -> Any:
        # print(ast.dump(node))
        # node.funcのType次第で扱いが変わる
        if isinstance(node.func, ast.Name):
            # メソッド名(変数名)のような形
            self.call_access_graph.add_edge((self.class_name, self.method_name), node.func.id)
        elif isinstance(node.func, ast.Attribute):
            # ~~~.メソッド名()という形
            if isinstance(node.func.value, ast.Name):
                called_func = node.func.attr
                call_class = self.visit(node.func)
                if call_class == "self":
                    call_class = self.class_name
                self.call_access_graph.add_edge((self.class_name, self.method_name),
                                                (call_class, called_func))

        self.generic_visit(node)
        return node

"""
tree = ast.parse(source2)
hoge = TCC.TCCCalculator()
hoge.visit(tree)
hoge.calc_TCC()
counter = WMC.WMCCounter()
counter.visit(tree)
counter.calc_wmc()
atfd = ATFD.ATFDCalculator()
atfd.visit(tree)
atfd.calc_ATFD()
