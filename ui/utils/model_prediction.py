import pickle
import pandas as pd


with open('models/random_forest_model.pkl', 'rb') as file:
    rf = pickle.load(file)

with open('models/shap_explainer.pkl', 'rb') as file:
    explainer = pickle.load(file)

# Load the original dataset
df = pd.read_csv('database/cleaned_dataset.csv')
    

def model_prediction(customer_id):
    df_dummies = pd.get_dummies(df, columns=['residence_status'], drop_first=True)

    # Retrieve the customer's data from the original dataset
    customer_data = df_dummies[df_dummies['ID'] == customer_id]
    if customer_data.empty:
        print(f"No customer found with ID {customer_id}")
        return None

    # Drop irrelevant columns
    customer_data_cleaned = customer_data.drop(columns=['ID', 'TARGET'])

    # One-hot encode 'residence_status' and ensure same columns as training data
    if 'residence_status' in customer_data_cleaned.columns:
        customer_data_cleaned = pd.get_dummies(customer_data_cleaned, columns=['residence_status'], drop_first=True)

    # Convert boolean columns to integers
    bool_cols = customer_data_cleaned.select_dtypes(include=['bool']).columns.tolist()
    customer_data_cleaned[bool_cols] = customer_data_cleaned[bool_cols].astype(int)

    # Compute SHAP values for the customer
    shap_values = explainer(customer_data_cleaned)

    # Extract SHAP values for class 1
    shap_values_array = shap_values.values[0, :, 1]  # Shape: (n_features,)

    # Get feature names and values
    feature_names = customer_data_cleaned.columns
    feature_values = customer_data_cleaned.values[0]

    # Create DataFrame
    individual_explanation = pd.DataFrame({
        'Feature': feature_names,
        'Feature Value': feature_values,
        'SHAP Value': shap_values_array
    })

    # Sort by absolute SHAP value
    individual_explanation['abs_SHAP_Value'] = individual_explanation['SHAP Value'].abs()
    individual_explanation = individual_explanation.sort_values(by='abs_SHAP_Value', ascending=False).reset_index(drop=True)

    # Optionally, convert to dictionary
    # result_dict = individual_explanation[['Feature', 'Feature Value', 'SHAP Value']].to_dict('records')
    # return result_dict

    return individual_explanation