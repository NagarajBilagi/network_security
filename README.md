# 🛡️ Phishing Website Detection – End-to-End MLOps Project

## 📌 Project Overview


This project showcases an end-to-end Machine Learning pipeline for phishing website detection.

It implements a modular ML architecture and applies MLOps practices including automated CI/CD workflows, Docker containerization, and deployment on AWS cloud infrastructure.

The system includes:
- Structured ML pipeline architecture
- CI/CD automation with GitHub Actions
- Docker containerization
- AWS cloud deployment (ECR + EC2)
- FastAPI inference API with interactive documentation

---

## 🏗️ System Architecture
```

├── src/
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   ├── model_trainer.py
│   │   └── model_evaluation.py
│   ├── pipeline/
│   └── utils/
├── app.py
├── Dockerfile
├── .github/workflows/
├── requirements.txt
└── README.md
```



---

## 🧠 Machine Learning Pipeline

The project follows a modular ML pipeline structure:

### 1️⃣ Data Ingestion
- Retrieves phishing website dataset from MongoDB
- Splits into train/test sets
- Stores artifacts in structured directories

### 2️⃣ Data Validation
- Schema validation
- Data type verification
- Missing value checks

### 3️⃣ Data Transformation
- Feature engineering
- Scaling and preprocessing
- Pipeline object creation

### 4️⃣ Model Trainer and Evaluation
- Model training & Model selection
- Performance metric calculation
- Model validation before deployment

---

## ⚙️ Tech Stack

- **Python**
- **Scikit-learn**
- **Pandas & NumPy**
- **FastAPI**
- **Docker**
- **GitHub Actions (CI/CD)**
- **AWS ECR**
- **AWS EC2**

---

## 🚀 CI/CD & Deployment Workflow

### 🔹 Continuous Integration
- Triggered on GitHub push
- Automated Docker image build
- Image pushed to AWS ECR

### 🔹 Containerization
- Application packaged using Docker
- Ensures reproducible environments

### 🔹 Cloud Deployment
- Docker image stored in AWS ECR
- Pulled and deployed on AWS EC2 instance
- FastAPI application exposed as a web service

---

## 📊 API Interface

FastAPI provides:
- Interactive Swagger UI at `/docs`
- REST API endpoint for predictions

