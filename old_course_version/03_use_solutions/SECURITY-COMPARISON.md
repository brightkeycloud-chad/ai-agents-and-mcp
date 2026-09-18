# Security Comparison: Vulnerable vs Secure Implementation

This document provides a side-by-side comparison of security vulnerabilities and their fixes, demonstrating CLAUDE.md compliance.

---

## 1. Hardcoded Secrets (CRITICAL)

### ❌ Vulnerable Version
**File:** `legacy-app-vulnerable/app.py:13-17`, `utils.py:11-12`

```python
# SECURITY ISSUE: Hardcoded credentials
API_KEY = "sk_live_abc123xyz789"
DB_USER = "admin"
DB_PASS = "Password123"
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
```

**Issues:**
- Credentials visible in source code
- Exposed in version control history
- Visible in logs and error messages
- Cannot be rotated without code changes

**CLAUDE.md Rule Violated:** NO_SECRETS_IN_CODE

### ✅ Secure Version
**File:** `legacy-app-secure/app.py:27-37`, `.env.example`

```python
# SECURITY: Load from environment variables
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('API_KEY')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')

# Validate required variables
if not all([API_KEY, DB_USER, DB_PASS]):
    raise ValueError("Missing required environment variables")
```

**.env.example:**
```bash
API_KEY=your_api_key_here
DB_USER=your_database_user
DB_PASS=your_database_password
```

**Improvements:**
- Secrets in `.env` file (git-ignored)
- Can rotate without code changes
- Different values per environment
- Fails safely if missing

**CLAUDE.md Rules Followed:** NO_SECRETS_IN_CODE, CONFIG_MANAGEMENT

---

## 2. SQL Injection (CRITICAL)

### ❌ Vulnerable Version
**File:** `legacy-app-vulnerable/app.py:26, 43-44, 64, 80`

```python
# SECURITY ISSUE: String concatenation allows SQL injection
query = "SELECT * FROM users WHERE id = " + id
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
query = f"SELECT * FROM users WHERE name LIKE '%{search_term}%'"
query = f"DELETE FROM users WHERE id = {user_id}"
```

**Attack Examples:**
```bash
# Extract all users
curl "http://localhost:5000/users/1 OR 1=1--"

# Drop table
curl "http://localhost:5000/users/1; DROP TABLE users;--"

# Bypass authentication
curl -X POST /login -d "username=admin'--&password=anything"
```

**CLAUDE.md Rule Violated:** INPUT_VALIDATION

### ✅ Secure Version
**File:** `legacy-app-secure/app.py:112-116, 169-173`, `models.py:136-143`

```python
# SECURITY: Parameterized queries prevent SQL injection
cursor.execute(
    "SELECT * FROM users WHERE id = ?",
    (user_id,)
)

cursor.execute(
    "SELECT * FROM users WHERE username = ?",
    (username,)
)

cursor.execute(
    "SELECT * FROM users WHERE name LIKE ? OR email LIKE ?",
    (f'%{search_term}%', f'%{search_term}%')
)
```

**Improvements:**
- Database driver handles escaping
- User input never concatenated into queries
- Prevents all SQL injection attacks
- Input validation as defense-in-depth

**CLAUDE.md Rules Followed:** INPUT_VALIDATION

---

## 3. Password Storage (CRITICAL)

### ❌ Vulnerable Version
**File:** `legacy-app-vulnerable/app.py:37`, `utils.py:28-31`

```python
# SECURITY ISSUE: Plain text password
password = request.form['password']  # No hashing!

# SECURITY ISSUE: MD5 is cryptographically broken
def hash_password(password):
    return hashlib.md5(password.encode()).hexdigest()
```

**Issues:**
- MD5 is broken (rainbow tables exist)
- No salt (same password = same hash)
- Fast to brute force (billions of hashes/sec)
- All passwords compromised if database leaked

**CLAUDE.md Rule Violated:** DATA_ENCRYPTION

### ✅ Secure Version
**File:** `legacy-app-secure/utils.py:27-83`, `models.py:93-115`

```python
# SECURITY: Argon2 password hashing (PHC winner 2015)
from argon2 import PasswordHasher

ph = PasswordHasher(
    time_cost=2,
    memory_cost=65536,  # 64 MB
    parallelism=2,
    hash_len=32,
    salt_len=16
)

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(password_hash: str, password: str) -> bool:
    try:
        ph.verify(password_hash, password)
        return True
    except VerifyMismatchError:
        return False
```

**Improvements:**
- Argon2 is memory-hard (resistant to GPUs/ASICs)
- Automatic salt generation
- Configurable work factors
- Timing-safe verification

**CLAUDE.md Rules Followed:** DATA_ENCRYPTION

---

## 4. Missing Authentication (CRITICAL)

### ❌ Vulnerable Version
**File:** `legacy-app-vulnerable/app.py:72-85`

```python
@app.route('/admin/delete/<user_id>')
def delete_user(user_id):
    # SECURITY ISSUE: No authentication check!
    # Anyone can delete any user
    query = f"DELETE FROM users WHERE id = {user_id}"
    cursor.execute(query)
```

**Issues:**
- No authentication required
- No authorization check
- Anyone can delete users
- Uses vulnerable GET instead of DELETE

**CLAUDE.md Rule Violated:** LEAST_PRIVILEGE

### ✅ Secure Version
**File:** `legacy-app-secure/app.py:284-325`

```python
@app.route('/admin/delete/<int:user_id>', methods=['DELETE'])
@require_auth  # SECURITY: Require authentication
def delete_user(user_id: int):
    # In production, also verify admin role
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()

            # Check if user exists
            cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
            if not cursor.fetchone():
                return jsonify({"error": "User not found"}), 404

            # Parameterized query
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()

            logger.info(f"User {user_id} deleted")
            return jsonify({"success": True}), 200

    except sqlite3.Error as e:
        logger.error(f"Error deleting user {user_id}: {str(e)}")
        return jsonify({"error": "Database error"}), 500
```

**Decorator Implementation:**
```python
def require_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = request.headers.get('Authorization')

        if not auth_token or not auth_token.startswith('Bearer '):
            return jsonify({"error": "Authentication required"}), 401

        # In production: validate token against database/JWT
        return f(*args, **kwargs)
    return decorated_function
```

**Improvements:**
- Authentication required
- Proper HTTP method (DELETE)
- Existence check before deletion
- Error handling and logging

**CLAUDE.md Rules Followed:** LEAST_PRIVILEGE

---

## 5. No Error Handling (HIGH)

### ❌ Vulnerable Version
**File:** `legacy-app-vulnerable/app.py:88-108`

```python
def send_email(recipient, subject, body):
    headers = {'Authorization': f'Bearer {API_KEY}'}
    data = {'to': recipient, 'subject': subject, 'body': body}

    # SECURITY ISSUE: No error handling, no timeout
    response = requests.post('https://api.emailservice.com/send',
                           headers=headers,
                           json=data)
    return response.json()
```

**Issues:**
- No timeout (can hang forever)
- No error handling (exposes stack traces)
- No retry logic (fails on transient errors)
- No input validation

**CLAUDE.md Rule Violated:** ERROR_HANDLING

### ✅ Secure Version
**File:** `legacy-app-secure/app.py:327-385`

```python
def send_email(recipient: str, subject: str, body: str) -> Dict[str, Any]:
    # Input validation
    if not all([recipient, subject, body]):
        raise ValueError("recipient, subject, and body are required")

    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_regex, recipient):
        raise ValueError(f"Invalid email: {recipient}")

    # Retry strategy
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504]
    )

    session = requests.Session()
    session.mount("https://", HTTPAdapter(max_retries=retry_strategy))

    try:
        response = session.post(
            EMAIL_SERVICE_URL,
            headers={'Authorization': f'Bearer {API_KEY}'},
            json={'to': recipient, 'subject': subject, 'body': body},
            timeout=10  # 10 second timeout
        )

        response.raise_for_status()
        logger.info(f"Email sent to {recipient}")
        return response.json()

    except requests.Timeout as e:
        logger.error(f"Timeout sending email: {str(e)}")
        raise
    except requests.HTTPError as e:
        logger.error(f"HTTP error: {response.status_code}")
        raise
    finally:
        session.close()
```

**Improvements:**
- Input validation
- 10-second timeout
- Retry logic for transient failures
- Comprehensive error handling
- Structured logging

**CLAUDE.md Rules Followed:** ERROR_HANDLING, CONTEXT_IN_ERRORS, INPUT_VALIDATION

---

## 6. Poor Logging (HIGH)

### ❌ Vulnerable Version
**File:** `legacy-app-vulnerable/utils.py:58-67`

```python
def log_activity(user_id, action):
    # SECURITY ISSUE: Logs may contain sensitive data
    logging.info(f"User {user_id} performed: {action}")

    # SECURITY ISSUE: World-readable file
    with open('/tmp/app.log', 'a') as f:
        f.write(f"User {user_id}: {action}\n")
```

**Issues:**
- May log sensitive data (passwords, tokens)
- World-readable log file (`/tmp/app.log`)
- No log levels
- No structured format
- No log rotation

**CLAUDE.md Rule Violated:** LOGGING

### ✅ Secure Version
**File:** `legacy-app-secure/utils.py:251-291`, `app.py:23-26`

```python
# Configure structured logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def log_activity(user_id: int, action: str, context: Optional[dict] = None):
    # Sanitize context
    safe_fields = ['ip', 'user_agent', 'action_type', 'resource_id']
    safe_context = {
        k: v for k, v in (context or {}).items()
        if k in safe_fields
    }

    # Structured logging
    logger.info(
        "User activity",
        extra={
            'user_id': user_id,
            'action': action,
            'context': safe_context
        }
    )
```

**Usage throughout application:**
```python
logger.info(f"User {user_id} retrieved successfully")
logger.warning(f"Failed login attempt for user {username}")
logger.error(f"Database error: {str(e)}")
logger.debug(f"Password hashed successfully")
```

**Improvements:**
- Structured logging with levels
- Whitelist of safe fields to log
- No sensitive data (passwords filtered)
- Configurable log level
- Proper file permissions via logging config
- Integration-ready (CloudWatch, Splunk, etc.)

**CLAUDE.md Rules Followed:** LOGGING

---

## 7. AWS Credentials (CRITICAL)

### ❌ Vulnerable Version
**File:** `legacy-app-vulnerable/utils.py:10-25`

```python
# SECURITY ISSUE: Hardcoded AWS credentials
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

def connect_to_s3():
    import boto3

    # SECURITY ISSUE: Hardcoded credentials
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    return s3_client
```

**Issues:**
- Long-lived credentials in code
- Cannot rotate without code change
- No IAM role support
- Credentials in logs/version control

**CLAUDE.md Rule Violated:** TEMPORARY_CREDENTIALS, NO_SECRETS_IN_CODE

### ✅ Secure Version
**File:** `legacy-app-secure/utils.py:206-249`

```python
def connect_to_s3(region: Optional[str] = None):
    """
    AWS Credential Chain (in order):
    1. IAM role (EC2/ECS/Lambda) - RECOMMENDED
    2. Environment variables
    3. ~/.aws/credentials file
    4. ~/.aws/config file
    """
    if not region:
        region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')

    try:
        # Uses boto3 default credential chain
        s3_client = boto3.client('s3', region_name=region)

        # Verify credentials
        s3_client.list_buckets()

        logger.info(f"Connected to S3 in region {region}")
        return s3_client

    except NoCredentialsError:
        logger.error("No AWS credentials found")
        raise
    except ClientError as e:
        logger.error(f"S3 connection failed: {str(e)}")
        raise
```

**Improvements:**
- Uses IAM roles (temporary credentials)
- Falls back to environment variables
- No hardcoded credentials
- Comprehensive error handling
- Verifies connectivity

**CLAUDE.md Rules Followed:** TEMPORARY_CREDENTIALS, NO_SECRETS_IN_CODE

---

## Summary Table

| Issue | Vulnerable | Secure | CLAUDE.md Rule | Priority |
|-------|-----------|--------|----------------|----------|
| Hardcoded Secrets | In source code | Environment variables | NO_SECRETS_IN_CODE | CRITICAL |
| SQL Injection | String concat | Parameterized queries | INPUT_VALIDATION | CRITICAL |
| Passwords | Plain text/MD5 | Argon2 hashing | DATA_ENCRYPTION | CRITICAL |
| Authentication | None | Required decorator | LEAST_PRIVILEGE | CRITICAL |
| Error Handling | None | Comprehensive | ERROR_HANDLING | HIGH |
| Logging | Plain text file | Structured | LOGGING | HIGH |
| AWS Credentials | Hardcoded | IAM roles/env vars | TEMPORARY_CREDENTIALS | CRITICAL |

---

## For Instructors

Use this comparison to demonstrate:

1. **Real-world consequences** of each vulnerability
2. **Proper fixes** following industry best practices
3. **CLAUDE.md rule compliance** for each security issue
4. **Defense-in-depth** approach (multiple layers of security)

---

**Related Files:**
- Vulnerable version: `legacy-app-vulnerable/`
- Secure version: `legacy-app-secure/`
- CLAUDE.md rules: `/Users/csmith/.claude/CLAUDE.md`
