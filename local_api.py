import requests

base_url = "http://127.0.0.1:8000"

get_response = requests.get(
    f"{base_url}/",
    timeout=30,
)

print(f"Status Code: {get_response.status_code}")
print(f"Result: {get_response.json()['message']}")


data = {
    "age": 37,
    "workclass": "Private",
    "fnlgt": 178356,
    "education": "HS-grad",
    "education-num": 10,
    "marital-status": "Married-civ-spouse",
    "occupation": "Prof-specialty",
    "relationship": "Husband",
    "race": "White",
    "sex": "Male",
    "capital-gain": 0,
    "capital-loss": 0,
    "hours-per-week": 40,
    "native-country": "United-States",
}

post_response = requests.post(
    f"{base_url}/data/",
    json=data,
    timeout=30,
)

print(f"Status Code: {post_response.status_code}")
print(f"Result: {post_response.json()['result']}")
