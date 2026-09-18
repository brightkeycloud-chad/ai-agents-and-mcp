"""
Utility functions
CONTAINS SECURITY ISSUES FOR DEMO PURPOSES
"""

import os
import hashlib


# SECURITY ISSUE: Hardcoded AWS credentials
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"


def connect_to_s3():
    """Connect to S3 - HARDCODED CREDENTIALS"""
    import boto3

    # SECURITY ISSUE: Hardcoded credentials
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY
    )
    return s3_client


def hash_password(password):
    """Hash password - WEAK HASHING"""
    # SECURITY ISSUE: MD5 is not suitable for passwords
    return hashlib.md5(password.encode()).hexdigest()


def validate_email(email):
    """Validate email - POOR VALIDATION"""
    # ISSUE: Very basic validation, doesn't catch many invalid emails
    return '@' in email


def sanitize_input(user_input):
    """Sanitize user input - INEFFECTIVE"""
    # SECURITY ISSUE: Incomplete sanitization, can be bypassed
    dangerous_chars = ["'", '"']
    for char in dangerous_chars:
        user_input = user_input.replace(char, '')
    return user_input


def generate_token():
    """Generate session token - PREDICTABLE"""
    import time

    # SECURITY ISSUE: Predictable token based on timestamp
    timestamp = str(int(time.time()))
    return hashlib.md5(timestamp.encode()).hexdigest()


def log_activity(user_id, action):
    """Log user activity - LOGS SENSITIVE DATA"""
    import logging

    # SECURITY ISSUE: May log sensitive information
    logging.info(f"User {user_id} performed: {action}")

    # SECURITY ISSUE: Writing logs to world-readable file
    with open('/tmp/app.log', 'a') as f:
        f.write(f"User {user_id}: {action}\n")
