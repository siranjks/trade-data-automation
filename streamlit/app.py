import streamlit as st
import pandas as pd
import plotly.express as px
import sqlite3
import os

# Page config
st.set_page_config(page_title="Trade Data Command Center", layout="wide")

# 1. DYNAMIC DATABASE CONNECTION (Updated with Smart Logic)
@st.cache_data(ttl=600)  # Caches data for 10 minutes so it's lightning fast
def load_real_data():
    # Define the two possible locations
    local_path = r"C:\TRADE_DATA\Local-Execution\DATABASES\Trade_Data.db"
    cloud_path = "Trade_Data.db"
    
    # Smart Connection Logic
    if os.path.exists(local_path):
        conn = sqlite3.connect(local_path)
        # We don't print st.success here because it would cache and act weird, 
        # but rest assured, if it hits this, you are on the local C: drive!
    elif os.path.exists(cloud_path):
        conn = sqlite3.connect(cloud_path)
    else:
        st.error("❌ Database file not found in local OR cloud paths. Please check your KNIME export.")
        return pd.DataFrame() # Return empty dataframe to prevent crash
        
    # SQL Query to pull your cleaned master data
    query = "SELECT * FROM trade_data" 
    
    try:
        df = pd.read_sql_query(query, conn)
    except Exception as e:
        st.error(f"❌ Error reading table: {e}. Check if your table name is correct.")
        # If it fails, print out the actual table names to help you debug!
        df_tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
        st.info(f"Available tables in your DB: {df_tables['name'].tolist()}")
        df = pd.DataFrame()
    finally:
        conn.close() # Always hang up the phone!
        
    return df

# Load the real data
df = load_real_data()

# Check if data loaded successfully before rendering the page
if not df.empty:
    # 2. SIDEBAR FILTERS
    st.sidebar.title("Navigation & Filters")
    
    # Dynamically grab the first text column for the filter (usually Country or Importer)
    filter_column = 'Country' if 'Country' in df.columns else df.columns[0] 
    
    unique_values = ["All"] + sorted(list(df[filter_column].dropna().unique()))
    selected_filter = st.sidebar.selectbox(f"Select {filter_column}", unique_values)

    # 3. MAIN UI
    st.title(" 📊 Global Trade Command Center")
    st.markdown("Direct pipeline from automated SQLite database.")

    tab1, tab2, tab3 = st.tabs(["🗄️ Master Database View", "📈 Visual Analytics", "🤖 AI Assistant"])

    with tab1:
        st.header("Real-Time Data Rows")
        
        # Filter logic
        display_df = df if selected_filter == "All" else df[df[filter_column] == selected_filter]
        
        # Display the real data
        st.dataframe(display_df, use_container_width=True)
        
        # Live CSV Downloader for your supervisor
        csv = display_df.to_csv(index=False).encode('utf-8')
        st.download_button(label="📥 Download Filtered Data as CSV", data=csv, file_name='trade_data_export.csv', mime='text/csv')

    with tab2:
        st.header("Interactive Analytics")
        
        # Dynamic Chart Generation
        fig = px.histogram(df, x=filter_column, title=f"Data Distribution by {filter_column}")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.header("🤖 Chat with your Data")
        st.info("Database connected successfully! Next step: Wiring up the AI API Key.")
        st.chat_input("Ask a question about the database...")