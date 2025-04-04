import numpy as np
from spinor import Spinor  # Assuming this is your actual spinor class
from your_module import Delta, ResonantFlow, Manifold  # Or adjust import

# Step 1: Initialize Δ
init_spinor = Spinor(np.random.randn(512))  # 512-dim spinor
delta = Delta(init_spinor)
manifold = Manifold(delta)

# Step 2: Simulate a few flows
for _ in range(10):
    random_spinor = Spinor(np.random.randn(512))
    flow = ResonantFlow(random_spinor)
    manifold.tick(flow)

# Step 3: Rebase resonance
manifold.resonate()

# Output results
print("Delta mass:", delta.mass)
print("Delta origin (truncated):", delta.origin.vector[:5])
print("First flow sentiment:", manifold.flows[0].sentiment)
print("Last flow surprise:", manifold.flows[-1].surprise)
