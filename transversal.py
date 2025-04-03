# transversal.py

from hyperflow import HyperFlow, Spinor
from manifold import Manifold

class SurpriseEngine:
    @staticmethod
    def surprise(similarity: float) -> float:
        # Surprise is inverse of similarity
        return 1.0 - similarity

    @staticmethod
    def sentiment(previous: float, current: float) -> float:
        # Change in influence
        return current - previous

class Transversal:
    def __init__(self, manifold: Manifold):
        self.manifold = manifold

    def move(self, from_flow: HyperFlow, to_id: str) -> HyperFlow:
        target = self.manifold.get_flow(to_id)
        if not target:
            raise ValueError(f"Target HyperFlow {to_id} not found.")

        previous_spinor = target.spinor_embedding or from_flow.spinor_embedding
        updated = target.visit(from_flow.spinor_embedding)

        # Compute similarity for surprise
        sim = updated.spinor_embedding.similarity(previous_spinor)
        updated.metadata['surprise'] = SurpriseEngine.surprise(sim)
        updated.metadata['sentiment'] = SurpriseEngine.sentiment(0.5, sim)  # Static baseline for now

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
        sim = {}
        for fid, other in self.manifold.state.items():
            if other.spinor_embedding:
                sim[fid] = flow.spinor_embedding.similarity(other.spinor_embedding)
        return sorted(sim.items(), key=lambda x: x[1], reverse=True)
