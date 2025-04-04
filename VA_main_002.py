# ∇Δ — Modal Translation of Resonance as Code

import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

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
    def get_weight_matrix(self):
        return self.origin.vector.reshape(1, -1)  # or reshape for model injection

    def save_weights(self, name="delta_weights"):
        np.save(f"{name}.npy", self.origin.vector)

    def condition(self, external_vector, weight=0.5):
        blended = (1 - weight) * self.origin.vector + weight * np.array(external_vector)
        self.origin = Spinor(blended)
        self.transition_log.append(self.origin)

    def __init__(self, svsa):
        self.origin = svsa
        self.history = []
        self.mass = 1.0
        self.transition_log = []

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
            self.transition_log.append(self.origin)
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
        self.promoted = []
        self.faded = []

    def tick(self, flow):
        flow.update_sentiment(self.delta)
        flow.update_surprise(self.delta)
        for attractor in self.latent_attractors:
            flow.spinor = flow.spinor.bind(attractor.spinor)
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

    def project_attractors(self, steps=3):
        for attractor in self.latent_attractors[:]:
            current = attractor.spinor
            lineage = attractor.lineage[:]
            for _ in range(steps):
                projected = current.permute().rotate(self.delta.origin)
                flow = ResonantFlow(projected, lineage=lineage[:])
                self.tick(flow)
                lineage.append(flow)
                current = projected
            if attractor.sentiment > 0.9:
                self.promoted.append(attractor)
                self.delta.origin = attractor.spinor
                self.delta.transition_log.append(self.delta.origin)
            elif attractor.sentiment < 0.5:
                self.faded.append(attractor)
                self.latent_attractors.remove(attractor)

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

    def visualize_transitions(self):
        if len(self.delta.transition_log) < 2:
            print("No Δ transitions recorded.")
            return
        pca = PCA(n_components=2)
        vectors = [s.vector for s in self.delta.transition_log]
        reduced = pca.fit_transform(vectors)
        plt.figure(figsize=(8, 6))
        colors = np.linspace(0, 1, len(reduced))
        for i in range(1, len(reduced)):
            plt.plot([reduced[i-1, 0], reduced[i, 0]],
                     [reduced[i-1, 1], reduced[i, 1]],
                     color=plt.cm.viridis(colors[i]), linewidth=2)
        plt.scatter(reduced[:, 0], reduced[:, 1], c=colors, cmap='viridis', s=50, edgecolors='k')
        plt.title("Δ Transition Trajectory (Phase Space)")
        plt.xlabel("PCA 1")
        plt.ylabel("PCA 2")
        plt.colorbar(label="Time Step")
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def visualize_density(self):
        vectors = [flow.spinor.vector for flow in self.flows]
        if len(vectors) < 2:
            print("Need at least 2 flows to estimate density.")
            return
        if len(vectors) < 2:
            print("Insufficient flows for density visualization.")
            return
        pca = PCA(n_components=2)
        reduced = pca.fit_transform(vectors)
        x, y = reduced[:, 0], reduced[:, 1]
        plt.figure(figsize=(6, 5))
        plt.hist2d(x, y, bins=30, cmap='magma')
        plt.colorbar(label='Flow Density')
        plt.title("Flow Density in PCA Space")
        plt.xlabel("PCA 1")
        plt.ylabel("PCA 2")
        plt.tight_layout()
        plt.show()


import os
from datetime import datetime

# --- Simulation Logging and Versioned Artifact Output ---
def run_simulation(run_id="default"):
    log_dir = f"run_logs/{run_id}"
    os.makedirs(log_dir, exist_ok=True)

    def save_plot(prefix):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        version = len([f for f in os.listdir(log_dir) if f.startswith(prefix)]) + 1
        filename = f"{prefix}_v{version:02d}_{timestamp}.png"
        plt.savefig(os.path.join(log_dir, filename))
        plt.close()

    return save_plot, log_dir
def save_plot(prefix):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    version = len([f for f in os.listdir('.') if f.startswith(prefix)]) + 1
    filename = f"{prefix}_v{version:02d}_{timestamp}.png"
    plt.savefig(filename)
    plt.close()

import json

import argparse


import csv

def batch_run(seed_list, run_prefix="hyperrun", delta_conditions=None):
    summary_data = []

    for i, seed in enumerate(seed_list):
        run_id = f"{run_prefix}_{i:02d}"
        print(f"--- Starting batch run: {run_id} (seed={seed}) ---")
        save_plot, log_dir = run_simulation(run_id)
        np.random.seed(seed)
        base_spinor = Spinor(np.random.randn(512))
        delta = Delta(base_spinor)
        if delta_conditions and i in delta_conditions:
            delta.condition(delta_conditions[i], weight=0.7)
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

        manifold.project_attractors(steps=3)

        run_metadata = {
            "timestamp": datetime.now().isoformat(),
            "run_id": run_id,
            "seed": seed,
            "delta_mass": delta.mass,
            "num_flows": len(manifold.flows),
            "num_attractors": len(manifold.latent_attractors),
            "num_promoted": len(manifold.promoted),
            "num_faded": len(manifold.faded),
            "num_transitions": len(delta.transition_log),
            "dream_lineage_depth": len(dreamed_flow.lineage) if dreamed_flow else 0,
            "dream_valid": bool(dreamed_flow),
        }
        summary_path = os.path.join(log_dir, f"run_summary_{run_metadata['timestamp'].replace(':', '-')}.json")
        with open(summary_path, "w") as f:
            json.dump(run_metadata, f, indent=2)
        summary_data.append(run_metadata)

        manifold.visualize()
        save_plot("flow_dynamics")
        manifold.visualize_density()
        save_plot("flow_density")
        manifold.visualize_transitions()
        save_plot("delta_transitions")

    # Save CSV summary
    csv_path = os.path.join("run_logs", f"summary_{run_prefix}.csv")
    with open(csv_path, "w", newline="") as csvfile:
        fieldnames = list(summary_data[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_data)
    print(f"Batch summary saved to {csv_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--prefix", default="batch_test")
    parser.add_argument("--seeds", nargs="*", type=int, default=[42, 101, 202, 303])
    parser.add_argument("--condition", action="store_true")
    args = parser.parse_args()

    # Optional conditioning
    conditions = None
    if args.condition:
        vector = np.ones(512) * 0.5
        conditions = {i: vector for i in range(len(args.seeds))}

    batch_run(seed_list=args.seeds, run_prefix=args.prefix, delta_conditions=conditions)

    # Default single-run fallback (optional)
    batch_run(seed_list=[42, 101, 202, 303], run_prefix="batch_test")
    save_plot, log_dir = run_simulation("hyperrun")
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

    manifold.project_attractors(steps=3)

    print("Promoted attractors:", len(manifold.promoted))
    print("Faded attractors:", len(manifold.faded))
    print("Δ transitions logged:", len(delta.transition_log))

    # Export run metadata
    run_metadata = {
        "timestamp": datetime.now().isoformat(),
        "delta_mass": delta.mass,
        "num_flows": len(manifold.flows),
        "num_attractors": len(manifold.latent_attractors),
        "num_promoted": len(manifold.promoted),
        "num_faded": len(manifold.faded),
        "num_transitions": len(delta.transition_log),
        "dream_lineage_depth": len(dreamed_flow.lineage) if dreamed_flow else 0,
        "dream_valid": bool(dreamed_flow),
    }
    summary_path = os.path.join(log_dir, f"run_summary_{run_metadata['timestamp'].replace(':', '-')}.json")
    with open(summary_path, "w") as f:
        json.dump(run_metadata, f, indent=2)
        print("Run summary saved.")

    manifold.visualize()
    save_plot("flow_dynamics")
    plt.savefig("flow_dynamics_v1.png")
    plt.close()
    manifold.visualize_density()
    save_plot("flow_density")
    plt.savefig("flow_density_v1.png")
    plt.close()
    manifold.visualize_transitions()
    save_plot("delta_transitions")
    plt.savefig("delta_transitions_v1.png")
    plt.close()
    plt.savefig("delta_transitions.png")
    plt.close()
    plt.savefig("flow_dynamics.png")
    plt.close()
    manifold.visualize_transitions()
