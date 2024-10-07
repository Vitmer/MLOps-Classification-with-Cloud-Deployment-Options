import time
from fastapi import FastAPI, UploadFile, File, Form, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from joblib import load as joblib_load
from tensorflow.keras.models import load_model
from PIL import Image
from io import BytesIO
import os
import numpy as np
from sqlalchemy.orm import Session
from uuid import uuid4
import requests  # Импортируем библиотеку для HTTP-запросов

from src.api.util_model import predict_classification, train_model_on_new_data, evaluate_model_on_untrained_data
from src.api.util_auth import create_access_token, verify_password, get_password_hash, verify_access_token, admin_required
from src.api.database import create_user, get_user, add_product, SessionLocal, User, create_tables, delete_user, log_event, get_all_logs, is_database_available

# Load vectorizer and model globally when the app starts
vectorizer_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'Tfidf_Vectorizer.joblib')
model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'retrained_balanced_model.keras')

vectorizer = joblib_load(vectorizer_path)
model = load_model(model_path)

# Define the upload directory for images
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'Img')  # Путь к папке для изображений

# Dependency to get a session from the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize OAuth2PasswordBearer to extract access token from the Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI()

# Initialize database when the app starts
@app.on_event("startup")
def on_startup():
    while not is_database_available():
        print("Waiting for the database to become available...")
        time.sleep(5)  # Wait for 5 seconds before retrying
    create_tables()

# Endpoint to retrieve metrics from Prometheus
@app.get("/metrics")
async def get_prometheus_metrics(request: Request):
    """Retrieve metrics from Prometheus."""
    prometheus_url = "http://localhost:9090/api/v1/query"
    query = 'sum(rate(http_requests_total[5m]))'

    try:
        response = requests.get(prometheus_url, params={'query': query})
        response.raise_for_status()  # Проверяем наличие ошибок HTTP

        result = response.json()
        return {"metrics": result}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve metrics: {e}")

# Updated signup function to assign admin role to the first user
@app.post("/signup")
async def signup(username: str, password: str, db: Session = Depends(get_db)):
    existing_user = get_user(db, username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    users_exist = db.query(User).count() > 0
    role = 'admin' if not users_exist else 'user'

    hashed_password = get_password_hash(password)
    new_user = create_user(db, username, hashed_password, role)
    log_event(db, new_user.id, f"User {username} signed up ")

    return {"message": f"User created successfully with role: {role}"}

# User authentication and token generation
@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})
    log_event(db, user.id, f"User {user.username} logged in")
    return {"access_token": token, "token_type": "bearer"}

# Product category prediction endpoint
@app.post("/predict")
async def predict_category(
    token: str = Depends(oauth2_scheme),
    designation: str = Form(...),
    description: str = Form(...),
    file: UploadFile = File(...),
):
    user_info = verify_access_token(token)
    if not user_info:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token or user not authenticated")
    
    image_data = await file.read()
    image = Image.open(BytesIO(image_data))

    predicted_result = predict_classification(model, vectorizer, designation, description, image)
    predicted_class = int(predicted_result['predicted_class'][0])
    confidence = float(predicted_result['confidence'][0])

    return {
        "predicted_class": predicted_class,
        "confidence": confidence
    }

# Admin-only route
@app.get("/admin-only")
@admin_required()
async def admin_route(
    request: Request,
    session: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    return {"message": "Welcome, admin!"}

# Endpoint to add new product data
@app.post("/add-product-data", operation_id="add_product_data")
@admin_required()
async def add_product_api(
    request: Request,
    session: Session = Depends(get_db),
    image: UploadFile = File(...),
    designation: str = Form(...),
    description: str = Form(...),
    category: str = Form(...),
    token: str = Depends(oauth2_scheme)
):
    file_extension = os.path.splitext(image.filename)[1]
    image_filename = f"{uuid4()}{file_extension}"
    image_path = os.path.join(UPLOAD_DIR, image_filename)

    try:
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        with open(image_path, "wb") as f:
            f.write(await image.read())
        
        add_product(session, image_path, designation, description, category)

        return {"message": "Product added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving product: {str(e)}")
    
# Endpoint to evaluate the model on untrained data
@app.get("/evaluate", operation_id="evaluate_model")
@admin_required()
async def evaluate_model_endpoint(
    request: Request,
    session: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    try:
        f1, report = evaluate_model_on_untrained_data(model, vectorizer, session)
        return {"f1_score": f1, "classification_report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")

# Endpoint to train the model on new data
@app.get("/train", operation_id="train_model")
@admin_required()
async def train_model_endpoint(
    request: Request,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    try:
        f1, report = train_model_on_new_data(model, vectorizer, db)
        return {"f1_score": f1, "classification_report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

# Admin-only route to return all logs
@app.get("/admin/logs", operation_id="admin_get_logs")
@admin_required()
async def get_logs(
    request: Request,
    session: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    logs = get_all_logs(session)
    
    log_list = [
        {
            "id": log.id,
            "timestamp": log.timestamp,
            "user_id": log.user_id,
            "event": log.event
        } for log in logs
    ]
    
    return {"logs": log_list}

# Admin-only route to delete a user by username
@app.delete("/delete-user/{username}", operation_id="delete_user")
@admin_required()
async def delete_user_by_admin(
    request: Request,
    username: str,
    session: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
):
    result = delete_user(session, username)
    if result:
        return {"message": f"User '{username}' deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail="User not found")