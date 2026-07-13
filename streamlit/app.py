import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(page_title="Trade Data Command Center", layout="wide")

# Mock Data (We will swap this out for your SQLite DB later)
@st.cache_data
def load_data():
    return pd.DataFrame({
        "Country": ["Vietnam", "USA", "Germany", "Japan", "Brazil"],
        "Export Volume": [700, 15000, 8500, 12000, 4200],
        "Top Category": ["Electronics", "Machinery", "Vehicles", "Robotics", "Agriculture"]
    })

df = load_data()

# Sidebar
st.sidebar.title("Navigation")
country_filter = st.sidebar.selectbox("Select a Country", ["All"] + list(df["Country"]))

# Main UI
st.title("📊 Global Trade Command Center")

tab1, tab2, tab3 = st.tabs(["Raw Data & Exports", "Visual Analytics", "AI Assistant"])

with tab1:
    st.header("🗄️ Database View")
    display_df = df if country_filter == "All" else df[df["Country"] == country_filter]
    st.dataframe(display_df, use_container_width=True)
    
    csv = display_df.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Download CSV", data=csv, file_name='trade_data.csv', mime='text/csv')

with tab2:
    st.header("📈 Visual Analytics")
    fig = px.bar(df, x="Country", y="Export Volume", color="Top Category", title="Total Volume")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.header("🤖 Chat with your Data")
    st.info("AI Chat interface placeholder.")
    st.chat_input("Ask a question...")