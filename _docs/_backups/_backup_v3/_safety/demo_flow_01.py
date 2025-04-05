# demo_flow.py

from hyperflow import HyperFlow, Spinor
from manifold import Manifold
from transversal import Transversal

from transversal import Transversal
from hyperflow import Spinor
from manifold_visualizer import ManifoldVisualizer


# Initialize system
origin_spinor = Spinor([1.0, 0.5, 0.0, 0.0, 0.0])
manifold = Manifold()
transversal = Transversal(manifold)

# Create initial hyperflows
node_a = HyperFlow()
node_b = HyperFlow()
node_c = HyperFlow()

# Encode basic state
node_a.encode_state("start", [0.1, 0.2, 0.3, 0.4, 0.5])
node_b.encode_state("middle", [0.3, 0.1, 0.4, 0.1, 0.2])
node_c.encode_state("end", [0.5, 0.5, 0.5, 0.5, 0.5])

# Add to manifold
manifold.add(node_a)
manifold.add(node_b)
manifold.add(node_c)

# Link flows
node_a.connect(node_b.static_id, direction="tail")
node_b.connect(node_c.static_id, direction="tail")

# Walk the path
print("Before traversal:")
print(node_a)
print(node_b)
print(node_c)

print("\nTraversing via Transversal...")
visited = transversal.walk_path([node_a.static_id, node_b.static_id, node_c.static_id], origin_spinor)

print("\nAfter traversal:")
for node in visited:
    print(node)

# Reflection: compare last node to all others
print("\nReflection result:")
for flow_id, score in transversal.reflect(visited[-1]):
    print(f"{flow_id[:8]}... -> similarity: {score:.4f}")

# Summarize manifold
print("\nManifold Summary:")
print(manifold.summarize())