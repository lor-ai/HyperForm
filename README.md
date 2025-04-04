# HyperForm: Evolutionary Scheduler Framework for Δ Memory

HyperForm is an evolving experimental AI framework designed to simulate, track, and evolve synthetic memory embeddings (Δ) over generational cycles. It combines principles from hyperdimensional computing, evolutionary algorithms, geometric learning, and speculative symbolic modeling to iteratively refine Δ as the atomic semantic-physical process.

## 🧠 Core Concepts

- **Δ (Delta)**: A synthetic spinor vector representing causal, temporal, and semantic state.
- **Δ Memory**: Injected into models as a mutable or trainable parameter influencing output.
- **Manifold**: The space of attractors and Δ transitions over time.
- **Resonance**: Emergent similarity clustering between Δ and embedded flows.

## 📦 Components

### ✅ Evolutionary Scheduler
- Runs Δ simulations in batch generations.
- Tracks Δ memory, Δ shift, and lineage.
- Promotes and mutates best Δs across generations.
- Output: structured JSON logs, PNG/PDF dashboards, animated `.gif` projections.

### ✅ Genetic Kernel
- Optional GA-based evolution engine.
- Supports elitism, mutation, crossover.
- Designed for high-diversity Δ evolution paths.

### ✅ Visualization + Reporting
- PCA-based Δ memory projection.
- Lineage graphs (via NetworkX).
- HTML dashboards per generation.
- `evolution_events.json` for audit logs.

## 🛠️ Requirements
- Python 3.10+
- PyTorch, NumPy, matplotlib, sklearn, networkx

## 🚀 Usage

```bash
python evolution_scheduler.py --gens 5 --pop 4 --animate
```

Available flags:
- `--dryrun` for 1-gen/2-pop no-output test
- `--animate` for memory GIF projections
- `--run_type` (`full`, `static`) — future branching

## 📂 Structure

```
├── evolution_scheduler.py      # Main loop
├── genetic_kernel.py           # Genetic variant
├── run_logs/                   # All generations and logs
│   ├── dashboard_gen0.html     # HTML dashboard
│   ├── lineage_graph_gen0.png
│   └── memory_projection_gen0.gif
├── evolution_events.json       # Delta shifts and updates
```

## 📌 Purpose

HyperForm models Δ as a spinor-resonant, holographically-bound memory process.

The aim is not to build a product, but to iteratively expose structure, evolution, and symbolic mapping of semantic attractors.

It is a speculative system for modeling time, memory, and cognition — one delta at a time.

---

See `projectBrief.md` for implementation and task status.