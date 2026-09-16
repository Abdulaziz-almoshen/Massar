"""LangGraph state graph definition.

    START → classify_intent ─ opt_out intent → END (handler opts out in code)
          → route_to_tool → check_escalation
          ─┬─ escalate (trigger or HOT) → escalate_to_human ─┐
           ├─ WARM → nurture ───────────────────────────────┤→ generate_response → END
           └─ COLD → self_service ──────────────────────────┘
"""

from __future__ import annotations

from langgraph.graph import END, START, StateGraph

from agent.nodes import Deps, make_nodes
from agent.state import ConversationState


def build_graph(deps: Deps, checkpointer=None):
    n = make_nodes(deps)
    g = StateGraph(ConversationState)
    for name in ("classify_intent", "route_to_tool", "check_escalation", "escalate_to_human", "nurture", "self_service", "generate_response"):
        g.add_node(name, n[name])
    g.add_edge(START, "classify_intent")
    g.add_conditional_edges("classify_intent", n["route_after_opt_out_check"], {"opt_out": END, "continue": "route_to_tool"})
    g.add_edge("route_to_tool", "check_escalation")
    g.add_conditional_edges(
        "check_escalation",
        n["route_after_check"],
        {"escalate": "escalate_to_human", "nurture": "nurture", "self_service": "self_service"},
    )
    for name in ("escalate_to_human", "nurture", "self_service"):
        g.add_edge(name, "generate_response")
    g.add_edge("generate_response", END)
    return g.compile(checkpointer=checkpointer)
