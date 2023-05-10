import streamlit as st
import pandas as pd
import numpy as np


base="dark"
primaryColor="#0926f1"
backgroundColor="#22a5e8"

def app():
	st.title("Note From the Creator:")
	st.write("This project has some humble beginnings, starting from an ordinary walk with a friend and a quick game of “guess the house price” in the richer part of town. I took the game a little further and checked out random housing prices in different neighborhoods and different cities on my computer. All these ideas and curiosities started merging together, and I could see my project coming to life. ")
	st.write("Over the course of the year, I used the data that I gathered from various sources (databases, websites, web scraping, etc) and  constructed a recommender system that took in a person’s preferences and outputted a zip code that matches their criteria the best. The challenges I faced during this journey were more of stepping stones that propelled me to the next phase of the adventure. They served as learning points and opportunities for skill growth. I gained more knowledge about the housing market and was surprised to see how so many factors come into play when deciding on an ideal location.")
	st.write("In a world where the uncertainties of the housing market can be daunting, it is always nice to have a way to narrow down places to live based on relevant factors. This project aims to be a useful aid and a form of reassurance that there is always a place for someone in this country.")
	st.write('<p style="font-family: cursive;">-- Riya Mhatre, Data Science/Business Psychology Major + Music Minor at UC San Diego</p>', unsafe_allow_html=True)
	st.write("Special thanks: This project could not be done without the help of my mentor, Dr. Justin Eldridge. ")