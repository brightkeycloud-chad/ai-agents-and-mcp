"""
Secure Flask Application - Best Practices Implementation
Demonstrates proper security practices following CLAUDE.md rules
"""

from flask import Flask, request, jsonify
import sqlite3
import os
import logging
from dotenv import load_dotenv
from functools import wraps
import secrets
from typing import Optional, Dict, Any, Tuple
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Load environment variables from .env file
load_dotenv()

# Configure structured logging (LOGGING rule)
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(pathname)s:%(lineno)d'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# SECURITY: Load configuration from environment variables (NO_SECRETS_IN_CODE, CONFIG_MANAGEMENT)
API_KEY = os.getenv('API_KEY')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'users.db')
EMAIL_SERVICE_URL = os.getenv('EMAIL_SERVICE_URL', 'https://api.emailservice.com/send')

# Validate required environment variables
if not all([API_KEY, DB_USER, DB_PASS]):
    logger.error("Missing required environment variables: API_KEY, DB_USER, DB_PASS")
    raise ValueError("Missing required environment variables. Check .env file.")

# Configure Flask security settings
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(32))
app.config['SESSION_COOKIE_SECURE'] = os.getenv('SESSION_COOKIE_SECURE', 'True') == 'True'
app.config['SESSION_COOKIE_HTTPONLY'] = os.getenv('SESSION_COOKIE_HTTPONLY', 'True') == 'True'
app.config['SESSION_COOKIE_SAMESITE'] = os.getenv('SESSION_COOKIE_SAMESITE', 'Lax')


def get_db_connection() -> sqlite3.Connection:
    """
    Get database connection with proper configuration.

    Returns:
        sqlite3.Connection: Database connection object

    Raises:
        sqlite3.Error: If connection fails

    Note:
        Connection should be closed by caller using context manager or explicit close()
    """
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        logger.debug(f"Database connection established to {DB_NAME}")
        return conn
    except sqlite3.Error as e:
        logger.error(f"Failed to connect to database {DB_NAME}: {str(e)}")
        raise


def require_auth(f):
    """
    Decorator to require authentication for protected endpoints.

    This is a simplified example - in production, use proper authentication
    frameworks like Flask-Login, Flask-JWT-Extended, etc.

    Args:
        f: Function to wrap

    Returns:
        Wrapped function that checks authentication
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = request.headers.get('Authorization')

        if not auth_token:
            logger.warning(f"Unauthorized access attempt to {request.path}")
            return jsonify({"error": "Authentication required"}), 401

        # In production, validate token against database/JWT/session
        # This is simplified for demonstration
        if not auth_token.startswith('Bearer '):
            logger.warning(f"Invalid authorization format from {request.remote_addr}")
            return jsonify({"error": "Invalid authentication format"}), 401

        return f(*args, **kwargs)
    return decorated_function


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id: int) -> Tuple[Dict[str, Any], int]:
    """
    Get user by ID with proper security controls.

    SECURITY IMPROVEMENTS from vulnerable version:
    - Uses parameterized query to prevent SQL injection (INPUT_VALIDATION)
    - Comprehensive error handling (ERROR_HANDLING)
    - Structured logging (LOGGING)
    - Returns JSON instead of raw string (API best practice)
    - Does not expose sensitive data (passwords, etc.)

    Args:
        user_id (int): User ID to retrieve (Flask converts and validates)

    Returns:
        Tuple[Dict, int]: JSON response and HTTP status code

    Example:
        >>> GET /users/123
        {"id": 123, "username": "john_doe", "email": "john@example.com"}
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # SECURITY: Parameterized query prevents SQL injection
            cursor.execute(
                "SELECT id, username, email FROM users WHERE id = ?",
                (user_id,)
            )

            user = cursor.fetchone()

            if user:
                logger.info(f"User {user_id} retrieved successfully")
                return jsonify({
                    "id": user['id'],
                    "username": user['username'],
                    "email": user['email']
                }), 200
            else:
                logger.warning(f"User {user_id} not found")
                return jsonify({"error": "User not found"}), 404

    except sqlite3.Error as e:
        # CONTEXT_IN_ERRORS: Include operation details without exposing sensitive data
        logger.error(f"Database error retrieving user {user_id}: {str(e)}")
        return jsonify({"error": "Database error occurred"}), 500

    except Exception as e:
        logger.error(f"Unexpected error retrieving user {user_id}: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@app.route('/login', methods=['POST'])
def login() -> Tuple[Dict[str, Any], int]:
    """
    Login endpoint with secure password handling.

    SECURITY IMPROVEMENTS from vulnerable version:
    - Uses parameterized queries (INPUT_VALIDATION)
    - Passwords verified using secure hashing (DATA_ENCRYPTION)
    - Input validation (ERROR_HANDLING)
    - Rate limiting should be added in production (RATE_LIMITING)

    Args:
        JSON body with 'username' and 'password' fields

    Returns:
        Tuple[Dict, int]: JSON response and HTTP status code

    Example:
        >>> POST /login
        >>> {"username": "john_doe", "password": "SecurePass123!"}
        {"success": true, "message": "Login successful", "token": "..."}
    """
    try:
        # Validate input
        if not request.is_json:
            logger.warning("Login attempt with non-JSON content type")
            return jsonify({"error": "Content-Type must be application/json"}), 400

        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Input validation
        if not username or not password:
            logger.warning(f"Login attempt with missing credentials from {request.remote_addr}")
            return jsonify({"error": "Username and password required"}), 400

        if len(username) > 100 or len(password) > 200:
            logger.warning(f"Login attempt with oversized input from {request.remote_addr}")
            return jsonify({"error": "Invalid input length"}), 400

        with get_db_connection() as conn:
            cursor = conn.cursor()

            # SECURITY: Parameterized query prevents SQL injection
            cursor.execute(
                "SELECT id, username, password_hash FROM users WHERE username = ?",
                (username,)
            )

            user = cursor.fetchone()

            if user:
                # Import here to allow utils.py to use proper password verification
                from utils import verify_password

                # SECURITY: Verify password using secure hashing
                if verify_password(user['password_hash'], password):
                    logger.info(f"Successful login for user {user['username']}")

                    # In production, generate actual JWT or session token
                    token = secrets.token_urlsafe(32)

                    return jsonify({
                        "success": True,
                        "message": "Login successful",
                        "token": token
                    }), 200
                else:
                    logger.warning(f"Failed login attempt for user {username} - invalid password")
                    return jsonify({"error": "Invalid credentials"}), 401
            else:
                # Use same message as wrong password to prevent user enumeration
                logger.warning(f"Failed login attempt for non-existent user {username}")
                return jsonify({"error": "Invalid credentials"}), 401

    except sqlite3.Error as e:
        logger.error(f"Database error during login: {str(e)}")
        return jsonify({"error": "Database error occurred"}), 500

    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@app.route('/search', methods=['GET'])
def search() -> Tuple[Dict[str, Any], int]:
    """
    Search users with proper input validation and SQL injection protection.

    SECURITY IMPROVEMENTS from vulnerable version:
    - Parameterized query prevents SQL injection (INPUT_VALIDATION)
    - Input validation and sanitization
    - Rate limiting should be added in production

    Args:
        Query parameter 'q': Search term

    Returns:
        Tuple[Dict, int]: JSON response with search results and HTTP status code

    Example:
        >>> GET /search?q=john
        {"results": [{"id": 1, "username": "john_doe", "email": "john@example.com"}]}
    """
    try:
        search_term = request.args.get('q', '').strip()

        # Input validation
        if not search_term:
            logger.warning("Search attempted with empty query")
            return jsonify({"error": "Search term required"}), 400

        if len(search_term) > 100:
            logger.warning(f"Search attempted with oversized query from {request.remote_addr}")
            return jsonify({"error": "Search term too long"}), 400

        # Additional validation: alphanumeric and common characters only
        import re
        if not re.match(r'^[a-zA-Z0-9\s\-_.@]+$', search_term):
            logger.warning(f"Search attempted with invalid characters: {search_term}")
            return jsonify({"error": "Invalid characters in search term"}), 400

        with get_db_connection() as conn:
            cursor = conn.cursor()

            # SECURITY: Parameterized query prevents SQL injection
            # Use LIKE with proper escaping
            cursor.execute(
                "SELECT id, username, email FROM users WHERE username LIKE ? OR email LIKE ?",
                (f'%{search_term}%', f'%{search_term}%')
            )

            results = cursor.fetchall()

            logger.info(f"Search for '{search_term}' returned {len(results)} results")

            return jsonify({
                "results": [
                    {"id": row['id'], "username": row['username'], "email": row['email']}
                    for row in results
                ]
            }), 200

    except sqlite3.Error as e:
        logger.error(f"Database error during search: {str(e)}")
        return jsonify({"error": "Database error occurred"}), 500

    except Exception as e:
        logger.error(f"Unexpected error during search: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


@app.route('/admin/delete/<int:user_id>', methods=['DELETE'])
@require_auth  # SECURITY: Require authentication (LEAST_PRIVILEGE)
def delete_user(user_id: int) -> Tuple[Dict[str, Any], int]:
    """
    Delete user with proper authentication and authorization.

    SECURITY IMPROVEMENTS from vulnerable version:
    - Requires authentication (LEAST_PRIVILEGE)
    - Parameterized query prevents SQL injection
    - Proper HTTP method (DELETE instead of GET)
    - Authorization check (simplified for demo)

    Args:
        user_id (int): ID of user to delete

    Returns:
        Tuple[Dict, int]: JSON response and HTTP status code

    Example:
        >>> DELETE /admin/delete/123
        >>> Headers: Authorization: Bearer <token>
        {"success": true, "message": "User deleted"}
    """
    try:
        # In production, verify user has admin role
        # This is simplified for demonstration

        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Check if user exists first
            cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()

            if not user:
                logger.warning(f"Attempted to delete non-existent user {user_id}")
                return jsonify({"error": "User not found"}), 404

            # SECURITY: Parameterized query prevents SQL injection
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()

            logger.info(f"User {user_id} deleted successfully")
            return jsonify({
                "success": True,
                "message": "User deleted"
            }), 200

    except sqlite3.Error as e:
        logger.error(f"Database error deleting user {user_id}: {str(e)}")
        return jsonify({"error": "Database error occurred"}), 500

    except Exception as e:
        logger.error(f"Unexpected error deleting user {user_id}: {str(e)}", exc_info=True)
        return jsonify({"error": "Internal server error"}), 500


def send_email(recipient: str, subject: str, body: str) -> Dict[str, Any]:
    """
    Send email using external API with proper error handling and security.

    SECURITY IMPROVEMENTS from vulnerable version:
    - Uses environment variable for API key (NO_SECRETS_IN_CODE)
    - Comprehensive error handling with timeouts (ERROR_HANDLING)
    - Retry logic for transient failures
    - Input validation

    Args:
        recipient (str): Email address of recipient
        subject (str): Email subject
        body (str): Email body content

    Returns:
        Dict[str, Any]: Response from email service

    Raises:
        ValueError: If inputs are invalid
        requests.RequestException: If email sending fails after retries

    Example:
        >>> send_email("user@example.com", "Welcome", "Welcome to our service!")
        {"success": true, "message_id": "abc123"}
    """
    # Input validation
    if not all([recipient, subject, body]):
        raise ValueError("recipient, subject, and body are required")

    import re
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, recipient):
        raise ValueError(f"Invalid email address: {recipient}")

    # SECURITY: Use environment variable for API key
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        'to': recipient,
        'subject': subject,
        'body': body
    }

    # Configure retry strategy for transient failures
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"]
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)

    try:
        # SECURITY: Include timeout to prevent hanging (ERROR_HANDLING)
        response = session.post(
            EMAIL_SERVICE_URL,
            headers=headers,
            json=data,
            timeout=10  # 10 second timeout
        )

        response.raise_for_status()  # Raise exception for 4xx/5xx responses

        logger.info(f"Email sent successfully to {recipient}")
        return response.json()

    except requests.Timeout as e:
        logger.error(f"Timeout sending email to {recipient}: {str(e)}")
        raise

    except requests.ConnectionError as e:
        logger.error(f"Connection error sending email to {recipient}: {str(e)}")
        raise

    except requests.HTTPError as e:
        logger.error(f"HTTP error sending email to {recipient}: {response.status_code} - {str(e)}")
        raise

    except requests.RequestException as e:
        logger.error(f"Unexpected error sending email to {recipient}: {str(e)}")
        raise

    finally:
        session.close()


@app.route('/health', methods=['GET'])
def health_check() -> Tuple[Dict[str, Any], int]:
    """
    Health check endpoint for monitoring (HEALTH_CHECKS rule).

    Returns:
        Tuple[Dict, int]: Health status and HTTP status code

    Example:
        >>> GET /health
        {"status": "healthy", "database": "connected"}
    """
    try:
        # Check database connectivity
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()

        return jsonify({
            "status": "healthy",
            "database": "connected"
        }), 200

    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }), 503


if __name__ == '__main__':
    # SECURITY: Use secure defaults (no debug in production, localhost only)
    flask_env = os.getenv('FLASK_ENV', 'production')
    flask_debug = os.getenv('FLASK_DEBUG', 'False') == 'True'
    flask_host = os.getenv('FLASK_HOST', '127.0.0.1')  # Localhost only by default
    flask_port = int(os.getenv('FLASK_PORT', '5000'))

    if flask_env == 'production' and flask_debug:
        logger.warning("Debug mode should not be enabled in production!")

    logger.info(f"Starting Flask application on {flask_host}:{flask_port} (env: {flask_env})")

    app.run(
        debug=flask_debug,
        host=flask_host,
        port=flask_port
    )
