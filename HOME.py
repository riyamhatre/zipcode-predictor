import streamlit as st
import pandas as pd
import numpy as np


base="dark"
primaryColor="#0926f1"
backgroundColor="#22a5e8"

def app():
	header = st.container()
	dataset = st.container()
	features  = st.container()
	modelTraining = st.container()

	with header:
	    st.write('<p style="font-size:32px;"><b>Zip Code Recommendation Based on Given Factors</b></p>', unsafe_allow_html=True)
	    st.write('<p style="font-size:20px;">Welcome! This website is meant for you to find an ideal zip code based on your criteria. Enter any zip code here to see its general location on the map! After that, head to the Model tab on the left. </p>', unsafe_allow_html=True)
	location = pd.read_csv('location.csv')
	z = st.text_input("Enter a Zip Code!")
	if len(z) >1:
		st.map(location[location['ZIP'] == int(z)])
	else: 
		st.map(location)

