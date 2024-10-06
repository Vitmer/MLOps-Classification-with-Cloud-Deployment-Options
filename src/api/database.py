from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from datetime import datetime
import os

# Path to the existing database located in `src/data/test.db`
DATABASE_URL = "sqlite:///./src/data/test.db"

# Setting up the connection to the existing database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Defining the table classes to interact with the existing database

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False)  # 'user' or 'admin'

    # Relationship with the logs table
    logs = relationship("Log", back_populates="user")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    image_path = Column(String, nullable=False)  # Path to the image
    designation = Column(Text, nullable=False)  # Title of the product
    description = Column(Text, nullable=False)  # Description of the product
    category = Column(String, nullable=False)  # Category of the product
    state = Column(Integer, default=0)  # State: 1 if used for training, 0 otherwise

class Log(Base):
    __tablename__ = "logs"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)  # ID of the user
    event = Column(String, nullable=False)  # Description of the event

    # Relationship with the User table
    user = relationship("User", back_populates="logs")

# Function to connect to the existing database and print a message
def connect_to_database():
    try:
        with engine.connect() as connection:
            print("Successfully connected to the existing database.")
    except Exception as e:
        print(f"Error connecting to the database: {e}")

# Function to create a new user in the database
def create_user(session: Session, username: str, hashed_password: str, role: str):
    new_user = User(username=username, password_hash=hashed_password, role=role)
    session.add(new_user)
    session.commit()
    return new_user

# Function to get a user by username
def get_user(session: Session, username: str):
    return session.query(User).filter(User.username == username).first()

# Function to log an event in the database
def log_event(session: Session, user_id: int, event: str):
    """
    Logs an event in the database.

    Args:
        session (Session): SQLAlchemy session to connect to the database.
        user_id (int): ID of the user associated with the event.
        event (str): Description of the event.

    Returns:
        Log: The created Log object.
    """
    new_log = Log(user_id=user_id, event=event)
    session.add(new_log)
    session.commit()
    print(f"Event '{event}' logged successfully.")

# New function to log the deletion of a user
def log_user_deletion(session: Session, user_id: int, username: str):
    """
    Logs the event of a user being deleted from the database.

    Args:
        session (Session): SQLAlchemy session to connect to the database.
        user_id (int): ID of the deleted user.
        username (str): Username of the deleted user.
    """
    event = f"User '{username}' with ID {user_id} was deleted"
    log_event(session, user_id, event)

# Updated function to delete a user by username with logging
def delete_user(session: Session, username: str) -> bool:
    """
    Deletes a user from the database by username and logs this action.

    Args:
        session (Session): SQLAlchemy session to connect to the database.
        username (str): Username of the user to delete.

    Returns:
        bool: True if the user was deleted, False if the user was not found.
    """
    user = get_user(session, username)
    if user:
        user_id = user.id
        # Log the deletion event before deleting the user
        log_user_deletion(session, user_id, username)

        # Удаляем все записи в таблице logs, связанные с этим пользователем
        session.query(Log).filter(Log.user_id == user_id).delete()

        # Delete the user
        session.delete(user)
        session.commit()
        print(f"User '{username}' deleted successfully.")

        return True
    else:
        print(f"User '{username}' not found.")
        return False

# Function to get all users
def get_all_users(session: Session):
    return session.query(User).all()

# Function to get untrained products
def get_untrained_products(session: Session):
    return session.query(Product).filter(Product.state == 0).all()

# Function to add a product to the database
def add_product(session: Session, image_path: str, designation: str, description: str, category: str):
    """
    Adds a new product to the database.

    Args:
        session (Session): SQLAlchemy session to connect to the database.
        image_path (str): Path to the product image.
        designation (str): Designation of the product.
        description (str): Description of the product.
        category (str): Category of the product.

    Returns:
        Product: The created Product object.
    """
    new_product = Product(
        image_path=image_path,
        designation=designation,
        description=description,
        category=category,
        state=0  # Default state is 0 (not trained)
    )
    session.add(new_product)
    session.commit()
    print(f"Product '{designation}' added successfully.")
    return new_product

# Function to update the state of a product
def update_product_state(session: Session, product_id: int, new_state: int):
    product = session.query(Product).filter(Product.id == product_id).first()
    if product:
        product.state = new_state
        session.commit()
        print(f"Product ID: {product_id} updated to state: {new_state}")
    else:
        print(f"Product ID: {product_id} not found.")

# Function to create all tables in the database
def create_tables():
    Base.metadata.create_all(bind=engine)

# Function to get all logs
def get_all_logs(session: Session):
    return session.query(Log).all()

# Function to check if the database is available
def is_database_available() -> bool:
    """
    Checks if the database is available and can be connected to.

    Returns:
        bool: True if the database is available, False otherwise.
    """
    try:
        with engine.connect() as connection:
            return True
    except Exception:
        return False