# demo_flow.py

from hyperflow import HyperFlow, Spinor

# Initialize seed context spinor
origin_spinor = Spinor([1.0, 0.5, 0.0, 0.0, 0.0])

# Create initial hyperflows
node_a = HyperFlow()
node_b = HyperFlow()
node_c = HyperFlow()

# Encode some basic state
node_a.encode_state("start", [0.1, 0.2, 0.3, 0.4, 0.5])
node_b.encode_state("middle", [0.3, 0.1, 0.4, 0.1, 0.2])
node_c.encode_state("end", [0.5, 0.5, 0.5, 0.5, 0.5])

# Link nodes
node_a.connect(node_b.static_id, direction="tail")
node_b.connect(node_c.static_id, direction="tail")

# Simulate traversal through the graph
print("Before traversal:")
print(node_a)
print(node_b)
print(node_c)

print("\nTraversing...")

node_a.visit(origin_spinor)
node_b.visit(node_a.spinor_embedding)
node_c.visit(node_b.spinor_embedding)

print("\nAfter traversal:")
print(node_a)
print(node_b)
print(node_c)

# Show spinor similarity between A and C
similarity = node_a.spinor_embedding.similarity(node_c.spinor_embedding)
print(f"\nSimilarity between node A and node C: {similarity:.4f}")