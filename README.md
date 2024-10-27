# PostFinance Explainable AI for Credit Score Analysis

This project aims to provide explainable insights into credit scores for customers at PostFinance, combining **Machine Learning**, **Explainable AI (Shapley values)**, a **Knowledge Graph** (GraphDB), and **LLMs** for natural language explanations. Built with a **Streamlit** interface, the solution empowers operators with contextualized, human-readable insights into credit score factors.

## Features
- **Predictive Model**: Calculates credit scores and extracts Shapley values to highlight feature importance.
- **Knowledge Graph Integration**: Enriches feature explanations, connecting them to financial concepts like stability and liquidity.
- **LLM-Powered Explanations**: Generates comprehensive summaries in natural language using Azure/OpenAI.
- **Interactive UI**: A PostFinance-branded Streamlit interface with case selection for user-friendly analysis.

## Tech Stack
- **Python**
- **Streamlit**
- **GraphDB (via Docker)**
- **Azure/OpenAI API**

## Quick Start
1. Clone the repository and install dependencies.
2. Set up GraphDB with Docker and load the custom ontology.
3. Run `interface.py` with Streamlit to launch the UI.

