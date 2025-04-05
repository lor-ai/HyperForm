# Genetic Algorithm Kernel for Δ Evolution
import numpy as np
import json
import os
from pathlib import Path
from datetime import datetime

POP_SIZE = 8
GENS = 10
MUT_STD = 0.2
ELITISM = 2
DELTA_DIM = 512

def fitness_fn(summary):
    return (
        2.0 * float(summary["dream_valid"]) +
        1.0 * summary["dream_lineage_depth"] +
        0.5 * summary["delta_mass"]
    )

def mutate(vec, std=MUT_STD):
    return vec + np.random.randn(len(vec)) * std

def crossover(parent1, parent2):
    alpha = np.random.rand()
    return alpha * parent1 + (1 - alpha) * parent2

def load_summary_vectors(prefix):
    summaries = []
    for f in Path("run_logs").rglob(f"{prefix}*/run_summary_*.json"):
        with open(f) as file:
            data = json.load(file)
            data["path"] = str(f)
            summaries.append(data)
    summaries.sort(key=fitness_fn, reverse=True)
    vectors = []
    for s in summaries:
        vec_path = Path(s["path"]).parent / "delta_weights.npy"
        if vec_path.exists():
            vectors.append(np.load(vec_path))
    return summaries, vectors

def genetic_loop():
    population = [np.random.randn(DELTA_DIM) * 0.1 for _ in range(POP_SIZE)]

    for gen in range(GENS):
        prefix = f"ga_gen{gen}"
        seeds = [100 + gen * 10 + i for i in range(POP_SIZE)]
        print(f"\n-- Gen {gen} | Prefix: {prefix} --")

        # Save temporary delta_conditions.json
        delta_conditions = {i: population[i].tolist() for i in range(len(population))}
        with open("delta_conditions.json", "w") as f:
            json.dump(delta_conditions, f)

        # Run batch externally (replace with subprocess or function call)
        os.system(f"python your_script.py --prefix {prefix} --seeds {' '.join(map(str, seeds))} --condition")

        # Evaluate fitness
        summaries, vectors = load_summary_vectors(prefix)
        next_pop = vectors[:ELITISM]  # carry over elites

        while len(next_pop) < POP_SIZE:
            p1, p2 = np.random.choice(vectors, 2, replace=True)
            child = mutate(crossover(p1, p2))
            next_pop.append(child)

        population = next_pop

if __name__ == "__main__":
    genetic_loop()
