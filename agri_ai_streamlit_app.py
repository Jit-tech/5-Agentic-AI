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
from collections import Counter

# === UI Configuration ===
st.set_page_config(page_title="Agri-Food Agentic AI Council", layout="wide")
st.title("Agentic AI for Agri-Food Sustainability: Ireland’s Strategic Simulator")
st.markdown("<h6 style='text-align: center;'>Designed by Jit</h6>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center;'>Powered by Econometrics and AI</h6>", unsafe_allow_html=True)

# === Sidebar: Scenario & County Selection ===
st.sidebar.header("Scenario Options & County Selector")
selected_county = st.sidebar.selectbox("Select County:", [
    "Cork", "Kerry", "Limerick", "Galway", "Dublin", "Clare",
    "Wexford", "Kilkenny", "Donegal", "Mayo", "Meath", "Tipperary"
])
climate_shock = st.sidebar.checkbox("Climate Shock")
export_block  = st.sidebar.checkbox("Export Block")
subsidy_cut   = st.sidebar.checkbox("Subsidy Cut")

# === Load Data ===
counties = ["Cork","Kerry","Limerick","Galway","Dublin","Clare",
            "Wexford","Kilkenny","Donegal","Mayo","Meath","Tipperary"]
metrics = {
    "County": counties,
    "Soil_Carbon_2024": [2.8,3.2,2.5,3.0,2.3,2.9,3.1,3.0,2.6,2.7,3.3,2.4],
    "Nitrogen_Level":   [65,72,60,70,68,66,74,71,67,64,69,62],
    "Food_Poverty_Index":[0.22,0.30,0.25,0.28,0.18,0.26,0.27,0.29,0.33,0.31,0.21,0.24],
    "Farmer_Sentiment_Positive":[0.66,0.52,0.60,0.58,0.69,0.61,0.54,0.59,0.50,0.55,0.65,0.57],
    "Text_Comments":[
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
df = pd.DataFrame(metrics)

# === Scenario Context ===
ctx = df[df['County']==selected_county].iloc[0].to_dict()
ctx.update({
    'climate_shock': climate_shock,
    'export_block': export_block,
    'subsidy_cut': subsidy_cut
})

# === Agent Response Logic ===
def generate_agent_response(agent, c):
    soil = c['Soil_Carbon_2024']; nit = c['Nitrogen_Level']; pov = c['Food_Poverty_Index']
    sent = c['Farmer_Sentiment_Positive'] + random.uniform(-0.03,0.03)
    county = c['County']
    if agent=='GAIA':
        if c['climate_shock']:
            return (f"GAIA: '{county}' soils hit by drought. "
                    + ("Severe: emergency regreening." if soil<2.5 else "Moderate: deploy soil drones."))
        if nit>70: return f"GAIA: '{county}' nitrogen leaching. Apply N-fixing cover crops.'"
        if soil<2.6: return f"GAIA: '{county}' low soil C. Mobilize compost banks.'"
        return f"GAIA: '{county}' eco-stable. Maintain no-till practices.'"
    if agent=='ASTRA':
        if c['export_block']:
            return (f"ASTRA: '{county}' export hub disrupted. "
                    + ("Re-route perishables via Shannon." if county in ['Cork','Wexford'] else "Scale rail buffer zones."))
        return f"ASTRA: '{county}' exports nominal. Monitor customs & fuel costs.'"
    if agent=='FLORA':
        if c['subsidy_cut']:
            return (f"FLORA: '{county}' food stress up. "
                    + ("Launch meal relief + vouchers." if pov>0.3 else "Enable CSA partnerships."))
        if pov>0.3: return f"FLORA: '{county}' vulnerability high. Activate predictive food banks.'"
        return f"FLORA: '{county}' nutrition adequate. Align with EIP-Agri pilots.'"
    if agent=='SYLVA':
        if soil>=3.0: return f"SYLVA: '{county}' prime for agroforestry carbon credits.'"
        if nit>70: return f"SYLVA: '{county}' runoff risk. Install riparian buffers.'"
        return f"SYLVA: '{county}' moderate. Pilot mixed-stand forestry.'"
    if agent=='VERA':
        if sent<0.52: return f"VERA: '{county}' morale low. Host innovation summits.'"
        if sent<0.60: return f"VERA: '{county}' mixed sentiment. Deploy peer-led labs.'"
        return f"VERA: '{county}' sentiment strong. Incentivize AI farming grants.'"
    return f"{agent}: No recommendation."

# === Visualization Helpers ===
def generate_wordcloud(text):
    wc=WordCloud(width=600,height=300,background_color='white').generate(text)
    buf=BytesIO(); plt.figure(figsize=(6,3)); plt.imshow(wc,interpolation='bilinear'); plt.axis('off');
    plt.tight_layout(pad=0); plt.savefig(buf,format='png'); st.image(buf)

def generate_keyword_network(text):
    words=text.split(); G=nx.Graph()
    for a,b in zip(words,words[1:]): G.add_edge(a,b,weight=G[a][b]['weight']+1 if G.has_edge(a,b) else 1)
    pos=nx.spring_layout(G)
    edge_x,edge_y=[],[]
    for u,v in G.edges(): x0,y0=pos[u]; x1,y1=pos[v]; edge_x+=[x0,x1,None]; edge_y+=[y0,y1,None]
    edge_trace=go.Scatter(x=edge_x,y=edge_y,mode='lines',line=dict(width=0.5,color='#888'))
    node_x=[pos[n][0] for n in G]; node_y=[pos[n][1] for n in G]
    node_trace=go.Scatter(x=node_x,y=node_y,mode='markers+text',text=list(G.nodes()),textposition='top center',marker=dict(size=10,color='lightblue'))
    fig=go.Figure(data=[edge_trace,node_trace],layout=go.Layout(title='Keyword Network',margin=dict(b=0,l=0,r=0,t=30),showlegend=False))
    st.plotly_chart(fig,use_container_width=True)

def show_most_used_words(text):
    freqs=Counter(text.split()).most_common(10)
    dfw=pd.DataFrame(freqs,columns=['Word','Frequency'])
    fig=px.bar(dfw,x='Word',y='Frequency',title='Top Used Words'); st.plotly_chart(fig,use_container_width=True)

def generate_sentiment_trend(text,effect):
    dates=pd.date_range('2023-01',periods=6,freq='Q')
    base=np.linspace(0.55,0.65,6)+np.random.normal(0,0.01,6)
    adj=base+(-0.05 if effect else 0.03)
    fig=px.line(x=dates,y=adj,labels={'x':'Quarter','y':'Sentiment'},title='Simulated Sentiment Trend'); st.plotly_chart(fig,use_container_width=True)

# === Choropleth Map ===
st.markdown("### Nitrogen Levels by County")
with open("assets/ireland_counties.geojson") as f: gj=json.load(f)
fig=px.choropleth_mapbox(df,geojson=gj,locations='County',featureidkey='properties.CountyName',
    color='Nitrogen_Level',color_continuous_scale='RdYlGn_r',mapbox_style='carto-positron',zoom=5.5,
    center={'lat':53.4,'lon':-7.9},opacity=0.6,hover_name='County')
fig.update_layout(margin={'r':0,'t':0,'l':0,'b':0}); st.plotly_chart(fig,use_container_width=True)

# === Agent Responses ===
st.subheader(f"Agentic Insights for {selected_county}")
for agent in ['GAIA','ASTRA','FLORA','SYLVA','VERA']:
    st.markdown(f"**{generate_agent_response(agent,ctx)}**")

# === NLP Analysis ===
comments=ctx['Text_Comments']
st.subheader("Farmer Feedback Analysis")
show_most_used_words(comments)
## Sentiment Trend
generate_sentiment_trend(comments,climate_shock or subsidy_cut or export_block)
## Network Graph
generate_keyword_network(comments)
## WordCloud
generate_wordcloud(comments)
st.caption("© Jit | Powered by Econometrics & AI")
