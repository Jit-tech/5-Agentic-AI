import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO
import json
import networkx as nx
import numpy as np
import random

# === Load core data ===
counties = [
    "Cork", "Kerry", "Limerick", "Galway", "Dublin", "Clare",
    "Wexford", "Kilkenny", "Donegal", "Mayo", "Meath", "Tipperary"
]

metrics = {
    "County": counties,
    "Soil_Carbon_2024": [2.8, 3.2, 2.5, 3.0, 2.3, 2.9, 3.1, 3.0, 2.6, 2.7, 3.3, 2.4],
    "Nitrogen_Level": [65, 72, 60, 70, 68, 66, 74, 71, 67, 64, 69, 62],
    "Food_Poverty_Index": [0.22, 0.30, 0.25, 0.28, 0.18, 0.26, 0.27, 0.29, 0.33, 0.31, 0.21, 0.24],
    "Farmer_Sentiment_Positive": [0.66, 0.52, 0.60, 0.58, 0.69, 0.61, 0.54, 0.59, 0.50, 0.55, 0.65, 0.57],
    "Text_Comments": [
        "soil health biodiversity water conservation",
        "market disruption rural support",
        "agriculture economy innovation",
        "export block logistics",
        "fertilizer water runoff",
        "carbon sequestration soil regeneration",
        "smart tech robotics farming",
        "subsidy cut farmer income",
        "climate crisis drought",
        "young farmer support",
        "crop rotation sustainability",
        "organic farming trend"
    ]
}
df_geo = pd.DataFrame(metrics)

# === Agent Response Framework ===
def generate_agent_response(agent, context):
    county = context['County']
    soil = context['Soil_Carbon_2024']
    nitrogen = context['Nitrogen_Level']
    poverty = context['Food_Poverty_Index']
    sentiment = context['Farmer_Sentiment_Positive'] + random.uniform(-0.03, 0.03)

    if agent == "GAIA":
        if context['climate_shock']:
            if soil < 2.5:
                return f"GAIA: 'Severe drought + low carbon in {county}. Start emergency regenerative protocols with mulching.'"
            elif soil < 2.8:
                return f"GAIA: '{county} soils marginal post-shock. Deploy localized soil monitoring drones.'"
            else:
                return f"GAIA: '{county} remains stable. Test long-term resilience of biodiversity buffers.'"
        elif nitrogen > 70:
            return f"GAIA: '{county} nitrogen leaching detected. Consider switch to biological N-fixing methods.'"
        elif soil < 2.6:
            return f"GAIA: '{county} needs carbon restoration. Mobilize compost bank initiatives.'"
        else:
            return f"GAIA: '{county} ecosystem resilient. Maintain precision-based no-till systems.'"

    elif agent == "ASTRA":
        if context['export_block']:
            if county in ["Cork", "Wexford"]:
                return f"ASTRA: 'Disruption at {county} hub. Redirect cold chain to Shannon and reevaluate perishable pathways.'"
            else:
                return f"ASTRA: '{county} affected by downstream logistics crunch. Reoptimize through rail-fed buffer zones.'"
        else:
            return f"ASTRA: '{county} exports flowing. Monitor congestion indicators + diesel volatility.'"

    elif agent == "FLORA":
        if context['subsidy_cut']:
            if poverty > 0.3:
                return f"FLORA: 'Food stress surge in {county} due to policy cuts. Launch school meal relief + direct produce linkage.'"
            elif poverty > 0.25:
                return f"FLORA: '{county} at tipping point. Suggest prepaid agro-coop food cards.'"
            else:
                return f"FLORA: '{county} shows soft resilience. Watch dietary diversity metrics closely.'"
        else:
            if poverty > 0.3:
                return f"FLORA: 'Underlying vulnerability in {county}. Activate food bank AI for predictive delivery.'"
            return f"FLORA: '{county} food ecosystem manageable. Align with next gen EIP-Agri projects.'"

    elif agent == "SYLVA":
        if soil >= 3.0:
            return f"SYLVA: '{county} high biocapacity. Fast-track carbon-credit afforestation zones.'"
        elif nitrogen > 70:
            return f"SYLVA: '{county} runoff hotspots. Plant mixed hedgerows + wetland phytoremediation strips.'"
        else:
            return f"SYLVA: '{county} moderate index. Launch smart forest pilot with remote sensing telemetry.'"

    elif agent == "VERA":
        if sentiment < 0.52:
            return f"VERA: 'Low morale in {county}. Host agri-hackathons + participatory innovation summits.'"
        elif sentiment < 0.6:
            return f"VERA: 'Farmer sentiment mixed in {county}. Tailor microlearning + peer-led field labs.'"
        else:
            return f"VERA: 'Positive momentum in {county}. Incentivize early AI-farm adopters with digital twin grants.'"

    return f"{agent}: 'No data-driven recommendation available.'"

# === WordCloud ===
def generate_wordcloud(text):
    wc = WordCloud(width=600, height=300, background_color='white').generate(text)
    buf = BytesIO()
    plt.figure(figsize=(6, 3))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig(buf, format='png')
    st.image(buf)

# === Network Graph ===
def generate_keyword_network(text):
    words = text.lower().split()
    pairs = [(words[i], words[i+1]) for i in range(len(words)-1)]
    G = nx.Graph()
    for a, b in pairs:
        if G.has_edge(a, b):
            G[a][b]['weight'] += 1
        else:
            G.add_edge(a, b, weight=1)
    edge_x, edge_y = [], []
    pos = nx.spring_layout(G)
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=0.5, color='#888'), mode='lines')
    node_x = [pos[node][0] for node in G.nodes()]
    node_y = [pos[node][1] for node in G.nodes()]
    node_trace = go.Scatter(x=node_x, y=node_y, mode='markers+text',
                            marker=dict(size=10, color='lightblue'),
                            text=list(G.nodes()), textposition="top center")
    fig = go.Figure(data=[edge_trace, node_trace],
                   layout=go.Layout(title='Keyword Network', showlegend=False,
                                    margin=dict(b=0,l=0,r=0,t=30)))
    st.plotly_chart(fig, use_container_width=True)
