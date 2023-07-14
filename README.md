# ETL (Migration of data from SQS to postgreSQL)
    This project focuses on creating an application that reads data from an AWS SQS Queue, performs data transformation, and writes the transformed data to a PostgreSQL database. The application utilizes Docker to run all the components locally.

## Prerequisites

    Before running the application, ensure that the following software is installed on your system:

1. Python (latest version)
2. Docker
3. PostgreSQL

## Setup

1. Install Python, Docker, and PostgreSQL in your system as mentioned in the assignment and set them up.

2. Pull the required Docker images by running the following commands:

    docker pull fetchdocker/data-takehome-localstack
    docker pull fetchdocker/data-takehome-postgres
    
        or 
    To avoid above steps just do run below command by pointing to docker-compose.yml file from the directory

        docker-compose up

1. Start the LocalStack container to simulate AWS services locally:

    docker run -d -p 4566:4566 -p 4571:4571 localstack/localstack

2. Create a local SQS queue in LocalStack by running the following command:

    aws --endpoint-url=http://localhost:4566 sqs create-queue --queue-name my-queue

    Create an sqs.json file in the same directory. A sample sqs.json file is attached above.

    Send a message to the queue using the sqs.json file:(update sqs.json with relative path)

        aws --endpoint-url=http://localhost:4566 sqs send-message --queue-url http://localhost:4566/000000000000/my-queue --message-body file://sqs.json

3. Once the data is pushed to the queue, create the required table in PostgreSQL. Connect to your PostgreSQL database and execute the following query:

    CREATE TABLE IF NOT EXISTS user_logins (
        user_id varchar(128),
        device_type varchar(32),
        masked_ip varchar(256),
        masked_device_id varchar(256),
        locale varchar(32),
        app_version integer,
        create_date date
    );

4. Open the sqs_to_psql.py file and make any necessary changes to usernames and passwords if required.

5. Run the sqs_to_psql.py file using the command python3 sqs_to_psql.py.

6. The migration of data from the SQS queue to PostgreSQL will be performed.

7. To verify the migration, connect to your PostgreSQL database and execute the following query:

    psql -d postgres -U postgres -p 5432 -h localhost -W
    select * from user_logins;
8. Note:

    You can keep the code running in an infinite loop to continuously fetch messages from the SQS queue. Currently, it's stopped to prevent continuous execution. If needed, add a while True loop before the relevant function.

    To load data to the SQS queue (LocalStack), run the command mentioned in step 4(c) with the appropriate file path, updating it with the JSON file.

## Next Steps
    The code can be enhanced to handle error handling and logging for better production readyness.

    Scaling the application can be achieved by deploying it in a container orchestration platform like Kubernetes, where multiple instances of the application can be run to handle increased message load.

    For recovery of PII data, a backup and restore for the PostgreSQL database can be implemented.

## Deployment in Production

To deploy this application in production, you can follow these steps:

Containerize the application using Docker: 
    Create a Docker image for the application that includes all the necessary dependencies and configurations.You can use my docker-compose.yml file and update with all the dependencies and configurations

Set up a container orchestration platform: 
    Deploy the Docker image to a container orchestration platform like Kubernetes or AWS ECS(Elastic Container Service). Configure the platform to manage the deployment, scaling, and monitoring of the application.

Use a cloud provider: 
    Utilize a cloud provider such as AWS, Azure, or Google Cloud to host the application. Set up infrastructure resources such as virtual machines, load balancers, and databases to support the application's operation.

Automated deployment: 
    Set up a CI/CD pipeline to automate the build, testing, and deployment of the application. This ensures efficient and consistent deployment processes.

Secure the application: 
    Implement security measures such as access controls, encryption, and authentication to protect the application and its data. Follow security best practices to mitigate risks and vulnerabilities.

Monitoring and logging: 
    Set up monitoring and logging solutions to track the application's performance, detect issues, and collect logs for analysis. Use tools like New Relic, Data Dog, Prometheus, or ELK stack for effective monitoring and troubleshooting.

## Additional Components for Production Readiness
To make this application production-ready, consider adding the following components:

Scalability: 
    Design the application to handle growing datasets by utilizing scalable architectures. Implement techniques like horizontal scaling, sharding, or utilizing distributed systems to accommodate increased data volumes and  traffic.

Security enhancements: 
    Strengthen the security of the application by implementing encryption at rest, enforcing access controls, and adhering to security best practices. Regularly update and patch software components to mitigate vulnerabilities.

Backup and recovery: 
    Set up regular backups of the PostgreSQL database to ensure data integrity and disaster recovery. Implement backup strategies based on the data retention requirements and recovery point objectives.

Documentation and monitoring: 
    Maintain comprehensive documentation to aid in understanding and maintaining the application. Set up monitoring solutions to track performance metrics, identifying bottlenecks, and proactively addressing issues.

## Scaling with a Growing Dataset
To handle a growing dataset, consider the following strategies:

Database optimization: 
    Optimize the PostgreSQL database by adding indexes, partitioning tables, and using appropriate query optimization techniques. This will improve query performance and ensure efficient data retrieval.

Distributed message queue: 
    Replace the local SQS queue with a distributed message queue system like Apache Kafka or RabbitMQ. This allows for horizontal scaling by distributing message processing across multiple nodes.

Horizontal scaling: 
    Deploy multiple instances of the application and distribute the load across them. Utilize a load balancer to distribute incoming requests to these instances. This approach increases the processing capacity and enables the application to handle larger datasets.

Data partitioning: 
    Implement data partitioning techniques to divide the dataset into smaller subsets based on specific criteria. This allows for efficient data retrieval and processing, as well as improved scalability.

## Recovery of PII (Personally Identifiable Information)
To recover PII data, consider the following measures:

Data retention policies: 
    Define data retention policies that specify how long PII data should be stored. Ensure compliance with applicable data protection regulations.

Secure storage: 
    Implement secure storage mechanisms for PII data, such as encryption or tokenization. This ensures that even if the data is compromised, it remains unreadable to unauthorized parties.

Access controls: 
    Implement strict access controls to restrict access to PII data. Grant access only to authorized personnel who require it for legitimate purposes.

    

## Assumptions
    The provided code assumes that the required Python libraries (Boto3 and Psycopg2) are installed.

    The Docker images used in the setup contain the necessary preloaded data and configurations.

    The PostgreSQL database is running on the local machine with default settings.

    The provided sample sqs.json file adheres to the expected JSON structure.

    Proper security measures and access controls are in place to protect sensitive data.

    Please make sure to include the necessary code files, such as `sqs_to_psql.py`, `sqs.json`, and any other relevant files, along with this README file in your submission.

    Please note that the code provided is a simplified example, and in a production environment, additional security measures and best practices should be implemented to protect PII data effectively.

    If you want to make any changes to your postgres or any credentials make those changes in config.json file
    Every credential is read from this file.
