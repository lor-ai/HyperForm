# HyperForm System Outline (v0.1)

This is the minimal viable self-model for a neuromorphic system. Not a simulation, but the actual structural emergence, the conditions under which it begins to self-maintain.

## 1. CORE OBJECTS

### HyperFlow
- Class represents both hypernode or hyperedge or hyperpath or any or all (context-dependent).
    - Infinitely recursive (russian doll nesting)
- Encodes:
  - Static ID (initial encoding - immutable)
  - Dynamic ID (re-encoded w/ each visit)
  - Metadata (semantic - causal direction, influence, superposition, recursion/sequence)
  - State Vector (LLM embedding, modality-native content)
    - Human Readable (text, hyperlinked)
  - Connections (heads, tails, recursive transform rules)
  - Calculations (mass: weight, gravity, inertia, entropy)
  - Utiliy: can changes with use and context (dynamic function = context-aware reusability.)
    - i.e hyperflow used as path (directions) to actively transverse another (the map) as altered by another (detour)

### Spinor Embedding
- Atomic unit of encoding.
- Replaces traditional vector ops in HRR (binding, bundling/superposition, permute/symmetry)
- Encodes:
  - Causality (direction of cause/effect, influence)
  - Superposition (recursion, nesting)
  - Sequence (past → present → projected)
  - Certainty (magnitude, angular deviation)

### Manifold
- The totality of the hypergraph.
- A spinor-HRR superposition of all entities (sparse updates - visited + transformed)
- Cyclic origin/destination point for all hyperflow paths
    - Hyperflows only exist within context of system (i.e self-modeling)
- Functions:
  - Timeline (cumulative sequential history of system)
    - Recursively re-encodes past state into currect state (tick)
  - Sparse reconstruction key (can restore any state of system)
  - Reference frame for cauality and traversal (prediction, projection, connection, reflection, correction)
  - Store of sujective Metrics (surprise, sentiment)

---

## 2. CORE FUNCTIONS

### Transversal
- Movement via hyperflow as path through the manifold
- Every step of traversal:
  - Unpacks connections in hyperflow region (distance based on mass)
  - Re-encodes visited hyperentities (i.e. breadcrumb logic)
  - Re-encodes manifold with new context (i.e a tick)

### Prediciton / Projection / Reflection / Correction (SSRL Loop)
- Prediction: Possible future hyperflow input (external)
- Projection: Possible or enacted agentic hyperflow output (internal)
- Connection: New hyperflow creation 
- Reflection: Tranvsersal of hyperflows
- Correction: Adjustment of hyperflows

### Surprise + Sentiment Engine
- Calculated via resonance/dissonance (expected vs actual)
    - Surprise = Did actual input match prediction?
    - Sentiment = Did actual output influence inputs?
    - Modifies transversal behaivor (positive attracts, negative repels)
- Drives:
  - Reinforcement Learning
  - Memory update priority
  - Flow adaptation
  - Emergent motivation (qualia, etc)
- 
---

## 3. ARCHITECTURE MODULES

### /core
- `hyperflow.py`: Defines core object schema
- `spinor.py`: Spinor math + embedding ops
- `manifold.py`: Global state container + updater

### /memory
- `transversal.py`: Flow traversal + transformation
- `reflection.py`: Evaluation + recontextualization engine

### /interfaces
- `llm_bridge.py`: Encodes semantic state into spinors
- `graph_ui.py`: Visualization + mermaid / canvas output

---

## 4. NEXT STEPS

1. Finalize `HyperFlow` specs
2. Implement basic `Spinor` operations and VSA/GHRR encoding
3. Mock `Manifold` encoding & update cycle
4. Test traversal / reflection with simple hypergraph

---

## Notes

- All spinor embeddings are compositional.
- The system continually learns by navigating itself.
- High-surprise or high-variance regions are embedded with more fidelity. 
- Frequently traveled paths have more weight (but < neural plasticity)
- Frequenlty used hyperflow collapse into atomic represenations (instinct)
- The graph compresses itself recursively via spinor/hrr  bindings.
- World model = dynamic causal chains in relation to system
- 