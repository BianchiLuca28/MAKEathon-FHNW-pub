import streamlit as st
import pandas as pd
import requests
import json

# Inside the MAKEathon, launch the Streamlit app by running the following command in the terminal:
# streamlit run ui/interface.py

from utils.azure_llm_call import azure_llm_call
from utils.model_prediction import model_prediction

# Sample DataFrame with preselected cases (replace with your actual data)
# Columns: "Index", "Features", "Shapley Values", and "Explanation"
df = pd.read_csv("database/customers_data.csv")

# Set up Streamlit interface
st.title("Preselected Customer Credit Score Explanation Tool")
st.markdown("Select a customer case to view the credit score explanation.")

# Sidebar for case selection
case_index = st.sidebar.selectbox("Select a Case Index:", df["ID"])

# Get selected case data
selected_case = df[df["ID"] == case_index].iloc[0]

# Call the model prediction function
prediction_dictionary = model_prediction(selected_case["ID"])
# print(prediction_dictionary)

# Show selected case's details in the main section
st.subheader("Selected Case Features")
st.write(prediction_dictionary['Feature'])

st.subheader("Selected Case Shapley Values")
st.write(prediction_dictionary["SHAP Value"])

print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
explanation = azure_llm_call(shapley_values=prediction_dictionary)

# Display the explanation in a text box
st.subheader("Explanation")
st.text_area("Credit Score Explanation", explanation, height=200)
