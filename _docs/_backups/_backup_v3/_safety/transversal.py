# transversal.py

from hyperflow import HyperFlow, Spinor
from manifold import Manifold

class Transversal:
    def __init__(self, manifold: Manifold):
        self.manifold = manifold

    def move(self, from_flow: HyperFlow, to_id: str) -> HyperFlow:
        target = self.manifold.get_flow(to_id)
        if not target:
            raise ValueError(f"Target HyperFlow {to_id} not found.")

        # Simulate spinor rotation and record
        updated = target.visit(from_flow.spinor_embedding)
        self.manifold.tick(updated)
        return updated

    def walk_path(self, path: list[str], seed_spinor: Spinor):
        visited = []
        current = self.manifold.get_flow(path[0])
        current.visit(seed_spinor)
        self.manifold.tick(current)
        visited.append(current)

        for node_id in path[1:]:
            current = self.move(current, node_id)
            visited.append(current)

        return visited

    def reflect(self, flow: HyperFlow):
        # Placeholder reflection logic
        sim = {}
        for fid, other in self.manifold.state.items():
            if other.spinor_embedding:
                sim[fid] = flow.spinor_embedding.similarity(other.spinor_embedding)
        return sorted(sim.items(), key=lambda x: x[1], reverse=True)