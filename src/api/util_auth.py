from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, Depends, Request
from sqlalchemy.orm import Session
from functools import wraps

from src.api.database import get_user, SessionLocal

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key and algorithm used for JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"

# Utility function to hash a password
def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt algorithm.

    Args:
        password (str): Plain text password.

    Returns:
        str: Hashed password.
    """
    return pwd_context.hash(password)

# Utility function to verify a password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain text password against a hashed password.

    Args:
        plain_password (str): Plain text password.
        hashed_password (str): Hashed password stored in the database.

    Returns:
        bool: True if passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)

# Function to create a JWT token
def create_access_token(data: dict) -> str:
    """
    Create a JWT access token.

    Args:
        data (dict): Dictionary containing the data to include in the token (e.g., username).

    Returns:
        str: Encoded JWT token as a string.
    """
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

# Function to verify a JWT token
def verify_access_token(token: str) -> dict:
    """
    Verify a JWT access token.

    Args:
        token (str): JWT token to decode and verify.

    Returns:
        dict: Decoded token data containing the username.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return {"username": username}
    except JWTError:
        return None

# Dependency function to get a database session
def get_db():
    """
    Provide a database session dependency for FastAPI routes.

    Yields:
        Session: SQLAlchemy session connected to the database.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Decorator to require admin privileges
def admin_required():
    """
    Decorator to restrict access to a route to admin users only.

    Returns:
        decorator: Wrapped function with admin check.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, session: Session = Depends(get_db), *args, **kwargs):
            # Get the Authorization header and extract the Bearer token
            token = request.headers.get("Authorization")
            if not token or not token.startswith("Bearer "):
                raise HTTPException(status_code=403, detail="Not authenticated")

            token = token[len("Bearer "):]  # Remove "Bearer " prefix

            try:
                # Decode the JWT token
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                username: str = payload.get("sub")

                if username is None:
                    raise HTTPException(status_code=403, detail="Invalid token")

                # Get the user from the database
                user = get_user(session, username)
                if not user:
                    raise HTTPException(status_code=403, detail="User not found")

                # Check if the user is an admin
                if user.role != "admin":
                    raise HTTPException(status_code=403, detail="Not authorized")

            except JWTError as e:
                raise HTTPException(status_code=403, detail=f"Authentication error: {str(e)}")

            # If everything is fine, call the original function
            return await func(request, session=session, *args, **kwargs)

        return wrapper

    return decorator

# Example usage (for testing purposes only)
if __name__ == "__main__":
    # 1. Hash a password
    password = "my_secure_password"
    hashed_password = get_password_hash(password)
    print(f"Original Password: {password}")
    print(f"Hashed Password: {hashed_password}")

    # 2. Verify the hashed password
    is_verified = verify_password("my_secure_password", hashed_password)
    print(f"Password Verified: {is_verified}")  # Should print: True

    # 3. Test with an incorrect password
    is_verified_incorrect = verify_password("wrong_password", hashed_password)
    print(f"Password Verified (incorrect): {is_verified_incorrect}")  # Should print: False

    # 4. Create a JWT access token
    token_data = {"sub": "user@example.com"}
    access_token = create_access_token(token_data)
    print(f"Access Token: {access_token}")

    # 5. Decode the token (for testing purposes)
    try:
        decoded_data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"Decoded Token Data: {decoded_data}")
    except JWTError as e:
        print(f"Error decoding token: {str(e)}")