import requests
import json
import pandas as pd

from utils.graph_db_call import query_graphdb_for_ontology

def azure_llm_call(
        shapley_values: pd.DataFrame,
        feature_descriptions = {},
        tone: str = "regulatory",
        language: str = "en",
        target_length: str = "short",
):
    # Set up your endpoint and API key
    ## FILL HERE
    
    
    
    
    #test
    # Define the headers and data
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }

    # Get descriptions if not available
    if feature_descriptions == {}:
        feature_descriptions = pd.read_csv("database/feature_descriptions.csv")

    # Query GraphDB and format data for prompt
    ontology_data = query_graphdb_for_ontology()

    # Convert the Shapley dictionary to a JSON-formatted string
    shapley_input = "\n".join(
        f"- **{row['Feature']}**: {row['SHAP Value']}"
        for _, row in shapley_values.iterrows()
    )

    # Build the feature descriptions section by iterating over the DataFrame
    feature_descriptions = "\n".join(
        f"- **{row['Feature']}**: {row['Description']}"
        for _, row in feature_descriptions.iterrows()
    )
    
    match target_length:
        case 'short':
            length_prompt = "The description should be very short and should contain the score and the improvement, if needed. A couple of example can be:\n - no improvement promtpt: The customer has a good score and is elegible for a residential mortgage.\n - improvement prompt: based on the scores, the customer is not elegible, mainbly because the income. \n In the improvement prompt, the income was an example; you should make the observation based on the shap values provided, and keep it short to just one value."
        case 'medium':
            length_prompt = (
                            "The description should be concise, containing the score, eligibility status, and specific observations about areas of concern based on SHAP values, only if needed, all in a discoursive way.\n\n"
                            "Examples:\n"
                            "- **No improvement prompt**: Customer 10293487 is in the top 10% of applicants, with a strong profile that meets most eligibility requirements for a residential mortgage. Financial metrics, including balance and transaction patterns, indicate reliability.\n\n"
                            "- **Improvement prompt**: Customer 20384712 has been flagged as high-risk due to low cash balance and limited investment holdings, with a high number of recent transactions that raise concerns. Additionally, their recent income pattern does not meet eligibility thresholds. Improvements to eligibility could include increasing balance consistency and reducing high-frequency transactions that impact their risk score.\n\n"
                            "In the improvement prompt, provide specific details on areas of concern based on SHAP values, focusing on impactful features from the values of the shap. Follow the structure of the examples to heart, and don't make bulleted points. Don't mention all the features, at most the 3 most relevant ones."
                        )
    
    # Final prompt string with Shapley values and feature descriptions integrated
    prompt = f"""
    Generate an explanation of the customer’s credit score based on their financial data and, if it's not satisfactory, what needs to be improved.

    Input Data:
    Customer Features with Shapley Values:
    {shapley_input}

    Feature Descriptions:
    Each feature's description and context for its relevance in determining creditworthiness:
    {feature_descriptions}

    Financial Features Context:
    {ontology_data}

    Explanation structure and examples:
    {length_prompt}
    
    Don't mention the features themselves, like for exmaple vermoegenszuwachs_3mo, but include them in a discursive way.

    Use this structure to generate a similar explanation based on the provided customer data.
    """

    print(prompt)

    data = {
        "messages": [
            {
                "role": "user", 
                "content": prompt
            }
        ],
        "max_tokens": 500
    }

    # Make the request
    response = requests.post(endpoint, headers=headers, json=data)

    # Print the result
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return f"Error: {response.status_code}, {response.text}"
