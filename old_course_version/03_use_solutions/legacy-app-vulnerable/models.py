"""
Legacy database models
CONTAINS POOR PRACTICES FOR DEMO PURPOSES
"""

import sqlite3


class User:
    """User model - uses old patterns"""

    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password  # ISSUE: Storing plain text password
        self.email = email

    def save(self):
        """Save user to database - SQL INJECTION RISK"""
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # SECURITY ISSUE: String concatenation in SQL
        query = f"""
            INSERT INTO users (username, password, email)
            VALUES ('{self.username}', '{self.password}', '{self.email}')
        """

        cursor.execute(query)
        conn.commit()
        conn.close()

    @staticmethod
    def find_by_username(username):
        """Find user by username - SQL INJECTION RISK"""
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # SECURITY ISSUE: String formatting in SQL query
        query = f"SELECT * FROM users WHERE username = '{username}'"
        cursor.execute(query)
        result = cursor.fetchone()
        conn.close()

        if result:
            return User(*result)
        return None

    def update_password(self, new_password):
        """Update password - PLAIN TEXT STORAGE"""
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # SECURITY ISSUE: Plain text password, SQL injection
        query = f"UPDATE users SET password = '{new_password}' WHERE id = {self.id}"
        cursor.execute(query)
        conn.commit()
        conn.close()

        self.password = new_password


class Session:
    """User session - INSECURE SESSION MANAGEMENT"""

    def __init__(self, user_id, token):
        self.user_id = user_id
        self.token = token  # ISSUE: No expiration, weak token generation

    @staticmethod
    def create(user_id):
        """Create session - WEAK TOKEN GENERATION"""
        import random
        import string

        # SECURITY ISSUE: Predictable token generation
        token = ''.join(random.choices(string.ascii_letters, k=10))

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        # SECURITY ISSUE: SQL injection
        query = f"INSERT INTO sessions (user_id, token) VALUES ({user_id}, '{token}')"
        cursor.execute(query)
        conn.commit()
        conn.close()

        return Session(user_id, token)
