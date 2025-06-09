import requests
from bs4 import BeautifulSoup
import hashlib
import json

def get_status_data():
    url = "https://status.instructure.com/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    components = soup.find_all("div", class_="component-inner-container")
    data = []

    for component in components:
        name = component.find("span", class_="name").get_text(strip=True)
        status = component.find("span", class_="component-status").get_text(strip=True)
        data.append({"component": name, "status": status})

    return data

def hash_data(data):
    return hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()

def send_update(data):
    post_url = "https://yourserver.com/update_status"  # Replace with your endpoint
    headers = {"Content-Type": "application/json"}
    r = requests.post(post_url, json=data, headers=headers)
    print(f"POST response: {r.status_code}")

# For GitHub Actions we skip the loop and just run once
try:
    current_data = get_status_data()
    current_hash = hash_data(current_data)

    # Optional: store hash in a file or service to track changes
    # Here we just always post (you can customize this)
    send_update(current_data)

except Exception as e:
    print("❌ Error:", e)
