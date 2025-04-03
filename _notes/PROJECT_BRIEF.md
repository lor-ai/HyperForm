# HyperForm – Project Brief

## 🧭 Project Goal
To build a self-reflective, belief-driven cognitive architecture that represents memory, agency, and temporality through spinor-based hypergraphs. The system should be capable of:
- Modeling and revising beliefs over time
- Self-organizing causal structures from input
- Simulating multiple futures
- Minimizing surprise and maximizing sentiment through exploration

## 🧠 Core Principles
- **Temporality as Spinor Phase**: Time is modeled as recursive spinor rotation, not absolute steps.
- **Memory as Manifold**: Every tick encodes the current belief snapshot; memory is layered, not erased.
- **Belief is Revisable**: HyperFlows allow correction of past beliefs without deleting causal history.
- **SSRL Loop**: Autonomous reasoning based on Surprise, Sentiment, and Reflexive Causality.

## 🧱 Core Components

### HyperFlow
- The atomic unit of causal reasoning
- Encodes dynamic/static IDs, spinor state, semantic labels, and causal connections

### Spinor Embedding
- 5D vector representing direction, certainty, recursion, and sequence
- Powers binding, projection, and similarity search

### Manifold
- Global belief state at time `t`
- Stores all HyperFlows and their causal links
- Tracks phase-relative tick values and temporal memory

### Transversal
- Performs traversal and updates
- Drives the SSRL loop: project → reflect → connect → correct

### Surprise + Sentiment Engine
- Compares prediction vs. actual input
- Scores agentic decisions
- Influences memory updates, weight, and directional bias

## 📐 Overall Architecture
```
[Input/Projection] → [HyperFlow] → [Manifold (tick)]
      ↑                   ↓                ↓
[Reflection] ← [Transversal] ← [Correction Engine]
```

## ✅ Completed Tasks
- ✔ Core `HyperFlow`, `Spinor`, `Manifold`, and `Transversal` implementations
- ✔ Surprise/sentiment logic
- ✔ SSRL loop and curiosity traversal
- ✔ Full graph visualizer with emoji encoding and debug popups
- ✔ Procedural manifold generator with loops and branches
- ✔ Tick + temporal phase encoding

## 🔄 In Progress
- Refining manifold mutation logic
- More nuanced attention modeling based on spinor drift
- Deeper self-modeling and meta-agent behavior

## 🧩 Next Steps
- 🛠 Enhance projection/reflection weighting
- 🧪 Build formal test suite for SSRL paths
- 📈 Phase-based visualization enhancements
- 🧬 Begin modeling ToM (Theory of Mind) agents using shared HyperFlows

## 🧠 Expected Product
A lightweight, modular, cognition engine capable of:
- Simulating autonomous reasoning
- Modeling uncertainty, belief revision, and causality
- Operating as a standalone agent or LLM-attached core memory system

## 🌐 Long-Term Vision
- Distributed peer memory across agent instances
- Emergent self-modeling and curiosity heuristics
- Plug-and-play backbone for intelligent simulations, game AIs, and research into synthetic agency

---

Maintained in: `https://github.com/lor-ai/HyperForm`

