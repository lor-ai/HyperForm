# manifold_debugger.py

import random
from hyperflow import HyperFlow
from manifold import Manifold

def generate_debug_manifold(seed: int = 42, depth: int = 25, min_branch: int = 1, max_branch: int = 4, loop_chance: float = 0.2) -> Manifold:
    random.seed(seed)
    manifold = Manifold()
    nodes = []

    # Initialize root node
    root = HyperFlow()
    root.encode_state("root", [random.random() for _ in range(5)])
    manifold.add(root)
    nodes.append(root)

    for i in range(depth):
        parent = random.choice(nodes)
        if len(parent.connections.get("tails", [])) == 0 or random.random() < 0.5:
            branch_count = random.randint(min_branch, max_branch)
            for _ in range(branch_count):
                node = HyperFlow()
                node.encode_state(f"node_{i}_{random.randint(0,999)}", [random.random() for _ in range(5)])
                parent.connect(node.static_id, direction="tail")
                manifold.add(node)
                nodes.append(node)

        # Randomly loop to earlier node
        if random.random() < loop_chance and len(nodes) > 2:
            target = random.choice(nodes[:-2])
            parent.connect(target.static_id, direction="tail")

    return manifold
