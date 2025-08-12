import requests
from pprint import pprint
response = requests.post(
    "http://localhost:8000/api/v1/search",
    json={
        "query": "Best whodunnit tv shows of the last decade",
        "max_results": 10
    }
)

pprint(response.json())