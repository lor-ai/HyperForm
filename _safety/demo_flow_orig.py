# demo_flow_orig.py

from hyperflow import HyperFlow, Spinor
from manifold import Manifold
from transversal import Transversal
from manifold_visualizer import ManifoldVisualizer
from manifold_debugger import generate_debug_manifold

manifold = generate_debug_manifold(seed=1337, depth=30)
transversal = Transversal(manifold)


# Initialize manifold and transversal system
manifold = Manifold()
transversal = Transversal(manifold)
origin_spinor = Spinor([0.5, 0.5, 0.5, 0.5, 0.5])

# Create sample HyperFlows
node_a = HyperFlow()
node_b = HyperFlow()
node_c = HyperFlow()

node_a.encode_state("start", [0.1, 0.2, 0.3, 0.4, 0.5])
node_b.encode_state("middle", [0.3, 0.1, 0.4, 0.1, 0.2])
node_c.encode_state("end", [0.5, 0.5, 0.5, 0.5, 0.5])

# Link and register nodes
node_a.connect(node_b.static_id, direction="tail")
node_b.connect(node_c.static_id, direction="tail")

for node in [node_a, node_b, node_c]:
    manifold.add(node)

# Run SSRL loop
transversal.ssrl_loop(start_id=node_a.static_id, steps=5)

# Visualize results
viz = ManifoldVisualizer(manifold)
viz.draw()
