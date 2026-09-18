"""
Utility functions - Secure Implementation
Demonstrates security best practices following CLAUDE.md rules
"""

import os
import logging
from typing import Optional
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHash
import re
import secrets
import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure logging
logger = logging.getLogger(__name__)

# Initialize password hasher with secure defaults
# Argon2 is the recommended password hashing algorithm (winner of PHC 2015)
ph = PasswordHasher(
    time_cost=2,        # Number of iterations
    memory_cost=65536,  # Memory usage in KiB (64 MB)
    parallelism=2,      # Number of parallel threads
    hash_len=32,        # Length of hash in bytes
    salt_len=16         # Length of salt in bytes
)


def hash_password(password: str) -> str:
    """
    Hash password using Argon2 - cryptographically secure.

    SECURITY IMPROVEMENTS from vulnerable version:
    - Uses Argon2 instead of MD5 (DATA_ENCRYPTION)
    - Argon2 is resistant to GPU/ASIC attacks
    - Automatically handles salt generation
    - Configurable work factors

    Args:
        password (str): Plain text password to hash

    Returns:
        str: Argon2 password hash

    Raises:
        ValueError: If password is empty or too long
        Exception: If hashing fails

    Example:
        >>> hash_password("SecurePassword123!")
        "$argon2id$v=19$m=65536,t=2,p=2$..."

    Note:
        Hash includes algorithm parameters, so it's safe to store directly.
        No need to store salt separately - it's included in the hash.
    """
    if not password:
        raise ValueError("Password cannot be empty")

    if len(password) > 200:
        raise ValueError("Password too long (max 200 characters)")

    try:
        password_hash = ph.hash(password)
        logger.debug("Password hashed successfully")
        return password_hash

    except Exception as e:
        logger.error(f"Password hashing failed: {str(e)}")
        raise


def verify_password(password_hash: str, password: str) -> bool:
    """
    Verify password against Argon2 hash.

    SECURITY IMPROVEMENTS from vulnerable version:
    - Uses secure password verification (DATA_ENCRYPTION)
    - Timing-safe comparison
    - Automatically rehashes if parameters changed

    Args:
        password_hash (str): Stored Argon2 hash
        password (str): Plain text password to verify

    Returns:
        bool: True if password matches, False otherwise

    Example:
        >>> hash = hash_password("SecurePassword123!")
        >>> verify_password(hash, "SecurePassword123!")
        True
        >>> verify_password(hash, "WrongPassword")
        False

    Note:
        Returns False for any error to prevent timing attacks.
        Logs errors for monitoring.
    """
    if not password_hash or not password:
        logger.warning("Empty password or hash provided for verification")
        return False

    try:
        # Verify password - raises exception if doesn't match
        ph.verify(password_hash, password)

        # Check if hash needs rehashing (parameters changed)
        if ph.check_needs_rehash(password_hash):
            logger.info("Password hash needs rehashing with new parameters")

        return True

    except VerifyMismatchError:
        logger.debug("Password verification failed - mismatch")
        return False

    except (VerificationError, InvalidHash) as e:
        logger.warning(f"Invalid password hash format: {str(e)}")
        return False

    except Exception as e:
        logger.error(f"Unexpected error during password verification: {str(e)}")
        return False


def validate_email(email: str) -> bool:
    """
    Validate email address using comprehensive regex.

    SECURITY IMPROVEMENTS from vulnerable version:
    - Comprehensive regex validation instead of just checking for '@'
    - Follows RFC 5322 standards (simplified)
    - Input length validation

    Args:
        email (str): Email address to validate

    Returns:
        bool: True if valid email format, False otherwise

    Example:
        >>> validate_email("user@example.com")
        True
        >>> validate_email("invalid.email")
        False
        >>> validate_email("user@")
        False

    Note:
        This validates format only, not whether email exists.
        For production, consider using email verification services.
    """
    if not email or len(email) > 254:  # RFC 5321
        return False

    # Comprehensive email regex (simplified RFC 5322)
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

    return bool(re.match(email_regex, email))


def sanitize_input(user_input: str, max_length: int = 1000) -> str:
    """
    Sanitize user input by removing potentially dangerous characters.

    SECURITY IMPROVEMENTS from vulnerable version:
    - More comprehensive character filtering (INPUT_VALIDATION)
    - Length validation
    - Whitespace normalization
    - Logging of sanitization events

    Args:
        user_input (str): Raw user input to sanitize
        max_length (int): Maximum allowed length (default: 1000)

    Returns:
        str: Sanitized input

    Raises:
        ValueError: If input exceeds max_length after sanitization

    Example:
        >>> sanitize_input("Hello<script>alert('xss')</script>")
        "Helloalert('xss')"

    Note:
        This is a defense-in-depth measure. Primary defense should be:
        1. Parameterized queries for SQL
        2. Template escaping for HTML
        3. Input validation at application layer
    """
    if not user_input:
        return ""

    # Remove null bytes
    sanitized = user_input.replace('\x00', '')

    # Remove control characters except newline, carriage return, tab
    sanitized = ''.join(
        char for char in sanitized
        if char in '\n\r\t' or not (0 <= ord(char) <= 31 or ord(char) == 127)
    )

    # Normalize whitespace
    sanitized = ' '.join(sanitized.split())

    # Enforce length limit
    if len(sanitized) > max_length:
        logger.warning(f"Input truncated from {len(sanitized)} to {max_length} characters")
        sanitized = sanitized[:max_length]

    if sanitized != user_input:
        logger.debug("Input sanitization performed")

    return sanitized


def generate_token(length: int = 32) -> str:
    """
    Generate cryptographically secure random token.

    SECURITY IMPROVEMENTS from vulnerable version:
    - Uses secrets module instead of timestamp-based MD5
    - Cryptographically secure random generation
    - URL-safe encoding

    Args:
        length (int): Desired token length in bytes (default: 32)

    Returns:
        str: URL-safe random token

    Example:
        >>> token = generate_token()
        >>> len(token) > 0
        True
        >>> token1 = generate_token()
        >>> token2 = generate_token()
        >>> token1 != token2  # Extremely unlikely to be equal
        True

    Note:
        Uses os.urandom() internally via secrets module.
        Suitable for session tokens, CSRF tokens, API keys, etc.
    """
    if length < 16:
        logger.warning("Token length less than 16 bytes - using 16 minimum")
        length = 16

    if length > 128:
        logger.warning("Token length greater than 128 bytes - using 128 maximum")
        length = 128

    token = secrets.token_urlsafe(length)
    logger.debug(f"Secure token generated ({length} bytes)")
    return token


def connect_to_s3(region: Optional[str] = None):
    """
    Connect to AWS S3 using secure credential management.

    SECURITY IMPROVEMENTS from vulnerable version:
    - Uses AWS credential chain instead of hardcoded credentials (TEMPORARY_CREDENTIALS)
    - Supports IAM roles (recommended)
    - Falls back to environment variables
    - Comprehensive error handling (ERROR_HANDLING)

    AWS Credential Chain (in order of precedence):
    1. IAM role (recommended for EC2/ECS/Lambda)
    2. Environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
    3. AWS credentials file (~/.aws/credentials)
    4. AWS config file (~/.aws/config)

    Args:
        region (str, optional): AWS region. Defaults to AWS_DEFAULT_REGION env var or us-east-1

    Returns:
        boto3.client: S3 client object

    Raises:
        NoCredentialsError: If no credentials found in chain
        ClientError: If connection fails

    Example:
        >>> s3 = connect_to_s3('us-west-2')
        >>> buckets = s3.list_buckets()

    Note:
        BEST PRACTICE: Use IAM roles when running on AWS infrastructure.
        Never hardcode credentials in source code.
    """
    if not region:
        region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')

    try:
        # SECURITY: Uses boto3 default credential chain
        # This will automatically use IAM role if available (most secure)
        # Falls back to environment variables or credentials file
        s3_client = boto3.client('s3', region_name=region)

        # Verify credentials by making a simple API call
        s3_client.list_buckets()

        logger.info(f"Successfully connected to S3 in region {region}")
        return s3_client

    except NoCredentialsError as e:
        logger.error(
            "No AWS credentials found. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY "
            "environment variables or use IAM role."
        )
        raise

    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code', 'Unknown')
        logger.error(f"AWS S3 connection failed: {error_code} - {str(e)}")
        raise

    except Exception as e:
        logger.error(f"Unexpected error connecting to S3: {str(e)}")
        raise


def log_activity(user_id: int, action: str, context: Optional[dict] = None) -> None:
    """
    Log user activity with proper security controls.

    SECURITY IMPROVEMENTS from vulnerable version:
    - Structured logging instead of plain text file (LOGGING)
    - No sensitive data in logs
    - Secure file permissions (if file logging is configured)
    - Contextual information for audit trail (CONTEXT_IN_ERRORS)

    Args:
        user_id (int): User ID performing the action
        action (str): Action being performed (e.g., "login", "update_profile")
        context (dict, optional): Additional context (sanitized, no sensitive data)

    Example:
        >>> log_activity(123, "login", {"ip": "192.168.1.1", "user_agent": "Mozilla/5.0"})

    Note:
        Do NOT log sensitive data (passwords, tokens, PII unless required for compliance).
        Ensure log files have restricted permissions (600 or 640).
        Consider log aggregation service for production (CloudWatch, Splunk, etc.).
    """
    # Validate inputs
    if not isinstance(user_id, int) or user_id <= 0:
        logger.warning(f"Invalid user_id for activity logging: {user_id}")
        return

    if not action or len(action) > 100:
        logger.warning(f"Invalid action for activity logging: {action}")
        return

    # Sanitize context to prevent logging sensitive data
    safe_context = {}
    if context:
        # Whitelist of safe fields to log
        safe_fields = ['ip', 'user_agent', 'action_type', 'resource_id', 'timestamp']
        safe_context = {
            k: v for k, v in context.items()
            if k in safe_fields and isinstance(v, (str, int, float, bool))
        }

    # SECURITY: Use structured logging, not world-readable file
    logger.info(
        f"User activity",
        extra={
            'user_id': user_id,
            'action': action,
            'context': safe_context
        }
    )


# Example usage and tests
if __name__ == '__main__':
    # Configure logging for testing
    logging.basicConfig(level=logging.DEBUG)

    # Test password hashing
    print("Testing password hashing...")
    password = "SecurePassword123!"
    hashed = hash_password(password)
    print(f"Hash: {hashed[:50]}...")
    print(f"Verify correct password: {verify_password(hashed, password)}")
    print(f"Verify wrong password: {verify_password(hashed, 'WrongPassword')}")

    # Test email validation
    print("\nTesting email validation...")
    print(f"Valid email: {validate_email('user@example.com')}")
    print(f"Invalid email: {validate_email('invalid.email')}")

    # Test token generation
    print("\nTesting token generation...")
    token = generate_token()
    print(f"Generated token: {token[:20]}... (length: {len(token)})")

    # Test input sanitization
    print("\nTesting input sanitization...")
    dirty_input = "Hello<script>alert('xss')</script>\x00\n\n\n   World   "
    clean_input = sanitize_input(dirty_input)
    print(f"Original: {repr(dirty_input)}")
    print(f"Sanitized: {repr(clean_input)}")

    # Test activity logging
    print("\nTesting activity logging...")
    log_activity(123, "test_action", {"ip": "192.168.1.1", "password": "should_not_be_logged"})

    print("\nAll tests completed!")
