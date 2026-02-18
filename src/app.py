import streamlit as st

# Page settings
st.set_page_config(page_title="IT: Streamlit Showcase", layout="wide")


# Method to prevent recursive imports when using the navigation system
def show_home():
    st.title("Welcome to the Streamlit Showcase App!")
    st.markdown("""
    This app demonstrates how to use Streamlit for building interactive ML/AI web applications without any pain 
    (i.e. without needing to use CSS/JavaScript). 
    
    The app is structured into pages that show different aspects of typical ML/AI projects.
    """)


# Create pages and navigation
home_page = st.Page(show_home, title="Home Page", default=True)
eda_page = st.Page("eda.py", title="Exploratory Data Analysis")
model_page = st.Page("model.py", title="Model Usage")
pg = st.navigation([home_page, eda_page, model_page])
pg.run()
