import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import os

# Page config
st.set_page_config(page_title="Trade Data Command Center", layout="wide")

# 1. DYNAMIC DATABASE CONNECTION
@st.cache_data(ttl=600)  # Caches data for 10 minutes so it's lightning fast
def load_real_data():
    # Looks for Trade_Data.db one folder up from the streamlit folder
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "Trade_Data.db"))
    
    # Fallback if the file isn't found right away
    if not os.path.exists(db_path):
        # Try local folder absolute path just in case
        db_path = r"C:\TRADE_DATA\Local-Execution\DATABASES\Trade_Data.db"
        
    if not os.path.exists(db_path):
        st.error(f"❌ Database file not found at: {db_path}. Please check your KNIME export path.")
        return pd.DataFrame() # Return empty dataframe to prevent crash
        
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    
    # SQL Query to pull your cleaned master data (adjust table name if needed!)
    query = "SELECT * FROM trade_data" 
    
    try:
        df = pd.read_sql_query(query, conn)
    except Exception as e:
        st.error(f"❌ Error reading table: {e}. Check if your table name is correct.")
        df = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
        st.info(f"Available tables in your DB: {df['name'].tolist()}")
        df = pd.DataFrame()
    finally:
        conn.close()
        
    return df

# Load the real data
df = load_real_data()

# Check if data loaded successfully before rendering the page
if not df.empty:
    # 2. SIDEBAR FILTERS (Dynamically generated from your real data!)
    st.sidebar.title("Navigation & Filters")
    
    # Let's assume you have a 'Country' column. If it's named differently, change it here!
    country_column = 'Country' if 'Country' in df.columns else df.columns[0] 
    
    unique_countries = ["All"] + sorted(list(df[country_column].dropna().unique()))
    country_filter = st.sidebar.selectbox("Select Country", unique_countries)

    # 3. MAIN UI
    st.title(" 📊 Global Trade Command Center")
    st.markdown("Direct pipeline from local automated SQLite database.")

    tab1, tab2, tab3 = st.tabs(["🗄️ Master Database View", "📈 Visual Analytics", "🤖 AI Assistant"])

    with tab1:
        st.header("Real-Time Data Rows")
        
        # Filter logic
        display_df = df if country_filter == "All" else df[df[country_column] == country_filter]
        
        # Display the real data
        st.dataframe(display_df, use_container_width=True)
        
        # Live CSV Downloader for your supervisor
        csv = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Download Filtered Data as CSV", data=csv, file_name='trade_data_export.csv', mime='text/csv')

    with tab2:
        st.header("Interactive Analytics")
        
        # Dynamic Chart Generation based on available columns
        # Let's see if we have volume/weight columns, otherwise use row counts
        volume_col = 'Export Volume' if 'Export Volume' in df.columns else (df.columns[1] if len(df.columns) > 1 else df.columns[0])
        
        fig = px.histogram(df, x=country_column, title="Data Distribution by Country")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.header("🤖 Chat with your Data")
        st.info("Database connected successfully! Next step: Wiring up the AI API Key.")
        st.chat_input("Ask a question about the database...")