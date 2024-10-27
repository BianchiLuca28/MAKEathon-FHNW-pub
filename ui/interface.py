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
st.title("FinanceLense AI")
st.markdown("Select a customer case to view the credit score explanation.")

# Logo on the left small corner
st.sidebar.image("ui/images/PostFinanceLogo.png", use_column_width=True)

# Sidebar for case selection
# case_index = st.sidebar.selectbox("Select a Case Index:", df["ID"])

case_index = st.sidebar.selectbox(
    "Select a Case Index:", 
    options=["Select a Case"] + df["ID"].tolist()  # Add placeholder option
)

# Check if a valid case has been selected (i.e., not "Select a Case")
if case_index != "Select a Case":
    # Get selected case data
    selected_case = df[df["ID"] == case_index].iloc[0]

    # Call the model prediction function
    prediction_dictionary = model_prediction(selected_case["ID"])
    # print(prediction_dictionary)

    explanation = azure_llm_call(shapley_values=prediction_dictionary)

    # Display the explanation in a text box
    st.subheader("Explanation")
    st.text_area("Credit Score Explanation", explanation, height=200)

    st.subheader("Selected Case")
    st.table(prediction_dictionary[["Feature", "Feature Value"]])
    # st.write(prediction_dictionary[["Feature", "Feature Value", "SHAP Value"]])