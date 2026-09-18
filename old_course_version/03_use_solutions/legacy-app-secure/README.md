# Legacy Application - SECURE VERSION ✅

## Overview

This is the **secure, production-ready** version of the legacy application, refactored to follow CLAUDE.md development rules and security best practices.

This version demonstrates how to properly implement:
- Secure credential management
- Input validation and SQL injection prevention
- Password hashing and authentication
- Error handling and structured logging
- Health checks and monitoring
- Principle of least privilege

---

## Key Security Improvements

### ✅ CRITICAL Fixes

| Vulnerability | Vulnerable Version | This Version | CLAUDE.md Rule |
|---------------|-------------------|--------------|----------------|
| **Hardcoded Secrets** | API keys in code | Environment variables | NO_SECRETS_IN_CODE |
| **SQL Injection** | String concatenation | Parameterized queries | INPUT_VALIDATION |
| **Password Storage** | Plain text/MD5 | Argon2 hashing | DATA_ENCRYPTION |
| **No Authentication** | Anyone can delete users | Required auth | LEAST_PRIVILEGE |
| **No Error Handling** | Crashes expose details | Try-catch blocks | ERROR_HANDLING |
| **Poor Logging** | Plain text to `/tmp` | Structured logging | LOGGING |

---

## Installation & Setup

### Prerequisites
- Python 3.9+
- pip package manager
- Virtual environment (recommended)

### Installation Steps

1. **Create virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   # Copy example environment file
   cp .env.example .env

   # Edit .env with your actual values
   nano .env  # or use your preferred editor
   ```

   **Required environment variables:**
   ```bash
   API_KEY=your_api_key_here
   DB_USER=your_database_user
   DB_PASS=your_database_password
   SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
   ```

4. **Initialize database:**
   ```bash
   python init_db.py  # Create schema and sample data
   ```

5. **Run the application:**
   ```bash
   # Development
   python app.py

   # Production (use WSGI server)
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

---

## Architecture & Security Design

### Environment-Based Configuration (CONFIG_MANAGEMENT)

**Problem:** Hardcoded credentials expose secrets in source code and version control.

**Solution:**
```python
# ✅ Secure - loads from environment
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('API_KEY')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

# Validate required variables
if not all([API_KEY, DB_USER, DB_PASS]):
    raise ValueError("Missing required environment variables")
```

**Files:** app.py:27-32, .env.example

---

### Parameterized Queries (INPUT_VALIDATION)

**Problem:** String concatenation in SQL queries allows SQL injection attacks.

**Solution:**
```python
# ✅ Secure - parameterized query
cursor.execute(
    "SELECT * FROM users WHERE id = ?",
    (user_id,)
)

# ❌ Vulnerable - string concatenation
query = "SELECT * FROM users WHERE id = " + id  # DON'T DO THIS!
```

**Files:** app.py:112-116, models.py:99-106

---

### Secure Password Hashing (DATA_ENCRYPTION)

**Problem:** Plain text or MD5 passwords are easily compromised.

**Solution:**
```python
# ✅ Secure - Argon2 hashing
from argon2 import PasswordHasher

ph = PasswordHasher()
password_hash = ph.hash(plain_password)
verified = ph.verify(password_hash, plain_password)
```

**Why Argon2?**
- Winner of Password Hashing Competition 2015
- Resistant to GPU/ASIC attacks
- Memory-hard algorithm
- Configurable work factors

**Files:** utils.py:27-56, models.py:93-101

---

### Authentication & Authorization (LEAST_PRIVILEGE)

**Problem:** No authentication allows anyone to perform privileged operations.

**Solution:**
```python
# ✅ Secure - require authentication
@app.route('/admin/delete/<int:user_id>', methods=['DELETE'])
@require_auth  # Decorator ensures user is authenticated
def delete_user(user_id: int):
    # In production, also check user role/permissions
    ...
```

**Files:** app.py:83-100, app.py:284-325

---

### Comprehensive Error Handling (ERROR_HANDLING, CONTEXT_IN_ERRORS)

**Problem:** Unhandled errors expose stack traces and internal details.

**Solution:**
```python
# ✅ Secure - comprehensive error handling
try:
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()

        if user:
            logger.info(f"User {user_id} retrieved successfully")
            return jsonify({...}), 200
        else:
            logger.warning(f"User {user_id} not found")
            return jsonify({"error": "User not found"}), 404

except sqlite3.Error as e:
    logger.error(f"Database error retrieving user {user_id}: {str(e)}")
    return jsonify({"error": "Database error occurred"}), 500

except Exception as e:
    logger.error(f"Unexpected error retrieving user {user_id}: {str(e)}", exc_info=True)
    return jsonify({"error": "Internal server error"}), 500
```

**Files:** app.py:104-147, models.py:96-145

---

### Structured Logging (LOGGING)

**Problem:** Plain text logs to world-readable files leak sensitive data.

**Solution:**
```python
# ✅ Secure - structured logging
import logging

logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Log with appropriate levels and context
logger.info(f"User {user_id} retrieved successfully")
logger.warning(f"Failed login attempt for user {username}")
logger.error(f"Database error: {str(e)}")
```

**Files:** app.py:23-26, utils.py:17

---

### AWS Credentials via IAM Roles (TEMPORARY_CREDENTIALS)

**Problem:** Hardcoded AWS credentials in source code.

**Solution:**
```python
# ✅ Secure - uses boto3 credential chain
def connect_to_s3(region: Optional[str] = None):
    """
    Connect to S3 using AWS credential chain:
    1. IAM role (most secure - recommended)
    2. Environment variables
    3. ~/.aws/credentials file
    """
    s3_client = boto3.client('s3', region_name=region)
    return s3_client
```

**Files:** utils.py:206-249

---

### Health Checks (HEALTH_CHECKS)

**Problem:** No monitoring endpoint to verify application health.

**Solution:**
```python
# ✅ Secure - health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
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
            "database": "disconnected"
        }), 503
```

**Files:** app.py:387-411

---

## API Documentation

### Endpoints

#### GET /users/<user_id>
Get user by ID.

**Request:**
```bash
curl http://localhost:5000/users/123
```

**Response (200):**
```json
{
  "id": 123,
  "username": "john_doe",
  "email": "john@example.com"
}
```

**Response (404):**
```json
{
  "error": "User not found"
}
```

---

#### POST /login
Authenticate user and receive session token.

**Request:**
```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "password": "SecurePass123!"}'
```

**Response (200):**
```json
{
  "success": true,
  "message": "Login successful",
  "token": "abc123..."
}
```

**Response (401):**
```json
{
  "error": "Invalid credentials"
}
```

---

#### GET /search?q=<term>
Search users by username or email.

**Request:**
```bash
curl "http://localhost:5000/search?q=john"
```

**Response (200):**
```json
{
  "results": [
    {
      "id": 123,
      "username": "john_doe",
      "email": "john@example.com"
    }
  ]
}
```

---

#### DELETE /admin/delete/<user_id>
Delete user (requires authentication).

**Request:**
```bash
curl -X DELETE http://localhost:5000/admin/delete/123 \
  -H "Authorization: Bearer <token>"
```

**Response (200):**
```json
{
  "success": true,
  "message": "User deleted"
}
```

**Response (401):**
```json
{
  "error": "Authentication required"
}
```

---

#### GET /health
Health check endpoint for monitoring.

**Request:**
```bash
curl http://localhost:5000/health
```

**Response (200):**
```json
{
  "status": "healthy",
  "database": "connected"
}
```

---

## Testing

### Run Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

### Security Scanning
```bash
# Scan for security vulnerabilities
bandit -r .

# Check dependency vulnerabilities
safety check

# Static type checking
mypy app.py utils.py models.py
```

---

## Production Deployment

### Best Practices

1. **Use WSGI Server:**
   ```bash
   # Don't use Flask development server in production!
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

2. **Enable HTTPS:**
   - Use reverse proxy (nginx, Apache)
   - Obtain SSL certificate (Let's Encrypt)
   - Set `SESSION_COOKIE_SECURE=True`

3. **Database:**
   - Use PostgreSQL instead of SQLite
   - Enable connection pooling
   - Set up regular backups

4. **Monitoring:**
   - Integrate with CloudWatch, Splunk, or Datadog
   - Set up alerts for errors and performance issues
   - Monitor `/health` endpoint

5. **Rate Limiting:**
   ```python
   from flask_limiter import Limiter

   limiter = Limiter(app, default_limits=["200 per day", "50 per hour"])
   ```

6. **Secrets Management:**
   - Use AWS Secrets Manager, HashiCorp Vault, or similar
   - Rotate credentials regularly
   - Never commit `.env` files

---

## Comparison with Vulnerable Version

For a detailed side-by-side comparison of vulnerabilities and fixes, see:
- `../SECURITY-COMPARISON.md` - Comprehensive security analysis
- `../legacy-app-vulnerable/README.md` - Vulnerable version documentation

---

## CLAUDE.md Rules Compliance

This application follows all applicable CLAUDE.md rules:

✅ **CRITICAL:**
- NO_SECRETS_IN_CODE - Environment variables for all secrets
- INPUT_VALIDATION - Parameterized queries, input validation
- DATA_ENCRYPTION - Argon2 password hashing
- LEAST_PRIVILEGE - Authentication required for privileged operations
- CONFIG_MANAGEMENT - Environment-based configuration

✅ **HIGH:**
- ERROR_HANDLING - Comprehensive try-catch blocks
- LOGGING - Structured logging with levels
- CONTEXT_IN_ERRORS - Errors include operation context
- DOCUMENT_APIS - Comprehensive docstrings and API docs
- CODE_COMMENTS - Proper documentation throughout
- HEALTH_CHECKS - Health check endpoint implemented

✅ **MEDIUM:**
- TEMPORARY_CREDENTIALS - AWS IAM role support

---

## Contributing

When adding features, ensure:
1. All secrets in environment variables
2. All queries use parameterization
3. Comprehensive error handling
4. Structured logging
5. API documentation
6. Unit tests
7. Security scanning passes

---

## License

Educational use only. Part of "AI Agents and MCPs in Development and Operations" course.

---

## Related Files

- **Vulnerable Version:** `../legacy-app-vulnerable/`
- **Comparison Document:** `../SECURITY-COMPARISON.md`
- **CLAUDE.md Rules:** `/Users/csmith/.claude/CLAUDE.md`
- **Refactoring Plan:** `../../REFACTORING-PLAN.md`

---

**Last Updated:** 2025-10-27
**Purpose:** Demonstrate security best practices and CLAUDE.md compliance
