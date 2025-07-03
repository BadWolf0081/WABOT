import requests
import json
from requests.auth import HTTPBasicAuth
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_config(path="config.json"):
    with open(path, "r") as f:
        return json.load(f)

def get_job_definitions(config):
    url = f"{config['api_base_url']}/twsd/api/v2/model/jobdefinition"
    print(f"Querying job definitions from: {url}")
    auth = HTTPBasicAuth(config["api_username"], config["api_password"])
    headers = {
        "Accept": "application/json"
    }
    response = requests.get(url, auth=auth, headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

def print_job_definitions(data):
    if not data or "data" not in data:
        print("No job definitions found.")
        return
    print("Job Definitions:")
    for job in data["data"]:
        print(f"- Name: {job.get('name')}, ID: {job.get('id')}")

if __name__ == "__main__":
    config = load_config("config.json")
    data = get_job_definitions(config)
    print_job_definitions(data)