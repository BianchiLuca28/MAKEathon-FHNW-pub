import requests

# Define GraphDB SPARQL endpoint and repository name
sparql_endpoint = "http://localhost:7200/repositories/mortgage"

# Format ontology data for prompt
def format_ontology_data_for_prompt(ontology_data):
    formatted_data = []
    if ontology_data:
        for result in ontology_data["results"]["bindings"]:
            feature_label = result["featureLabel"]["value"]
            description = result["description"]["value"]
            impact = result.get("impact", {}).get("value", "no specific impact mentioned")
            concept = result.get("concept", {}).get("value", "no specific concept contribution")

            # Format each feature's information
            formatted_data.append(
                f"Feature: {feature_label}\nDescription: {description}\nImpact on Creditworthiness: {impact}\nContributes to: {concept}\n"
            )
    return "\n".join(formatted_data)

def query_graphdb_for_ontology():
    sparql_query = """
    SELECT ?feature ?featureLabel ?description ?impact ?concept
    WHERE {
        ?feature rdf:type ex:Feature ;
                 rdfs:label ?featureLabel ;
                 ex:description ?description .
        OPTIONAL {
            ?feature ex:affectsCreditworthiness ex:Creditworthiness ;
                     rdfs:label ?impact .
        }
        OPTIONAL {
            ?feature ex:contributesTo ?concept .
            ?concept rdfs:label ?conceptLabel .
        }
    }
    """
    headers = {
        "Content-Type": "application/sparql-query",
        "Accept": "application/sparql-results+json"
    }
    response = requests.post(sparql_endpoint, data=sparql_query, headers=headers)
    if response.status_code == 200:
        return format_ontology_data_for_prompt(response.json())
    else:
        print(f"Query failed with status code {response.status_code}")
        return None
