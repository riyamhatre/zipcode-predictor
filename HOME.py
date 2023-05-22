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
	    st.write('<p style="font-size:20px;">This part of the website consists of the model. Here, you will input your criteria. After answering the questions on the page and hitting the button at the bottom, you can head to the Zip Code Statistics tab at the left to see some relevant data about your recommended zip code. </p>', unsafe_allow_html=True)
	location = pd.read_csv('/Users/riyamhatre/Desktop/HDSI/location.csv')
	z = st.text_input("Enter a Zip Code!")
	if len(z) >1:
		st.map(location[location['ZIP'] == int(z)])
	else: 
		st.map(location)

