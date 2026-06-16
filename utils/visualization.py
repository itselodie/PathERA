"""Plotly + NetworkX visualizations for decision trees and tradeoffs."""

from __future__ import annotations

from typing import Any

import networkx as nx
import plotly.graph_objects as go


def build_decision_tree_figure(decision_tree: dict[str, Any]) -> go.Figure:
    """Render an interactive decision tree from mapper output."""
    G = nx.DiGraph()
    G.add_node("root", label=decision_tree.get("root_question", "Your decision"))

    for opt in decision_tree.get("options", []):
        G.add_node(opt["id"], label=opt["label"])
        for sub in opt.get("sub_options", []):
            G.add_node(sub["id"], label=sub["label"])

    for edge in decision_tree.get("tree_edges", []):
        G.add_edge(edge["from"], edge["to"], label=edge.get("label", ""))

    if G.number_of_nodes() <= 1:
        return go.Figure().update_layout(title="No decision tree data")

    pos = nx.spring_layout(G, seed=42, k=1.8)

    edge_x, edge_y, edge_text = [], [], []
    for u, v, data in G.edges(data=True):
        x0, y0 = pos[u]
        x1, y1 = pos[v]
        edge_x.extend([x0, x1, None])
        edge_y.extend([y0, y1, None])
        edge_text.append(data.get("label", ""))

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        mode="lines",
        line=dict(width=2, color="#94a3b8"),
        hoverinfo="none",
        showlegend=False,
    )

    node_x, node_y, node_text, node_color = [], [], [], []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        label = G.nodes[node].get("label", node)
        node_text.append(f"<b>{label}</b><br><span style='font-size:10px'>{node}</span>")
        node_color.append("#6366f1" if node == "root" else "#22d3ee")

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode="markers+text",
        text=[G.nodes[n].get("label", n)[:20] for n in G.nodes()],
        textposition="top center",
        hovertext=node_text,
        hoverinfo="text",
        marker=dict(size=28, color=node_color, line=dict(width=2, color="#1e293b")),
        showlegend=False,
    )

    fig = go.Figure(data=[edge_trace, node_trace])
    fig.update_layout(
        title="Decision Tree Map",
        showlegend=False,
        hovermode="closest",
        margin=dict(b=20, l=20, r=20, t=50),
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=420,
    )
    return fig


def build_tradeoff_radar(tradeoffs: dict[str, Any]) -> go.Figure:
    """Radar chart comparing option alignment scores."""
    items = tradeoffs.get("tradeoffs", [])
    if not items:
        return go.Figure().update_layout(title="No tradeoff data")

    labels = [t["option_label"][:18] for t in items]
    scores = [t.get("alignment_score", 50) for t in items]

    fig = go.Figure(
        data=go.Scatterpolar(
            r=scores + [scores[0]],
            theta=labels + [labels[0]],
            fill="toself",
            fillcolor="rgba(99, 102, 241, 0.25)",
            line=dict(color="#6366f1", width=2),
            name="Alignment",
        )
    )
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        title="Option Alignment Scores",
        height=380,
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def build_risk_benefit_bar(tradeoffs: dict[str, Any]) -> go.Figure:
    """Grouped bar chart of benefit vs risk counts per option."""
    items = tradeoffs.get("tradeoffs", [])
    if not items:
        return go.Figure()

    labels = [t["option_label"][:16] for t in items]
    benefits = [len(t.get("benefits", [])) for t in items]
    risks = [len(t.get("risks", [])) for t in items]

    fig = go.Figure(
        data=[
            go.Bar(name="Benefits", x=labels, y=benefits, marker_color="#22c55e"),
            go.Bar(name="Risks", x=labels, y=risks, marker_color="#f97316"),
        ]
    )
    fig.update_layout(
        barmode="group",
        title="Benefits vs Risks per Option",
        height=320,
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig
