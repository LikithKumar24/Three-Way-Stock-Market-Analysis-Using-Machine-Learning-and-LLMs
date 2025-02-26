import requests

# Unauthenticated request to the paper search endpoint
BASE_URL = "https://api.semanticscholar.org/graph/v1"
query = "machine learning"
fields = "title,authors,abstract"
params = {
    "query": query,
    "fields": fields,
    "limit": 5
}

response = requests.get(f"{BASE_URL}/paper/search", params=params)

if response.status_code == 200:
    print(response.json())
else:
    print(f"Error: {response.status_code} - {response.text}")
