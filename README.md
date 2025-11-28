
---

# **Build a Complete Medical Chatbot with LLMs, LangChain, Pinecone, Flask & AWS CI/CD**

This project demonstrates how to build a **production-ready medical chatbot** using:

* **LLMs (GPT-4o)**
* **LangChain**
* **Pinecone Vector Database**
* **Flask backend**
* **Docker**
* **AWS (ECR + EC2)**
* **GitHub Actions for CI/CD**

---

# **Local Development Setup**

## **1. Clone the Repository**

```bash
git clone https://github.com/aerofa45/Chatbot.git
cd Chatbot
```

---

## **2. Create and Activate a Conda Environment**

```bash
conda create -n medibot python=3.10 -y
conda activate medibot
```

---

## **3. Install Dependencies**

```bash
pip install -r requirements.txt
```

---

## **4. Add Your API Keys**

Create a `.env` file in the project root:

```ini
PINECONE_API_KEY="xxxxxxxxxxxxxxxxxxxx"
OPENAI_API_KEY="xxxxxxxxxxxxxxxxxxxx"
```

---

## **5. Upload Embeddings to Pinecone**

This stores your processed documents into your Pinecone index:

```bash
python store_index.py
```

---

## **6. Run the Flask App**

```bash
python app.py
```

Now visit:

```
http://localhost:8080
```

---

# **Tech Stack**

* **Python 3.10**
* **LangChain**
* **GPT-4o (OpenAI)**
* **Flask**
* **Pinecone Vector DB**
* **Docker**
* **AWS (ECR + EC2)**
* **GitHub Actions**

---

# **AWS Deployment with GitHub Actions (CI/CD Pipeline)**

This project includes full CI/CD automation to deploy your Dockerized chatbot to AWS.

---

# **1. Log in to AWS Console**

Make sure you have an active AWS account.

---

# **2. Create an IAM User for Deployment**

The IAM user must have programmatic access and the following AWS permissions:

### **Required Policies:**

1. `AmazonEC2FullAccess`
2. `AmazonEC2ContainerRegistryFullAccess`

### **Deployment Summary**

* Build Docker image from source code
* Push Docker image to AWS ECR
* Launch EC2 instance
* Pull latest image from ECR
* Run the container on EC2 (self-hosted GitHub runner)

---

# **3. Create an ECR Repository**

Example repository URI:

```
315865595366.dkr.ecr.us-east-1.amazonaws.com/medicalbot
```

Save this for later.

---

# **4. Launch an EC2 Instance (Ubuntu)**

Minimum recommended:
`t2.medium` or `t3.medium`

---

# **5. Install Docker on EC2**

```bash
sudo apt-get update -y
sudo apt-get upgrade -y   # optional
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker
```

---

# **6. Configure EC2 as a GitHub Self-Hosted Runner**

Go to:

```
GitHub → Repository → Settings → Actions → Runners → New self-hosted runner
```

Choose **Linux**, then run the commands provided on your EC2 machine:

```bash
./config.sh --url <repo-url> --token <token>
./run.sh
```

To run as a service:

```bash
sudo ./svc.sh install
sudo ./svc.sh start
```

---

# **7. Add GitHub Secrets**

Go to:

```
GitHub → Repo → Settings → Secrets → Actions → New Repository Secret
```

Add:

* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`
* `AWS_DEFAULT_REGION`
* `ECR_REPO`
* `PINECONE_API_KEY`
* `OPENAI_API_KEY`

These will be used inside GitHub Actions CI/CD workflow.

---


