# Jenkins Pipeline Dashboard

This project is a comprehensive Jenkins pipeline monitoring and analytics dashboard.
It ingests data from the Jenkins Blue Ocean API, stores it in PostgreSQL,
and provides real-time visualization and historical analysis of CI/CD pipeline performance.

## Modules

*   **Backend:** FastAPI application providing the API.
*   **Frontend:** React/TypeScript application for the user interface.
*   **Data Integration:** Python scripts for collecting and parsing data from Jenkins.

## Getting Started

(Instructions will be added here once the core components are in place)

## Running the Application

1.  **Environment Setup**:
    *   Copy `.env.example` to `.env` and customize the variables if needed (e.g., database credentials, Jenkins URLs for data collection - though data collection is currently manual via API).
    *   `cp .env.example .env`

2.  **Build and Start Services**:
    *   Use the `check_app.sh` script to build, start, and perform initial health checks:
        \`\`\`bash
        ./check_app.sh
        \`\`\`
    *   Alternatively, you can run Docker Compose manually:
        \`\`\`bash
        docker-compose up --build -d
        \`\`\`

3.  **Accessing Services**:
    *   **Frontend UI**: [http://localhost:3000](http://localhost:3000)
    *   **Backend OpenAPI Docs**: [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)

4.  **Seeding Sample Data**:
    *   After the application is running, you can populate the database with sample stage data using the `seed_data.sh` script:
        \`\`\`bash
        ./seed_data.sh
        \`\`\`
    *   This script will send POST requests to the `/api/v1/ingress/stage` endpoint.

5.  **Stopping Services**:
    *   \`\`\`bash
        docker-compose down
        \`\`\`
