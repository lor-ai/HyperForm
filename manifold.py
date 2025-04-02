# manifold.py

from typing import Dict, List
from hyperflow import HyperFlow, Spinor
import uuid

class Manifold:
    def __init__(self):
        self.state: Dict[str, HyperFlow] = {}
        self.timeline: List[str] = []
        self.id = str(uuid.uuid4())

    def add(self, flow: HyperFlow):
        self.state[flow.static_id] = flow

    def tick(self, flow: HyperFlow):
        flow_id = flow.static_id
        self.timeline.append(flow_id)
        self.state[flow_id] = flow  # Re-encode

    def get_flow(self, flow_id: str) -> HyperFlow:
        return self.state.get(flow_id)

    def summarize(self):
        return {
            "total_flows": len(self.state),
            "ticks": len(self.timeline),
            "last": self.timeline[-1] if self.timeline else None
        }

    def __repr__(self):
        return f"<Manifold flows:{len(self.state)} ticks:{len(self.timeline)} id:{self.id[:8]}>"