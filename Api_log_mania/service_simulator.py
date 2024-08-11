import requests
import time
import jwt

SERVICE_NAME = "service_1"
TOKEN = jwt.encode({"service_name": SERVICE_NAME}, "your_secret_key", algorithm="HS256")

def send_log(log_level, message):
    url = "http://127.0.0.1:8000/logs"
    log_data = {
        "service_name": SERVICE_NAME,
        "log_level": log_level,
        "message": message
    }
    headers = {"Authorization": f"Bearer {TOKEN}"}
    response = requests.post(url, json=log_data, headers=headers)
    print(response.status_code, response.json())

if __name__ == "__main__":
    while True:
        send_log("INFO", "This is a log message")
        time.sleep(5)
