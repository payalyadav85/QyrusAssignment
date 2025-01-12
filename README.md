# QyrusAssignment
Data Engineer QyrusAssignment


1. Clone the repository
    git clone https://github.com/payalyadav85/QyrusAssignment.git
2. Start the services using Docker Compose
    docker-compose up
3. Populate the SQS queue with sample data
    Use the provided Python script in the scripts folder to send messages to the Localstack SQS queue:
        python3 scripts/populate_sqs.py
4. Run the worker service using the command : 
    Use the worker service to poll messages from the SQS queue, process them, and update Redis.
        python3 worker/worker.py
5. Test the API endpoints
    Use curl or a browser to hit the following endpoints:
    curl http://localhost:8080/users/USER1/stats
    curl http://localhost:8080/stats/global
