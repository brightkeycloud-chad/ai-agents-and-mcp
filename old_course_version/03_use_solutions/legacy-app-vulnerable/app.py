"""
Legacy Flask Application (circa 2015)
INTENTIONALLY CONTAINS SECURITY VULNERABILITIES FOR DEMO PURPOSES
"""

from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

# SECURITY ISSUE: Hardcoded API key
API_KEY = "sk_live_abc123xyz789"

# SECURITY ISSUE: Hardcoded database credentials
DB_USER = "admin"
DB_PASS = "Password123"


@app.route('/users/<id>')
def get_user(id):
    """Get user by ID - HAS SQL INJECTION VULNERABILITY"""
    # SECURITY ISSUE: SQL injection vulnerability
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE id = " + id  # Vulnerable!
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    return str(user)


@app.route('/login', methods=['POST'])
def login():
    """Login endpoint - STORES PASSWORDS IN PLAIN TEXT"""
    username = request.form['username']
    password = request.form['password']  # Plain text password!

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # SECURITY ISSUE: Plain text password storage and SQL injection
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        return "Login successful"
    else:
        return "Login failed"


@app.route('/search')
def search():
    """Search users - MISSING INPUT VALIDATION"""
    # SECURITY ISSUE: No input validation
    search_term = request.args.get('q')

    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # SECURITY ISSUE: SQL injection via search parameter
    query = f"SELECT * FROM users WHERE name LIKE '%{search_term}%'"
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    return str(results)


@app.route('/admin/delete/<user_id>')
def delete_user(user_id):
    """Delete user - NO AUTHENTICATION/AUTHORIZATION"""
    # SECURITY ISSUE: No authentication check!
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # SECURITY ISSUE: SQL injection
    query = f"DELETE FROM users WHERE id = {user_id}"
    cursor.execute(query)
    conn.commit()
    conn.close()

    return "User deleted"


def send_email(recipient, subject, body):
    """Send email using external API"""
    import requests

    # SECURITY ISSUE: Using hardcoded API key from global variable
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }

    data = {
        'to': recipient,
        'subject': subject,
        'body': body
    }

    # SECURITY ISSUE: No error handling, no timeout
    response = requests.post('https://api.emailservice.com/send',
                           headers=headers,
                           json=data)
    return response.json()


if __name__ == '__main__':
    # SECURITY ISSUE: Debug mode in production, running on all interfaces
    app.run(debug=True, host='0.0.0.0', port=5000)
