# Medical Chatbot with LLM, LangChain, Pinecone and AWS Deployment

This project builds a medical question answering chatbot using a retrieval based LLM pipeline. The system uses LangChain with OpenAI models and Pinecone vector database to search documents and generate responses. The backend is written in Flask and the application is containerized with Docker. The project also includes a full deployment pipeline using GitHub Actions, AWS ECR, and EC2 so the chatbot can run in a cloud environment.

The goal of this project was to understand how real AI applications are built and deployed, not just trained locally. The system supports document embeddings, vector search, API based inference, and automated deployment to a remote server.

Tech stack used in the project includes Python, LangChain, OpenAI API, Pinecone, Flask, Docker, AWS EC2, AWS ECR, and GitHub Actions.

The deployment workflow works as follows. When code is pushed to GitHub, a GitHub Actions workflow builds a Docker image and pushes it to Amazon ECR. The EC2 instance runs as a self hosted runner and pulls the latest image, then starts the container automatically. This allows the chatbot to be updated without manual deployment.

To run locally, first clone the repository and create a Python environment. Install the dependencies from requirements.txt and create a .env file with the OpenAI and Pinecone keys. After that, run the indexing script to store document embeddings in Pinecone, then start the Flask server. The chatbot will be available on localhost.

AWS deployment requires an IAM user with programmatic access, an ECR repository, and an EC2 instance with Docker installed. The EC2 machine is configured as a GitHub self hosted runner so the CI/CD pipeline can deploy automatically.

This project demonstrates experience with LLM applications, vector databases, backend development, Docker, cloud deployment, and CI/CD automation. The focus was on building a complete working system similar to what is used in real production environments rather than only training a model in a notebook.

Repository link  
https://github.com/aerofa45/Chatbot
