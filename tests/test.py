import requests

url = "http://127.0.0.1:8000/user/check_or_create"
data = {"tg_user_id": 132, "user_tag": "sdfdf"}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())