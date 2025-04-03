# manifold_visualizer.py

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backend_bases import MouseEvent
from hyperflow import HyperFlow, Spinor
from manifold import Manifold
import random

class ManifoldVisualizer:
    def __init__(self, manifold: Manifold):
        self.manifold = manifold
        self.G = nx.DiGraph()
        self.pos = {}
        self.node_map = {}

    def build_graph(self):
        self.G.clear()
        self.node_map.clear()
        for flow_id, flow in self.manifold.state.items():
            self.G.add_node(flow_id, flow=flow)
            self.node_map[flow_id] = flow
            for tail in flow.connections.get("tails", []):
                self.G.add_edge(flow_id, tail)

    def draw(self):
        self.build_graph()

        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(10, 6))
        self.pos = nx.spring_layout(self.G, seed=42)

        node_colors = []
        node_labels = {}
        highlight_nodes = self._suggest_curiosity_targets()

        for i, node in enumerate(self.G.nodes):
            flow = self.node_map[node]
            visited = flow.visit_count > 0
            sentiment = flow.metadata.get("sentiment", 0.0)
            surprise = flow.metadata.get("surprise", 0.0)

            if node in highlight_nodes:
                node_colors.append("#ff9900")  # curiosity highlight
            elif visited:
                node_colors.append("#00ffd0")  # visited
            else:
                node_colors.append("#444444")  # unvisited

            emoji = "💖" if sentiment > 0.1 else ("💤" if sentiment < -0.1 else "⚪")
            spark = "✨" if surprise > 0.2 else ""
            node_labels[node] = f"{i} {emoji}{spark}"

        nx.draw(self.G, self.pos, with_labels=False, node_color=node_colors, node_size=800, edge_color="#888888")
        nx.draw_networkx_labels(self.G, self.pos, labels=node_labels, font_size=9)

        def on_click(event: MouseEvent):
            for node_id, coords in self.pos.items():
                x, y = coords
                if (event.xdata - x)**2 + (event.ydata - y)**2 < 0.02:
                    flow = self.node_map[node_id]
                    print("\n--- HyperFlow Metadata ---")
                    print(f"ID: {flow.static_id[:8]}")
                    print(f"Visit count: {flow.visit_count}")
                    for k, v in flow.metadata.items():
                        print(f"{k}: {v}")
                    print("---------------------------")

        fig.canvas.mpl_connect('button_press_event', on_click)
        plt.title("HyperForm Traversal Map")
        plt.tight_layout()
        plt.show()

    def _suggest_curiosity_targets(self):
        # Prioritize unvisited nodes with high surprise or low familiarity
        scores = {}
        for fid, flow in self.manifold.state.items():
            if flow.visit_count == 0:
                sim = flow.metadata.get("surprise", 0.0)
                scores[fid] = sim + random.uniform(0.01, 0.1)
        sorted_ids = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [fid for fid, _ in sorted_ids[:3]]

# Usage:
# from demo_flow import manifold
# viz = ManifoldVisualizer(manifold)
# viz.draw()
