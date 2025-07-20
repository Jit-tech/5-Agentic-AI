import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO

# === Load mock data ===
counties = [
    "Cork", "Kerry", "Limerick", "Galway", "Dublin", "Clare",
    "Wexford", "Kilkenny", "Donegal", "Mayo", "Meath", "Tipperary"
]

geo_data = {
    "County": counties,
    "Latitude": [51.9, 52.1, 52.7, 53.3, 53.3, 52.8, 52.3, 52.6, 55.0, 53.9, 53.6, 52.5],
    "Longitude": [-8.5, -9.7, -8.6, -9.0, -6.3, -9.0, -6.5, -7.3, -7.7, -9.3, -6.5, -7.8]
}
df_geo = pd.DataFrame(geo_data)

metrics = {
    "Soil_Carbon_2024": [2.8, 3.2, 2.5, 3.0, 2.3, 2.9, 3.1, 3.0, 2.6, 2.7, 3.3, 2.4],
    "Nitrogen_Level": [65, 72, 60, 70, 68, 66, 74, 71, 67, 64, 69, 62],
    "Food_Poverty_Index": [0.22, 0.30, 0.25, 0.28, 0.18, 0.26, 0.27, 0.29, 0.33, 0.31, 0.21, 0.24],
    "Farmer_Sentiment_Positive": [0.66, 0.52, 0.60, 0.58, 0.69, 0.61, 0.54, 0.59, 0.50, 0.55, 0.65, 0.57]
}
for key, values in metrics.items():
    df_geo[key] = values

# === Agent response logic ===
def gaia(c):
    if c['Soil_Carbon_2024'] < 2.6:
        return f"🧠 GAIA: 'Soil carbon low in {c['County']}. Urgent need for cover cropping.'"
    elif c['Nitrogen_Level'] > 70:
        return f"🧠 GAIA: 'Nitrogen overload in {c['County']}. Shift to leguminous rotation advised.'"
    return f"🧠 GAIA: '{c['County']} is balanced. Maintain eco-stability through smart practices.'"

def astra(c):
    return f"📦 ASTRA: '{c['County']} logistics flow stable. Monitor seasonal bottlenecks.'"

def flora(c):
    if c['Food_Poverty_Index'] > 0.3:
        return f"🥗 FLORA: 'Food poverty high in {c['County']}. Activate safety net subsidies.'"
    return f"🥗 FLORA: '{c['County']} food affordability acceptable. Watch CPI next quarter.'"

def sylva(c):
    return f"🌳 SYLVA: '{c['County']} land is viable for bioeconomy. Prioritize circular transitions.'"

def vera(c):
    if c['Farmer_Sentiment_Positive'] < 0.55:
        return f"🧑‍🌾 VERA: 'Farmer morale low in {c['County']}. Propose co-creation forums.'"
    return f"🧑‍🌾 VERA: 'Sentiment in {c['County']} improving. Reward engagement in policy cycles.'"

# === NLP WordCloud Mock ===
def generate_wordcloud(text):
    wc = WordCloud(width=600, height=300, background_color='white').generate(text)
    buf = BytesIO()
    plt.figure(figsize=(6, 3))
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig(buf, format='png')
    st.image(buf)

# === Streamlit UI ===
st.set_page_config(page_title="Agri AI Agents", layout="wide")
st.title("🇮🇪 Ireland's Agri-Food System – Multi-Agent AI Prototype")

# Metric Map
st.markdown("### 🗺️ County-wise Nitrogen Levels")
fig = px.scatter_geo(
    df_geo,
    lat='Latitude',
    lon='Longitude',
    text='County',
    color='Nitrogen_Level',
    color_continuous_scale='RdYlGn_r',
    projection="natural earth",
    size_max=15,
    size=[10]*len(df_geo),
    title="Nitrogen Intensity by County"
)
fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(
    paper_bgcolor='white',
    plot_bgcolor='white',
    geo=dict(
        bgcolor='white',
        showland=True,
        landcolor='rgb(229, 236, 246)'
    )
)
fig.update_traces(
    textfont=dict(color='black', size=12),
    marker=dict(line=dict(width=1, color='black'))
)
st.plotly_chart(fig, use_container_width=True)

# Select County for NLP + Agent Response
county = st.selectbox("🔍 Select County to Consult AIs:", df_geo['County'])
row = df_geo[df_geo['County'] == county].iloc[0]

# Agent Responses
st.markdown("### 🤖 Agent Responses")
st.info(gaia(row))
st.success(astra(row))
st.warning(flora(row))
st.info(sylva(row))
st.success(vera(row))

# NLP Mock Output
st.markdown("### 🧠 VERA’s WordCloud: Farmer Opinions in " + county)
mock_text = f"farming subsidy soil prices policy {county.lower()} {county.lower()} dairy milk export beef EU CAP support drought weed AI sensors"
generate_wordcloud(mock_text)

st.caption("Jit’s Prototype – Strategic + Humorous + Insightful. Powered by Streamlit, Plotly, WordCloud")
