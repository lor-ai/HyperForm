# Evolutionary Scheduler Scaffold for Δ Conditioning
import os
import json
import numpy as np
from pathlib import Path
from datetime import datetime
from shutil import copytree

# Hyperparameters for evolution
NUM_GENERATIONS = 5
POPULATION_SIZE = 4
MUTATION_STD = 0.15
DELTA_DIM = 512
BASE_VECTOR = np.ones(DELTA_DIM) * 0.5

# Fitness function weights (you can change these)
FITNESS_WEIGHTS = {
    "dream_valid": 3.0,
    "dream_lineage_depth": 1.0,
    "delta_mass": 0.5
}

def evaluate_fitness(summary):
    return (
        FITNESS_WEIGHTS["dream_valid"] * float(summary["dream_valid"]) +
        FITNESS_WEIGHTS["dream_lineage_depth"] * summary["dream_lineage_depth"] +
        FITNESS_WEIGHTS["delta_mass"] * summary["delta_mass"]
    )

def load_summaries(run_prefix):
    summaries = []
    for path in Path("run_logs").rglob(f"run_summary_*.json"):
        if run_prefix in str(path):
            with open(path) as f:
                data = json.load(f)
                summaries.append(data)
    return summaries

def mutate_vector(vec, std=MUTATION_STD):
    return vec + np.random.randn(len(vec)) * std

def blend_vectors(vectors):
    weights = np.random.dirichlet(np.ones(len(vectors)))
    return sum(w * v for w, v in zip(weights, vectors))

def evolve_population(parents):
    new_population = []
    for i in range(POPULATION_SIZE):
        p1, p2 = np.random.choice(parents, 2, replace=True)
        child = blend_vectors([p1, p2]) + np.random.randn(DELTA_DIM) * MUTATION_STD
        new_population.append(child)
    return new_population

def compare_memory_shift(current_vec, previous_vec):
    return np.linalg.norm(current_vec - previous_vec)

def should_trigger_model_update(memory_shift, threshold=0.25):
    return memory_shift > threshold

def log_event(event: dict, path="run_logs/evolution_events.json"):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        with open(path, "r") as f:
            events = json.load(f)
    else:
        events = []
    events.append(event)
    with open(path, "w") as f:
        json.dump(events, f, indent=2)

def evolutionary_schedule():
    current_vectors = [BASE_VECTOR + np.random.randn(DELTA_DIM) * 0.1 for _ in range(POPULATION_SIZE)]
    previous_best_vec = None

    for gen in range(NUM_GENERATIONS):
        print(f"===== Generation {gen} =====")
        seeds = [1000 + gen * 10 + i for i in range(POPULATION_SIZE)]
        delta_conditions = {i: current_vectors[i] for i in range(POPULATION_SIZE)}
        prefix = f"evolve_gen{gen}"

        # Run batch with conditions (requires integration with your batch_run)
        os.system(f"python your_script.py --prefix {prefix} --seeds {' '.join(map(str, seeds))} --condition")

        summaries = load_summaries(prefix)
        generate_dashboard(summaries, output=f"run_logs/dashboard_{prefix}.html")
        plot_lineage_graph(summaries, output=f"run_logs/lineage_graph_{prefix}.png")

        best = summaries[0]
        vec_path = Path("run_logs") / best["run_id"] / "delta_weights.npy"
        if vec_path.exists():
            delta_vec = np.load(vec_path)
            if previous_best_vec is not None:
                shift = compare_memory_shift(delta_vec, previous_best_vec)
                print(f"Δ memory shift from previous best: {shift:.4f}")
                log_event({
                    "generation": gen,
                    "run_id": best['run_id'],
                    "memory_shift": round(shift, 4),
                    "triggered_model_update": should_trigger_model_update(shift),
                    "timestamp": datetime.now().isoformat()
                })
                if should_trigger_model_update(shift):
                    print("Triggering model update: Δ memory shift exceeds threshold.")
            previous_best_vec = delta_vec.copy()
            try:
                import torch
                class RealisticModel(torch.nn.Module):
                    def embed_memory(self, memory_vector):
                        if hasattr(self, "memory"):
                            self.memory.data.copy_(torch.tensor(memory_vector))
                    def __init__(self):
                        super().__init__()
                        self.encoder = torch.nn.Linear(DELTA_DIM, 128)
                        self.decoder = torch.nn.Linear(128, 1)
                        self.memory = torch.nn.Parameter(torch.randn(DELTA_DIM), requires_grad=True)
                        self.decay_rate = 0.01
                    def forward(self, x):
                        self.memory.data = self.memory.data * (1.0 - self.decay_rate)
                        x_encoded = torch.relu(self.encoder(x))
                        x_mem = x_encoded + self.memory[:x_encoded.shape[1]]
                        return self.decoder(x_mem)
                model = RealisticModel()
                apply_to_model(model, delta_vec)
                model.embed_memory(delta_vec)
                output_sample = model(torch.ones(1, DELTA_DIM)).item()
                print(f"Injected best Δ into RealisticModel from {best['run_id']} | Output: {output_sample:.4f}")
            except Exception as e:
                print(f"[WARN] PyTorch injection failed: {e}")

        summaries.sort(key=evaluate_fitness, reverse=True)
        plot_memory_embeddings(summaries, output=f"run_logs/memory_projection_{prefix}.png")

        top = summaries[:2]
        parents = [np.load(f"run_logs/{s['run_id']}/delta_weights.npy") for s in top]
        current_vectors = evolve_population(parents)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--gens", type=int, default=NUM_GENERATIONS, help="Number of generations")
    parser.add_argument("--pop", type=int, default=POPULATION_SIZE, help="Population size")
    parser.add_argument("--animate", action="store_true", help="Enable memory animation")
    parser.add_argument("--run_type", choices=["full", "static"], default="full", help="Type of evolution")
    args = parser.parse_args()

    NUM_GENERATIONS = args.gens
    POPULATION_SIZE = args.pop

    print(f"[INFO] Running {args.run_type} evolution for {NUM_GENERATIONS} generations")
    
    current_vectors = [BASE_VECTOR + np.random.randn(DELTA_DIM) * 0.1 for _ in range(POPULATION_SIZE)]
    previous_best_vec = None

    for gen in range(NUM_GENERATIONS):
        print(f"\n===== Generation {gen} =====")
        seeds = [1000 + gen * 10 + i for i in range(POPULATION_SIZE)]
        delta_conditions = {i: current_vectors[i] for i in range(POPULATION_SIZE)}
        prefix = f"evolve_gen{gen}"

        # Run batch with conditions (requires integration with your batch_run)
        os.system(f"python your_script.py --prefix {prefix} --seeds {' '.join(map(str, seeds))} --condition")

        summaries = load_summaries(prefix)
        generate_dashboard(summaries, output=f"run_logs/dashboard_{prefix}.html")
        plot_lineage_graph(summaries, output=f"run_logs/lineage_graph_{prefix}.png")
        # Launch top Δ into model injection if valid
        best = summaries[0]
        vec_path = Path("run_logs") / best["run_id"] / "delta_weights.npy"
        if vec_path.exists():
            delta_vec = np.load(vec_path)
            if previous_best_vec is not None:
                shift = compare_memory_shift(delta_vec, previous_best_vec)
                print(f"Δ memory shift from previous best: {shift:.4f}")
                log_event({
                    "generation": gen,
                    "run_id": best['run_id'],
                    "memory_shift": round(shift, 4),
                    "triggered_model_update": should_trigger_model_update(shift),
                    "timestamp": datetime.now().isoformat()
                })
                if should_trigger_model_update(shift):
                    print("Triggering model update: Δ memory shift exceeds threshold.")
            previous_best_vec = delta_vec.copy()
            try:
                import torch
                class RealisticModel(torch.nn.Module):
                    def embed_memory(self, memory_vector):
                        if hasattr(self, "memory"):
                            self.memory.data.copy_(torch.tensor(memory_vector))
                    def __init__(self):
                        super().__init__()
                        self.encoder = torch.nn.Linear(DELTA_DIM, 128)
                        self.decoder = torch.nn.Linear(128, 1)
                        self.memory = torch.nn.Parameter(torch.randn(DELTA_DIM), requires_grad=True)
                        self.decay_rate = 0.01  # time-sensitive decay per forward  # now trainable
                    def forward(self, x):
                        # decay memory slightly
                        self.memory.data = self.memory.data * (1.0 - self.decay_rate)
                        x_encoded = torch.relu(self.encoder(x))
                        x_mem = x_encoded + self.memory[:x_encoded.shape[1]]  # combine with memory
                        return self.decoder(x_mem)
                    model = RealisticModel()
                    apply_to_model(model, delta_vec)
                    model.embed_memory(delta_vec)
                    output_sample = model(torch.ones(1, DELTA_DIM)).item()
                    print(f"Injected best Δ into RealisticModel from {best['run_id']} | Output: {output_sample:.4f}")
            except Exception as e:
                print(f"[WARN] PyTorch injection failed: {e}")
        summaries.sort(key=evaluate_fitness, reverse=True)
        plot_memory_embeddings(summaries, output=f"run_logs/memory_projection_{prefix}.png")

        top = summaries[:2]  # take top 2
        parents = [np.load(f"run_logs/{s['run_id']}/delta_weights.npy") for s in top]
        current_vectors = evolve_population(parents)

# Optional: PyTorch injection interface
try:
    import torch
    def apply_to_model(model, delta_vector):
        with torch.no_grad():
            for name, param in model.named_parameters():
                if param.data.ndim == 2 and param.shape[1] == DELTA_DIM:
                    param.copy_(torch.tensor(delta_vector).reshape(1, -1).expand_as(param))
                    break
except ImportError:
    print("PyTorch not available — skipping model injection helper.")

# Optional: HTML dashboard viewer (for later rendering)
def generate_dashboard(summaries, output="run_logs/dashboard.html"):
    lineage_paths = "".join(
        f"<li>{s['run_id']} → Δ mass: {s['delta_mass']:.2f}, depth: {s['dream_lineage_depth']}</li>"
        for s in sorted(summaries, key=lambda s: s.get('delta_mass', 0), reverse=True)
    )
    summaries.sort(key=lambda s: s.get('delta_mass', 0), reverse=True)
    rows = "".join(
        f"<tr><td>{s['run_id']}</td><td>{s['dream_valid']}</td><td>{s['dream_lineage_depth']}</td><td>{s['delta_mass']:.2f}</td></tr>"
        for s in summaries
    )
    mem_img = output.replace(".html", ".png").replace("dashboard_", "memory_projection_")
    mem_gif = mem_img.replace(".png", ".gif")
    mem_embed_html = f'<h2>Δ Memory Embedding</h2><img src="{Path(mem_gif).name}" width="600"/>' if Path(mem_gif).exists() else ""
    html = f"""
    <html><head><title>Δ Evolution Dashboard</title></head><body>
    <h1>Δ Evolution Results</h1>
    <ul>{lineage_paths}</ul>
    <html><head><title>Δ Evolution Dashboard</title></head><body>
    <h1>Δ Evolution Results</h1>
    <table border='1'>
        <tr><th>Run ID</th><th>Valid Dream</th><th>Lineage Depth</th><th>Δ Mass</th></tr>
        {rows}
    </table>
    {mem_embed_html}</body></html>
    """
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w") as f:
        f.write(html)
    img_name = output.replace(".html", ".png")
    if Path(img_name).exists():
        html = html.replace("</body>", f'<h2>Δ Lineage Graph</h2><img src="{Path(img_name).name}" width="600"/></body>')
        with open(output, "w") as f:
            f.write(html)
        print(f"Dashboard written to {output} (with embedded lineage graph)")

import networkx as nx
import matplotlib.pyplot as plt

def plot_lineage_graph(summaries, output="run_logs/lineage_graph.png"):
    G = nx.DiGraph()
    for i, s in enumerate(summaries):
        run_id = s.get("run_id", f"run_{i}")
        G.add_node(run_id, label=f"Δ mass: {s.get('delta_mass', 0):.2f}")
        if i > 0:
            G.add_edge(summaries[i - 1].get("run_id", f"run_{i - 1}"), run_id)
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(8, 6))
    nx.draw(G, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=8)
    labels = nx.get_node_attributes(G, 'label')
    for key, val in pos.items():
        plt.text(val[0], val[1] + 0.05, labels[key], horizontalalignment='center', fontsize=7)
    plt.title("Δ Lineage Graph")
    plt.tight_layout()
    plt.savefig(output)

    # Animation removed from plot_lineage_graph (handled in plot_memory_embeddings)
    print(f"Lineage graph saved to {output}")

from sklearn.decomposition import PCA

from matplotlib import animation

def plot_memory_embeddings(summaries, output="run_logs/memory_projection.png"):
    import matplotlib.pyplot as plt
    from IPython.display import HTML
    import matplotlib.pyplot as plt
    memory_vectors = []
    labels = []
    for s in summaries:
        vec_path = Path("run_logs") / s["run_id"] / "delta_weights.npy"
        if vec_path.exists():
            memory_vectors.append(np.load(vec_path))
            labels.append(s["run_id"])
    if len(memory_vectors) < 2:
        return
        print("Not enough memory vectors to project.")
        return
    pca = PCA(n_components=2)
    reduced = pca.fit_transform(memory_vectors)
    plt.figure(figsize=(7, 5))
    for i, label in enumerate(labels):
        plt.scatter(reduced[i, 0], reduced[i, 1], label=label)
        plt.text(reduced[i, 0], reduced[i, 1] + 0.01, label, fontsize=8, ha='center')
    plt.title("Δ Memory Embedding Space")
    plt.xlabel("PCA 1")
    plt.ylabel("PCA 2")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output)
    plt.close()
    print(f"Memory projection saved to {output}")

import argparse


