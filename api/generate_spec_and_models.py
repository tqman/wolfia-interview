import json
import os
import subprocess
from pathlib import Path
from time import sleep, time

import requests
from openapi_spec_validator import validate


def format_and_validate_openapi_spec(spec_content):
    """
    Formats the OpenAPI JSON spec and validates it.
    """
    spec = json.loads(spec_content)
    validate(spec)
    return json.dumps(spec, indent=2)


def export_openapi_spec(api_url, output_path):
    """
    Fetches the OpenAPI specification from a FastAPI server and saves it to a file.
    """
    response = requests.get(f"{api_url}/openapi.json")
    response.raise_for_status()
    formatted_spec = format_and_validate_openapi_spec(response.text)
    with open(output_path, "w") as file:
        file.write(formatted_spec)


def generate_frontend_models(frontend_path):
    """
    Runs the script to generate frontend models from the OpenAPI specification.
    """
    os.chdir(frontend_path)
    subprocess.run(["npm", "run", "open-api:generate"], check=True)


def wait_for_server(url, timeout=60):
    """
    Wait for the FastAPI server to start.
    """
    start_time = time()
    while time() - start_time < timeout:
        try:
            response = requests.get(url)
            if response.status_code == 200:
                return True
        except requests.ConnectionError:
            sleep(1)
    return False


def main():
    fastapi_server_url = "http://localhost:2020"
    api_spec_output_path = Path(__file__).parent / "openapi.json"
    frontend_directory_path = Path(__file__).parent.parent / "frontend"

    if not wait_for_server(f"{fastapi_server_url}/openapi.json"):
        raise RuntimeError("FastAPI server did not start in time.")

    export_openapi_spec(fastapi_server_url, api_spec_output_path)
    generate_frontend_models(frontend_directory_path)


if __name__ == "__main__":
    main()
