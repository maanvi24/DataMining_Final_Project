#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 08:42:59 2023

@author: Maanvi
"""

import streamlit as st



st.markdown("<h1 style='text-align: center;'>Stock Prediction App</h1>", unsafe_allow_html=True)
# Page title


st.markdown("""
We strive to make stock market insights easy and accessible for everyone. Explore our platform to make informed decisions in the dynamic world of stocks!
""")

# Instructions
st.subheader("Instructions to use the App:")

#Prediction 
st.markdown("- **Prediction Page:**")
st.markdown("Input an article and press predict to know if the stock will go up or not")
st.markdown("You will also get other relevant information such as the likelihood of the stock going up or down, sentiment score to understand the tone of the article and a score that tells the relevance of the article to a certain field like technology,etc")

# Live Feed section
st.markdown("- **Live Feed Page:**")
st.markdown("Input a stock ticker of your choice for example AAPL( Apple Stock) and duration to get all the relevant articles and some more useful information.")

# Summary Page section
st.markdown("- **Summary Page:**")
st.markdown("Input an article and the desired length to get a quick overview of complex information.")


