
# MLOps Classification with Cloud Deployment Options

This project, **MLOps Classification with Cloud Deployment Options**, builds on the principles of MLOps by integrating options for cloud deployment. The enhanced architecture ensures scalability, cost-effectiveness, and performance monitoring, with deployment options across platforms like AWS, GCP, and Azure.

---

## **Project Features**

- **Data Processing**: 
  Includes scripts for preprocessing and balancing data, such as text data (using TF-IDF) and image features.
- **Modular Architecture**: 
  The system's modularity enables easy updates and extensions without affecting the core functionality.
- **Automated Model Training and Retraining**: 
  Fully supports the automation of training and retraining processes with API integration.
- **Cloud Deployment Options**: 
  Provides deployment strategies for AWS, GCP, and Azure, leveraging serverless technologies and cloud-native tools.
- **CI/CD Integration**: 
  Uses Docker and Kubernetes for seamless CI/CD pipelines, ensuring rapid deployment and updates.
- **Monitoring and Logging**: 
  Incorporates Prometheus and Grafana for on-premise monitoring, with extensions for cloud monitoring tools like AWS CloudWatch and GCP Operations Suite.
- **Scalability**: 
  Supports horizontal scaling using container orchestration or serverless triggers.
- **Testing**: 
  Includes unit tests for stability and reliability across all components.

---

## **Cloud Deployment Architecture**

The project supports deployment on multiple cloud platforms, ensuring flexibility and robustness in various environments.

### **AWS Deployment**
1. **Compute**: AWS Lambda for serverless execution of model inference and retraining tasks.
2. **Storage**: Amazon S3 for storing datasets, models, and logs.
3. **API Management**: API Gateway for serving API requests.
4. **Monitoring**: AWS CloudWatch for logging and real-time performance metrics.

### **GCP Deployment**
1. **Compute**: Google Cloud Functions or Vertex AI for handling ML workloads.
2. **Storage**: Google Cloud Storage for persistent storage.
3. **API Management**: Google API Gateway for external API interaction.
4. **Monitoring**: Google Cloud Operations Suite for tracking performance and errors.

### **Azure Deployment**
1. **Compute**: Azure Functions for running inference and retraining tasks.
2. **Storage**: Azure Blob Storage for managing datasets and models.
3. **API Management**: Azure API Management for managing API endpoints.
4. **Monitoring**: Azure Monitor for tracking system health and performance.

---

## **Project Structure**

```plaintext
├── src
│   ├── api
│   │   ├── main.py             # Main API file for managing training and inference
│   │   ├── retrain_model.py    # Logic for model retraining
│   │   ├── util_auth.py        # Authentication utilities
│   │   ├── util_model.py       # Helper functions for model operations
├── data
│   ├── train_image_features_balanced.npy    # Image features for training
│   ├── X_train_tfidf_balanced.npy           # TF-IDF vectors for text data
│   ├── Y_train_balanced.npy                 # Labels for training data
├── tests
│   ├── test_main.py             # Unit tests for the main API
│   ├── test_retrain_model.py    # Unit tests for model retraining
│   ├── test_util_auth.py        # Unit tests for authentication utilities
│   ├── test_util_model.py       # Unit tests for model helpers
├── Dockerfile                   # Docker file for building the container
├── docker-compose.yml           # Docker Compose configuration
├── prometheus.yml               # Prometheus configuration
├── grafana.ini                  # Grafana configuration
```

---

## **How to Deploy**

### **1. On-Premise**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/MLOps-Classification.git
   ```
2. Build and run the application using Docker Compose:
   ```bash
   docker-compose up --build
   ```
3. Access Prometheus and Grafana for monitoring.

### **2. Cloud Deployment**
#### **AWS Example**
1. Upload the pre-trained model to S3:
   ```bash
   aws s3 cp model.pkl s3://your-bucket-name/
   ```
2. Package and deploy Lambda functions for inference and retraining:
   ```bash
   zip -r inference_function.zip inference_function.py
   aws lambda create-function        --function-name InferenceFunction        --runtime python3.9        --handler inference_function.lambda_handler        --code S3Bucket=your-bucket-name,S3Key=inference_function.zip        --role arn:aws:iam::your-role-arn
   ```
3. Configure API Gateway for external access.

---

## **Logging and Monitoring**

- **Prometheus and Grafana**: For on-premise deployments, use these tools to monitor performance and visualize metrics.
- **Cloud Monitoring**:
  - **AWS**: Use CloudWatch for logs and performance metrics.
  - **GCP**: Use Operations Suite for comprehensive insights.
  - **Azure**: Use Azure Monitor for system health tracking.

---

## **API Endpoints**
- `/train`: Train the model with existing data.
- `/retrain`: Retrain the model with new data.
- `/predict`: Make predictions using the deployed model.

### **Example Usage**
To train the model:
```bash
curl -X POST http://localhost:8000/train -H "Authorization: Bearer <your-token>"
```

---

## **Testing**
Run tests to ensure the stability of the application:
```bash
python -m unittest discover -s tests
```

---

## **Development and CI/CD**
- **Containerization**: Docker is used to containerize all components for consistent deployments.
- **CI/CD Pipelines**: Ensure seamless updates and testing for deployments.
- **Cloud Readiness**: The project is designed to be easily deployable in any cloud environment.

---

## **License**
This project is licensed under the MIT License.
