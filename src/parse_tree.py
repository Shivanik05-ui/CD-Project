import os
os.environ["PATH"] += os.pathsep + r"C:\Program Files\Graphviz\bin"

from graphviz import Digraph

class ParseTree:
    def __init__(self):
        self.graph = Digraph()
        self.node_count = 0

    def add_node(self, label):
        node_id = str(self.node_count)
        self.graph.node(node_id, label)
        self.node_count += 1
        return node_id

    def add_edge(self, parent, child):
        self.graph.edge(parent, child)

    def render(self, filename="parse_tree"):
        self.graph.render(filename, view=True)