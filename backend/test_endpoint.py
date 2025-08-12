import requests

response = requests.post(
    "http://localhost:8000/api/v1/search",
    json={
        "query": "best budget gaming laptops",
        "max_results": 5
    }
)

print(response.json())