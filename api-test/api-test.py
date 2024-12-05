import requests

BASE_URL = "http://16.170.251.94:8000"

# Test /run
run_data = {
    "BUSINESS_DETAILS": "Akki AI helps founders analyze startup pitches.",
    "PRODUCT_DESCRIPTION": "A platform to get detailed feedback on startup ideas."
}

response = requests.post(f"{BASE_URL}/run", json=run_data)
print("Run Response:", response.status_code, response.json())

# Test /train
train_data = {
    "BUSINESS_DETAILS": "Akki AI helps founders analyze startup pitches.",
    "PRODUCT_DESCRIPTION": "A platform to get detailed feedback on startup ideas.",
    "n_iterations": 10,
    "filename": "training_data.json"
}

response = requests.post(f"{BASE_URL}/train", json=train_data)
print("Train Response:", response.status_code, response.json())

# Test /replay
replay_data = {"task_id": "some_task_id"}

response = requests.post(f"{BASE_URL}/replay", json=replay_data)
print("Replay Response:", response.status_code, response.json())

# Test /test
test_data = {
    "BUSINESS_DETAILS": "Akki AI helps founders analyze startup pitches.",
    "PRODUCT_DESCRIPTION": "A platform to get detailed feedback on startup ideas.",
    "n_iterations": 5,
    "openai_model_name": "gpt-4"
}

response = requests.post(f"{BASE_URL}/test", json=test_data)
print("Test Response:", response.status_code, response.json())
