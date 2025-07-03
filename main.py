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
    print("Raw API response:")
    print(json.dumps(data, indent=2))  # Print the full response for debugging

    # Try to handle different possible structures
    jobs = []
    if isinstance(data, dict):
        # If the response is a dict with a list of job definitions
        if "data" in data and isinstance(data["data"], list):
            jobs = data["data"]
        elif "kind" in data and data["kind"] == "JobDefinition":
            jobs = [data]
        elif isinstance(data.get("items"), list):
            jobs = data["items"]
    elif isinstance(data, list):
        jobs = data

    if not jobs:
        print("No job definitions found.")
        return

    print("Job Definitions:")
    for job in jobs:
        print(f"- Name: {job.get('name')}, ID: {job.get('id')}")

if __name__ == "__main__":
    config = load_config("config.json")
    data = get_job_definitions(config)
    print_job_definitions(data)