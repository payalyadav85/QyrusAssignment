1. Clone the repository
    git clone <repository-link>
    cd <repository-folder>
2. Start the services using Docker Compose
    docker-compose up
3. Populate the SQS queue with sample data
    Use the provided Python script in the scripts folder to send messages to the Localstack SQS queue:
        python scripts/populate_sqs.py
4. Verify the worker processes the messages
    The worker service will read messages from the SQS queue, process them, and update Redis.
5. Test the API endpoints
    Use curl or a browser to hit the following endpoints:
    curl http://localhost:8080/users/USER1/stats
    curl http://localhost:8080/stats/global
