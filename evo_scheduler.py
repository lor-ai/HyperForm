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

def evolutionary_schedule():
    current_vectors = [BASE_VECTOR + np.random.randn(DELTA_DIM) * 0.1 for _ in range(POPULATION_SIZE)]

    for gen in range(NUM_GENERATIONS):
        print(f"\n===== Generation {gen} =====")
        seeds = [1000 + gen * 10 + i for i in range(POPULATION_SIZE)]
        delta_conditions = {i: current_vectors[i] for i in range(POPULATION_SIZE)}
        prefix = f"evolve_gen{gen}"

        # Run batch with conditions (requires integration with your batch_run)
        os.system(f"python your_script.py --prefix {prefix} --seeds {' '.join(map(str, seeds))} --condition")

        summaries = load_summaries(prefix)
        generate_dashboard(summaries, output=f"run_logs/dashboard_{prefix}.html")
        summaries.sort(key=evaluate_fitness, reverse=True)

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
    rows = "".join(
        f"<tr><td>{s['run_id']}</td><td>{s['dream_valid']}</td><td>{s['dream_lineage_depth']}</td><td>{s['delta_mass']:.2f}</td></tr>"
        for s in summaries
    )
    html = f"""
    <html><head><title>Δ Evolution Dashboard</title></head><body>
    <h1>Δ Evolution Results</h1>
    <table border='1'>
        <tr><th>Run ID</th><th>Valid Dream</th><th>Lineage Depth</th><th>Δ Mass</th></tr>
        {rows}
    </table>
    </body></html>
    """
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    with open(output, "w") as f:
        f.write(html)
    print(f"Dashboard written to {output}")

if __name__ == "__main__":
    evolutionary_schedule()
