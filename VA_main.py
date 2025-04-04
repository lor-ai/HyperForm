# ∇Δ — Modal Translation of Resonance as Code

import numpy as np
import matplotlib.pyplot as plt
from spinor import Spinor  # Ensure spinor module provides required methods

class Delta: 
    """
    The seed of recursive unfolding. Not a point, but a principle of coherence.
    It evolves through recursive resonance, curvature, and spinor rotation.
    """
    def __init__(self, svsa):
        self.origin = svsa  # Spinor-encoded value-state
        self.history = []   # List of rotated projections
        self.mass = 1.0     # Resonance weight

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
        if len(self.history) > 0:
            accumulated = sum((s.vector for s in self.history), self.origin.vector * 0.0)
            mean_vector = accumulated / len(self.history)
            self.origin = Spinor(mean_vector)
            self.history.clear()


class ResonantFlow:
    """
    A process through the manifold, modulated by spinor alignment to Delta.
    """
    def __init__(self, spinor):
        self.spinor = spinor
        self.sentiment = 0.0
        self.surprise = 0.0

    def update_sentiment(self, delta):
        self.sentiment = self.spinor.similarity(delta.origin)

    def update_surprise(self, delta):
        self.surprise = 1.0 - self.sentiment


class Manifold:
    """
    Encodes recursive transformation memory and resonance field.
    """
    def __init__(self, delta):
        self.delta = delta
        self.flows = []

    def tick(self, flow):
        flow.update_sentiment(self.delta)
        flow.update_surprise(self.delta)
        self.delta.rotate(flow.spinor)
        self.flows.append(flow)
        if flow.surprise < 0.2:
            self.delta.mass += 0.05  # Resonance deepens
        else:
            self.delta.mass -= 0.05  # Fracture risk
        self.delta.echo(flow)

    def resonate(self):
        self.delta.rebase()

    def dream(self, seed_flow, depth=3, threshold=0.8):
        """
        Generate a recursive dream trajectory based on a seed flow.
        """
        current = seed_flow.spinor
        for _ in range(depth):
            perturbation = Spinor(np.random.randn(len(current.vector)))
            projected = current.rotate(Spinor([0.1]*len(current.vector))).bind(perturbation)
            sentiment = projected.similarity(self.delta.origin)
            if sentiment < threshold:
                return None
            current = projected
        return ResonantFlow(current)

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

    dream_seed = manifold.flows[-1]  # Use the last flow as seed for dream
    dreamed_flow = manifold.dream(dream_seed)

    if dreamed_flow:
        print("Dream generated with sentiment:", dreamed_flow.spinor.similarity(delta.origin))
    else:
        print("Dream collapsed: insufficient resonance")

    print("Delta mass:", delta.mass)
    print("Delta origin (truncated):", delta.origin.vector[:5])
    print("First flow sentiment:", manifold.flows[0].sentiment)
    print("Last flow surprise:", manifold.flows[-1].surprise)

    # Visualize
    manifold.visualize()
