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
    "Farmer_Sentiment_Positive": [0.66, 0.52, 0.60, 0.58, 0.69, 0.61, 0.54, 0.59, 0.50, 0.55, 0.65, 0.57]
}
df_geo = pd.DataFrame(metrics)

# === Agent response logic ===
def gaia(c, climate_shock):
    if climate_shock and c['Soil_Carbon_2024'] < 2.8:
        return f"GAIA: 'Post-shock soil in {c['County']} requires regenerative tillage immediately.'"
    if c['Soil_Carbon_2024'] < 2.6:
        return f"GAIA: 'Soil carbon low in {c['County']}. Cover cropping now critical.'"
    elif c['Nitrogen_Level'] > 70:
        return f"GAIA: 'Nitrogen overload in {c['County']}. Shift to legumes needed.'"
    return f"GAIA: '{c['County']} shows balance. Sustain biodiversity with precision farming.'"

def astra(c, export_block):
    if export_block and c['County'] in ["Cork", "Wexford"]:
        return f"ASTRA: 'Export choke-point in {c['County']}! Reroute or buffer stocks needed.'"
    return f"ASTRA: '{c['County']} logistics are stable. Watch volatility indices quarterly.'"

def flora(c, subsidy_cut):
    if subsidy_cut and c['Food_Poverty_Index'] > 0.28:
        return f"FLORA: 'Food poverty alert in {c['County']}. Deploy emergency nutrition credits!'"
    elif c['Food_Poverty_Index'] > 0.3:
        return f"FLORA: 'Persistent poverty in {c['County']}. CAP buffer recommended.'"
    return f"FLORA: '{c['County']} food security fair. Monitor staple inflation.'"

def sylva(c):
    return f"SYLVA: '{c['County']} can lead in biomass + forestry. Recommend pilot circular cluster.'"

def vera(c):
    if c['Farmer_Sentiment_Positive'] < 0.55:
        return f"VERA: 'Morale dip in {c['County']}. Co-create next CAP block grants!'"
    return f"VERA: '{c['County']} sentiment holding. Prioritize training in tech-bio practices.'"

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

# === Bar Chart ===
def generate_keyword_barchart(text, deviation=0):
    base_words = text.lower().split()
    word_freq = {w: base_words.count(w) + deviation for w in set(base_words)}
    sorted_items = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:10]
    words, freqs = zip(*sorted_items)
    fig = go.Figure(go.Bar(x=freqs, y=words, orientation='h', marker=dict(color='green')))
    fig.update_layout(title="Top Keywords", yaxis_title="Keyword", xaxis_title="Adjusted Frequency")
    st.plotly_chart(fig, use_container_width=True)

# === Simulated Sentiment Trend ===
def generate_sentiment_trend(county, policy_effect):
    dates = pd.date_range(start='2023-01', periods=6, freq='Q')
    base = 0.60 + np.random.normal(0, 0.01, 6)
    impact = -0.04 if policy_effect else 0.02
    adjusted = base + impact
    fig = px.line(x=dates, y=adjusted, labels={'x': 'Quarter', 'y': 'Sentiment'},
                  title=f"Sentiment Trend for {county} under Current Scenario")
    st.plotly_chart(fig, use_container_width=True)

# === Streamlit App ===
st.set_page_config(page_title="Agri AI Agents", layout="wide")
st.title("🇮🇪 Ireland's Agri-Food System – Multi-Agent AI Prototype")

st.sidebar.header("⚙️ Policy Scenario Controls")
climate_shock = st.sidebar.checkbox("Simulate Climate Shock (Drought)")
export_block = st.sidebar.checkbox("Simulate Export Disruption")
subsidy_cut = st.sidebar.checkbox("Simulate CAP Subsidy Cut")

st.markdown("### 🗺️ Nitrogen Levels by County")
with open("assets/ireland_counties.geojson") as f:
    counties_geo = json.load(f)

fig = px.choropleth_mapbox(
    df_geo,
    geojson=counties_geo,
    locations='County',
    featureidkey='properties.CountyName',
    color='Nitrogen_Level',
    color_continuous_scale="RdYlGn_r",
    mapbox_style="carto-positron",
    zoom=5.5,
    center={"lat": 53.4, "lon": -7.9},
    opacity=0.6,
    hover_name='County')
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
st.plotly_chart(fig, use_container_width=True)

county = st.selectbox("Select County to Consult AIs:", df_geo['County'])
row = df_geo[df_geo['County'] == county].iloc[0]

st.markdown("### Agent Responses")
st.info(gaia(row, climate_shock))
st.success(astra(row, export_block))
st.warning(flora(row, subsidy_cut))
st.info(sylva(row))
st.success(vera(row))

# === NLP Analysis ===
st.markdown(f"### Farmer Feedback Analysis: {county}")
mock_text = f"soil subsidy cap export sentiment policy support {county.lower()} {county.lower()} agtech climate beef dairy training funding"

deviation = -1 if subsidy_cut else 1
policy_effect = climate_shock or subsidy_cut or export_block

st.subheader("Keyword Frequency (Bar Chart)")
generate_keyword_barchart(mock_text, deviation)

st.subheader("Sentiment Trend (Simulated)")
generate_sentiment_trend(county, policy_effect)

st.subheader("Keyword Network")
generate_keyword_network(mock_text)

st.subheader("WordCloud")
generate_wordcloud(mock_text)

st.caption("Jit’s Prototype – Strategic, Data-Driven, and Slightly Funny. Powered by Streamlit + Plotly + WordCloud + NLP Intelligence.")
