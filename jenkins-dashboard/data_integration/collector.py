import os
import time
import requests
from pydantic import BaseModel, ValidationError
from typing import List, Optional, Dict, Any
from dotenv import load_dotenv

# This import assumes parser.py is in the same directory.
# If running as a module in a larger structure, it might be:
# from .parser import parse_jenkins_build_data, TargetBuildSchema
from parser import parse_jenkins_build_data #, TargetBuildSchema # TargetBuildSchema is used by type hint in parser

load_dotenv()

JENKINS_URLS = [url.strip() for url in os.getenv("JENKINS_URLS", "").split(',') if url.strip()]
JENKINS_USER = os.getenv("JENKINS_USER")
JENKINS_TOKEN = os.getenv("JENKINS_TOKEN")
POLLING_INTERVAL_SECONDS = int(os.getenv("POLLING_INTERVAL_SECONDS", "120"))
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://backend:8000/api/builds/ingress") # Hypothetical ingress endpoint
DEFAULT_MONITORED_JOBS_PATHS = os.getenv("DEFAULT_MONITORED_JOBS_PATHS", "job/bundle/job/meci-sm/job/MR-12700")

class JenkinsStageDataForCollector(BaseModel): # Simplified for collector's initial fetch if needed
    id: Optional[str] = None
    name: str
    status: str
    startTimeMillis: int
    durationMillis: int
    pauseDurationMillis: Optional[int] = 0

class JenkinsBuildDataFromWFAPI(BaseModel):
    id: str
    name: Optional[str] = None
    status: str
    startTimeMillis: int
    endTimeMillis: Optional[int] = None
    durationMillis: int
    queueDurationMillis: Optional[int] = None
    stages: Optional[List[JenkinsStageDataForCollector]] = []

def fetch_jenkins_data_from_wfapi(jenkins_url: str, job_path: str, build_number: str = "lastBuild") -> Optional[Dict[str, Any]]:
    api_url = f"{jenkins_url.rstrip('/')}/{job_path.strip('/')}/{build_number}/wfapi/describe"
    auth = (JENKINS_USER, JENKINS_TOKEN) if JENKINS_USER and JENKINS_TOKEN else None

    print(f"Fetching data from: {api_url}")
    try:
        response = requests.get(api_url, auth=auth, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {api_url}: {e}")
    except ValueError as e:
        print(f"Error decoding JSON from {api_url}: {e}")
    return None

def post_data_to_backend(processed_data_dict: Dict[str, Any]):
    if not BACKEND_API_URL:
        print("BACKEND_API_URL is not set. Skipping post to backend.")
        return

    print(f"Attempting to post to backend: {BACKEND_API_URL}")
    try:
        # The backend should expect data that matches its Pydantic schema for creating builds
        response = requests.post(BACKEND_API_URL, json=processed_data_dict, timeout=15)
        response.raise_for_status()
        print(f"Data posted successfully to backend for build {processed_data_dict.get('project')}/{processed_data_dict.get('mr_number')}/{processed_data_dict.get('build_number')}: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Error posting data to backend for build {processed_data_dict.get('project')}/{processed_data_dict.get('mr_number')}/{processed_data_dict.get('build_number')}: {e}")

def main_polling_loop():
    print("Starting Jenkins data collector polling loop...")
    if not JENKINS_URLS:
        print("No JENKINS_URLS configured. Exiting polling loop.")
        return

    monitored_jobs_list = [job.strip() for job in DEFAULT_MONITORED_JOBS_PATHS.split(',') if job.strip()]
    if not monitored_jobs_list:
        print("No DEFAULT_MONITORED_JOBS_PATHS configured. Exiting polling loop.")
        return

    while True:
        for jenkins_api_base_url in JENKINS_URLS:
            print(f"Polling Jenkins instance: {jenkins_api_base_url}")

            for job_path in monitored_jobs_list:
                raw_build_data_json = fetch_jenkins_data_from_wfapi(jenkins_api_base_url, job_path)

                if raw_build_data_json:
                    try:
                        # Validate raw data against expected wfapi structure (optional here, parser will validate its input)
                        # JenkinsBuildDataFromWFAPI(**raw_build_data_json)

                        parsed_and_transformed_data_model = parse_jenkins_build_data(
                            raw_data=raw_build_data_json,
                            jenkins_base_url=jenkins_api_base_url,
                            job_path_segment=job_path
                        )

                        if parsed_and_transformed_data_model:
                            post_data_to_backend(parsed_and_transformed_data_model.dict())
                        else:
                            print(f"Failed to parse data for {job_path} from {jenkins_api_base_url}")

                    except ValidationError as e: # Pydantic validation error
                        print(f"Pydantic validation error during processing for {job_path}: {e}")
                    except Exception as e: # Other unexpected errors
                        print(f"Unexpected error processing build data for {job_path}: {e}")

        print(f"Polling cycle complete. Sleeping for {POLLING_INTERVAL_SECONDS} seconds...")
        time.sleep(POLLING_INTERVAL_SECONDS)

if __name__ == "__main__":
    print("Data integration collector script initialized.")
    # This will be the entry point for the Docker container
    main_polling_loop()
