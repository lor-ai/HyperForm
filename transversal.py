# transversal.py

from hyperflow import HyperFlow, Spinor
from manifold import Manifold

class SurpriseEngine:
    @staticmethod
    def surprise(similarity: float) -> float:
        return 1.0 - similarity

    @staticmethod
    def sentiment(previous: float, current: float) -> float:
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

        sim = updated.spinor_embedding.similarity(previous_spinor)
        updated.metadata['surprise'] = SurpriseEngine.surprise(sim)
        updated.metadata['sentiment'] = SurpriseEngine.sentiment(0.5, sim)

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

    def transverse_by_similarity(self, start_id: str, spinor: Spinor, steps: int = 5):
        current = self.manifold.get_flow(start_id)
        print("\n=== Spinor Similarity Traversal ===")

        for _ in range(steps):
            current.visit(spinor)
            self.manifold.tick(current)
            print(f"Visited: {current.static_id[:8]}")

            candidates = [fid for fid, flow in self.manifold.state.items()
                          if flow.visit_count == 0 and flow.spinor_embedding is not None]
            if not candidates:
                break

            scored = sorted(
                candidates,
                key=lambda fid: spinor.similarity(self.manifold.get_flow(fid).spinor_embedding),
                reverse=True
            )
            if not scored:
                break
            current = self.manifold.get_flow(scored[0])

        print("Similarity traversal complete.")