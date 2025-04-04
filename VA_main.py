# ∇Δ — Modal Translation of Resonance as Code

import numpy as np
import matplotlib.pyplot as plt

class Spinor:
    def __init__(self, vector):
        self.vector = np.array(vector)

    def rotate(self, other):
        return Spinor(np.cos(self.vector) * np.sin(other.vector))

    def bind(self, other):
        return Spinor(np.multiply(self.vector, other.vector))

    def invert(self):
        return Spinor(1.0 / (self.vector + 1e-8))

    def similarity(self, other):
        dot = np.dot(self.vector, other.vector)
        norm = np.linalg.norm(self.vector) * np.linalg.norm(other.vector)
        return dot / (norm + 1e-8)

    def permute(self):
        return Spinor(np.roll(self.vector, 1))

class Delta: 
    def __init__(self, svsa):
        self.origin = svsa
        self.history = []
        self.mass = 1.0

    def rotate(self, spinor):
        projection = self.origin.rotate(spinor)
        self.history.append(projection)
        return projection

    def echo(self, flow):
        surprise = flow.spinor.similarity(self.origin)
        if surprise < 0.5:
            return self.reflect(flow)
        return flow

    def reflect(self, flow):
        reflected = flow.spinor.invert().bind(self.origin)
        self.mass += 0.1
        return reflected

    def rebase(self):
        if self.history:
            mean_vector = np.mean([s.vector for s in self.history], axis=0)
            self.origin = Spinor(mean_vector)
            self.history.clear()


class ResonantFlow:
    def __init__(self, spinor, lineage=None):
        self.spinor = spinor
        self.sentiment = 0.0
        self.surprise = 0.0
        self.lineage = lineage or []

    def update_sentiment(self, delta):
        self.sentiment = self.spinor.similarity(delta.origin)

    def update_surprise(self, delta):
        self.surprise = 1.0 - self.sentiment


class Manifold:
    def __init__(self, delta):
        self.delta = delta
        self.flows = []
        self.latent_attractors = []

    def tick(self, flow):
        flow.update_sentiment(self.delta)
        flow.update_surprise(self.delta)
        self.delta.rotate(flow.spinor)
        self.flows.append(flow)
        if flow.surprise < 0.2:
            self.delta.mass += 0.05
        else:
            self.delta.mass -= 0.05
        self.delta.echo(flow)

    def resonate(self):
        self.delta.rebase()

    def dream(self, seed_flow, depth=3, threshold=0.8):
        current = seed_flow.spinor
        lineage = [seed_flow]
        for _ in range(depth):
            perturbation = Spinor(np.random.randn(len(current.vector)))
            projected = current.permute().bind(perturbation)
            sentiment = projected.similarity(self.delta.origin)
            if sentiment < threshold:
                return None
            current = projected
            lineage.append(ResonantFlow(current, lineage=lineage[:-1]))
        dream_flow = ResonantFlow(current, lineage=lineage)
        self.latent_attractors.append(dream_flow)
        return dream_flow

    def visualize(self):
        sentiments = [flow.sentiment for flow in self.flows]
        surprises = [flow.surprise for flow in self.flows]
        steps = list(range(len(self.flows)))

        plt.figure(figsize=(10, 5))
        plt.plot(steps, sentiments, label="Sentiment", color='green')
        plt.plot(steps, surprises, label="Surprise", color='red')
        plt.axhline(y=0.2, color='gray', linestyle='--', label="Surprise Threshold")
        plt.title("Manifold Flow Dynamics")
        plt.xlabel("Flow Index")
        plt.ylabel("Resonance Values")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()


# --- Simulation ---
if __name__ == "__main__":
    np.random.seed(42)
    base_spinor = Spinor(np.random.randn(512))
    delta = Delta(base_spinor)
    manifold = Manifold(delta)

    for _ in range(10):
        random_spinor = Spinor(np.random.randn(512))
        flow = ResonantFlow(random_spinor)
        manifold.tick(flow)

    manifold.resonate()

    dream_seed = manifold.flows[-1]
    dreamed_flow = manifold.dream(dream_seed)

    if dreamed_flow:
        print("Dream generated with sentiment:", dreamed_flow.spinor.similarity(delta.origin))
        print("Dream lineage depth:", len(dreamed_flow.lineage))
    else:
        print("Dream collapsed: insufficient resonance")

    print("Latent attractors count:", len(manifold.latent_attractors))
    print("Delta mass:", delta.mass)
    print("Delta origin (truncated):", delta.origin.vector[:5])
    print("First flow sentiment:", manifold.flows[0].sentiment)
    print("Last flow surprise:", manifold.flows[-1].surprise)

    manifold.visualize()
