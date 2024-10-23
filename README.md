
# MLOps-CLASSIFICATION

**MLOps-CLASSIFICATION** is a project designed to automate and manage the full lifecycle of machine learning (ML) model development, training, deployment, and monitoring, following MLOps principles.

## Project Features

- **Data Processing**: The project includes scripts for preprocessing and balancing data, such as text and image data, using TF-IDF for text and feature extraction for images.
- **Modular Architecture**: The code is organized modularly, allowing easy modification of individual components without affecting others.
- **Automated Model Training**: A mechanism is included for automatic model training and retraining with the ability to manage via API.
- **CI/CD**: The use of Docker and Kubernetes for building and deploying models allows automatic updates when data changes or architecture is improved.
- **Monitoring and Logging**: Prometheus and Grafana are used to monitor the model's performance in real-time.
- **Testing**: The project includes unit tests for all major components, ensuring stability and correctness at every stage of development.

## Project Structure

```plaintext
├── src
│   ├── api
│   │   ├── main.py             # Main API file for managing model training and retraining
│   │   ├── retrain_model.py    # Logic for retraining models
│   │   ├── util_auth.py        # Authentication and access management
│   │   ├── util_model.py       # Helper functions for model operations
├── data
│   ├── train_image_features_balanced.npy    # Image features for training data
│   ├── X_train_tfidf_balanced.npy           # TF-IDF vectors for text data
│   ├── Y_train_balanced.npy                 # Labels for training data
├── tests
│   ├── test_main.py             # Unit tests for the main API
│   ├── test_retrain_model.py    # Unit tests for retraining models
│   ├── test_util_auth.py        # Unit tests for authentication
│   ├── test_util_model.py       # Unit tests for model helper functions
├── Dockerfile                   # Docker file for deploying the application
├── docker-compose.yml           # Docker Compose configuration
├── prometheus.yml               # Prometheus configuration for monitoring
├── grafana.ini                  # Grafana configuration for monitoring
```

## How to Run the Project

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/MLOps-CLASSIFICATION.git
    ```

2. Build the Docker container:
    ```bash
    docker-compose up --build
    ```

3. Set up Prometheus and Grafana for monitoring the model's performance.

## API

The project provides an API for interacting with models:

- **/train**: Train the model using the provided data.
- **/retrain**: Retrain the existing model with new data.
- **/predict**: Make predictions using the model on new data.

## Example API Usage

To train the model, use the following request:

```bash
curl -X POST http://localhost:8000/train -H "Authorization: Bearer <your-token>"
```

## Logging and Monitoring

- **Prometheus**: Tracks model metrics such as accuracy, loss, and other parameters.
- **Grafana**: Provides real-time visualization of data through customizable dashboards.

## Testing

To run the tests, execute:

```bash
python -m unittest discover -s tests
```

## Development

- **Containerization**: All application components are containerized for easy setup and deployment.
- **CI/CD**: The project uses CI/CD tools for automatic testing and deployment.
- **Monitoring**: Tools for performance tracking and logging are set up.

## License

This project is licensed under the MIT License.
