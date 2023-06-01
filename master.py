import streamlit as st
import pandas as pd 
import numpy as np
base="dark"
primaryColor="#0926f1"
backgroundColor="#22a5e8"


import model
import zip_stats
import about

PAGES = {
    "Zip Code Recommendation System ": model,
    "Zip Code Statistics": zip_stats,
    "About": about
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("", list(PAGES.keys()))
page = PAGES[selection]
page.app()
