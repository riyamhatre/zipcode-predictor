import streamlit as st
import pandas as pd 
import numpy as np
base="dark"
primaryColor="#0926f1"
backgroundColor="#22a5e8"


import model
import HOME
import zip_stats
import about

PAGES = {
	"Home": HOME,
    "Model": model,
    "Zipcode Statistics": zip_stats,
    "About": about
}
st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
