#!/bin/bash

# Script to seed sample stage data into the Jenkins Dashboard application
# Ensure the application is running (e.g., via 'docker-compose up') before executing this script.

API_ENDPOINT="http://localhost:8000/api/v1/ingress/stage"

echo "Sending sample stage data to $API_ENDPOINT"
echo "--------------------------------------------------"

# Sample Data Array (using bash arrays for easier management)
# Note: Ensure jq is installed if you want to pretty-print JSON responses, otherwise remove | jq
# On most systems: sudo apt-get install jq OR brew install jq

declare -a stages_data=(
'{ "pipeURL":"http://swalgo-jeci.mobileye.com:8080/job/bundle/job/meci-sm/job/MR-12700/2/", "group":"bundle", "repo":"meci-sm", "MR_num":"12700", "build_num":"2", "displayName":"Init", "durationInMillis":15028, "result":"SUCCESS", "startTime":"2025-06-03T10:12:48.155+0300" }'
'{ "pipeURL":"http://swalgo-jeci.mobileye.com:8080/job/bundle/job/meci-sm/job/MR-12700/2/", "group":"bundle", "repo":"meci-sm", "MR_num":"12700", "build_num":"2", "displayName":"Load Pipeline", "durationInMillis":189174, "result":"SUCCESS", "startTime":"2025-06-03T10:13:45.678+0300" }'
'{ "pipeURL":"http://swalgo-jeci.mobileye.com:8080/job/bundle/job/meci-sm/job/MR-12700/2/", "group":"bundle", "repo":"meci-sm", "MR_num":"12700", "build_num":"2", "displayName":"Repos Clone", "durationInMillis":21076, "result":"SUCCESS", "startTime":"2025-06-03T10:16:55.084+0300" }'
'{ "pipeURL":"http://swalgo-jeci.mobileye.com:8080/job/bundle/job/meci-sm/job/MR-12700/2/", "group":"bundle", "repo":"meci-sm", "MR_num":"12700", "build_num":"2", "displayName":"Dev Clone", "durationInMillis":16889, "result":"SUCCESS", "startTime":"2025-06-03T10:16:59.271+0300" }'
'{ "pipeURL":"http://swalgo-jeci.mobileye.com:8080/job/bundle/job/meci-sm/job/MR-12700/2/", "group":"bundle", "repo":"meci-sm", "MR_num":"12700", "build_num":"2", "displayName":"Known Issues Clone", "durationInMillis":16814, "result":"SUCCESS", "startTime":"2025-06-03T10:16:59.346+0300" }'
'{ "pipeURL":"http://swalgo-jeci.mobileye.com:8080/job/bundle/job/meci-sm/job/MR-12700/2/", "group":"bundle", "repo":"meci-sm", "MR_num":"12700", "build_num":"2", "displayName":"Ref Clone", "durationInMillis":16853, "result":"SUCCESS", "startTime":"2025-06-03T10:16:59.307+0300" }'
'{ "pipeURL":"http://swalgo-jeci.mobileye.com:8080/job/bundle/job/meci-sm/job/MR-12700/2/", "group":"bundle", "repo":"meci-sm", "MR_num":"12700", "build_num":"2", "displayName":"SWALGO Scripts Clone", "durationInMillis":16774, "result":"SUCCESS", "startTime":"2025-06-03T10:16:59.386+0300" }'
'{ "pipeURL":"http://swalgo-jeci.mobileye.com:8080/job/bundle/job/meci-sm/job/MR-12700/2/", "group":"bundle", "repo":"meci-sm", "MR_num":"12700", "build_num":"2", "displayName":"Update Submodules", "durationInMillis":57526, "result":"SUCCESS", "startTime":"2025-06-03T10:17:16.515+0300" }'
'{ "pipeURL":"http://swalgo-jeci.mobileye.com:8080/job/bundle/job/meci-sm/job/MR-12700/2/", "group":"bundle", "repo":"meci-sm", "MR_num":"12700", "build_num":"2", "displayName":"Dev Submodules", "durationInMillis":51090, "result":"SUCCESS", "startTime":"2025-06-03T10:17:22.951+0300" }'
'{ "pipeURL":"http://swalgo-jeci.mobileye.com:8080/job/bundle/job/meci-sm/job/MR-12700/2/", "group":"bundle", "repo":"meci-sm", "MR_num":"12700", "build_num":"2", "displayName":"Ref Submodules", "durationInMillis":51065, "result":"SUCCESS", "startTime":"2025-06-03T10:17:22.976+0300" }'
'{ "pipeURL":"http://swalgo-jeci.mobileye.com:8080/job/bundle/job/meci-sm/job/MR-12700/2/", "group":"bundle", "repo":"meci-sm", "MR_num":"12700", "build_num":"2", "displayName":"Run Tasker", "durationInMillis":75734, "result":"SUCCESS", "startTime":"2025-06-03T10:18:14.393+0300" }'
'{ "pipeURL":"http://swalgo-jeci.mobileye.com:8080/job/bundle/job/meci-sm/job/MR-12700/2/", "group":"bundle", "repo":"meci-sm", "MR_num":"12700", "build_num":"2", "displayName":"Run 1/1", "durationInMillis":192596, "result":"UNSTABLE", "startTime":"2025-06-03T10:19:49.507+0300" }'
'{ "pipeURL":"http://swalgo-jeci.mobileye.com:8080/job/bundle/job/meci-sm/job/MR-12700/2/", "group":"bundle", "repo":"meci-sm", "MR_num":"12700", "build_num":"2", "displayName":"meci_toolkit:JIRA:jira_validation_19880dd6", "durationInMillis":192500, "result":"UNSTABLE", "startTime":"2025-06-03T10:19:49.603+0300" }'
'{ "pipeURL":"http://swalgo-jeci.mobileye.com:8080/job/bundle/job/meci-sm/job/MR-12700/2/", "group":"bundle", "repo":"meci-sm", "MR_num":"12700", "build_num":"2", "displayName":"Finish", "durationInMillis":626, "result":"SUCCESS", "startTime":"2025-06-03T10:23:04.223+0300" }'
# Stages with missing startTime (will be treated as null by backend)
'{ "pipeURL":"http://swalgo-jeci.mobileye.com:8080/job/bundle/job/meci-sm/job/MR-12700/2/", "group":"bundle", "repo":"meci-sm", "MR_num":"12700", "build_num":"2", "displayName":"Declarative: Checkout SCM", "result":"SUCCESS", "durationInMillis":35086 }'
'{ "pipeURL":"http://swalgo-jeci.mobileye.com:8080/job/bundle/job/meci-sm/job/MR-12700/2/", "group":"bundle", "repo":"meci-sm", "MR_num":"12700", "build_num":"2", "displayName":"Declarative: Post Actions", "result":"UNSTABLE", "durationInMillis":292314 }'
)

# Iterate over the array and send each JSON payload
for data in "${stages_data[@]}"; do
  echo ""
  echo "Sending data: $data"
  response_code=$(curl -s -o /dev/stderr -w "%{http_code}" -X POST -H "Content-Type: application/json" -d "$data" "$API_ENDPOINT")
  # The actual JSON response body is sent to /dev/stderr above so it appears on the console.
  # We only capture the HTTP status code in the variable.

  echo "" # Newline after stderr output from curl
  if [ "$response_code" -eq 201 ]; then
    echo "SUCCESS: Stage data accepted (HTTP $response_code)"
  else
    echo "ERROR: Stage data ingestion failed (HTTP $response_code)"
    # The error response from API (if any) would have been printed to stderr by curl.
  fi
  echo "--------------------------------------------------"
  sleep 0.1 # Small delay between requests
done

echo "Sample data seeding complete."
echo "Check the application UI or API to see the ingested data."
