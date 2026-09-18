"""
Secure Database Models
Demonstrates proper data access patterns following CLAUDE.md rules
"""

import sqlite3
import logging
from datetime import datetime, timedelta
from typing import Optional, List
from contextlib import contextmanager
from utils import hash_password, verify_password, generate_token

logger = logging.getLogger(__name__)


@contextmanager
def get_db():
    """
    Context manager for database connections (ERROR_HANDLING).

    Ensures connections are properly closed even if exceptions occur.

    Yields:
        sqlite3.Connection: Database connection

    Example:
        >>> with get_db() as conn:
        ...     cursor = conn.cursor()
        ...     cursor.execute("SELECT * FROM users")
    """
    conn = sqlite3.connect('users.db')
    conn.row_factory = sqlite3.Row  # Enable column access by name
    try:
        yield conn
    finally:
        conn.close()


class User:
    """
    User model with secure password handling and parameterized queries.

    SECURITY IMPROVEMENTS from vulnerable version:
    - Password hashing instead of plain text storage (DATA_ENCRYPTION)
    - Parameterized queries prevent SQL injection (INPUT_VALIDATION)
    - Input validation on all fields
    - Comprehensive error handling (ERROR_HANDLING)

    Attributes:
        id (int): User ID
        username (str): Username (unique)
        password_hash (str): Argon2 password hash
        email (str): Email address
        created_at (datetime): Account creation timestamp
    """

    def __init__(
        self,
        id: Optional[int] = None,
        username: str = "",
        password_hash: str = "",
        email: str = "",
        created_at: Optional[datetime] = None
    ):
        """
        Initialize User instance.

        Args:
            id (int, optional): User ID (None for new users)
            username (str): Username
            password_hash (str): Argon2 password hash
            email (str): Email address
            created_at (datetime, optional): Creation timestamp
        """
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.created_at = created_at or datetime.now()

    def save(self) -> bool:
        """
        Save user to database with secure password hashing.

        SECURITY IMPROVEMENTS:
        - Parameterized query prevents SQL injection (INPUT_VALIDATION)
        - Password is hashed before storage (DATA_ENCRYPTION)
        - Input validation
        - Error handling with context (ERROR_HANDLING, CONTEXT_IN_ERRORS)

        Returns:
            bool: True if successful, False otherwise

        Raises:
            ValueError: If validation fails

        Example:
            >>> user = User(username="john", email="john@example.com")
            >>> user.set_password("SecurePass123!")
            >>> user.save()
            True
        """
        # Validate inputs
        if not self.username or len(self.username) > 50:
            raise ValueError("Username must be between 1-50 characters")

        if not self.email or len(self.email) > 100:
            raise ValueError("Email must be between 1-100 characters")

        if not self.password_hash:
            raise ValueError("Password hash is required. Call set_password() first.")

        try:
            with get_db() as conn:
                cursor = conn.cursor()

                # SECURITY: Parameterized query prevents SQL injection
                cursor.execute(
                    """
                    INSERT INTO users (username, password_hash, email, created_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (self.username, self.password_hash, self.email, self.created_at)
                )

                conn.commit()
                self.id = cursor.lastrowid

                logger.info(f"User '{self.username}' created successfully (ID: {self.id})")
                return True

        except sqlite3.IntegrityError as e:
            # Username or email already exists
            logger.warning(f"Failed to create user '{self.username}': {str(e)}")
            return False

        except sqlite3.Error as e:
            logger.error(f"Database error creating user '{self.username}': {str(e)}")
            return False

        except Exception as e:
            logger.error(f"Unexpected error creating user '{self.username}': {str(e)}")
            return False

    def set_password(self, plain_password: str) -> None:
        """
        Set user password using secure hashing.

        SECURITY: Uses Argon2 for password hashing (DATA_ENCRYPTION)

        Args:
            plain_password (str): Plain text password

        Raises:
            ValueError: If password is invalid

        Example:
            >>> user = User(username="john", email="john@example.com")
            >>> user.set_password("SecurePass123!")
        """
        if not plain_password or len(plain_password) < 8:
            raise ValueError("Password must be at least 8 characters")

        if len(plain_password) > 200:
            raise ValueError("Password too long (max 200 characters)")

        self.password_hash = hash_password(plain_password)
        logger.debug(f"Password set for user '{self.username}'")

    def check_password(self, plain_password: str) -> bool:
        """
        Verify password against stored hash.

        SECURITY: Uses timing-safe comparison (DATA_ENCRYPTION)

        Args:
            plain_password (str): Plain text password to verify

        Returns:
            bool: True if password matches, False otherwise

        Example:
            >>> user = User.find_by_username("john")
            >>> user.check_password("SecurePass123!")
            True
        """
        if not self.password_hash or not plain_password:
            return False

        return verify_password(self.password_hash, plain_password)

    @staticmethod
    def find_by_username(username: str) -> Optional['User']:
        """
        Find user by username using parameterized query.

        SECURITY IMPROVEMENTS:
        - Parameterized query prevents SQL injection (INPUT_VALIDATION)
        - Input validation
        - Error handling

        Args:
            username (str): Username to search for

        Returns:
            Optional[User]: User instance if found, None otherwise

        Example:
            >>> user = User.find_by_username("john")
            >>> if user:
            ...     print(f"Found user: {user.email}")
        """
        if not username or len(username) > 50:
            logger.warning(f"Invalid username length for search: {len(username)}")
            return None

        try:
            with get_db() as conn:
                cursor = conn.cursor()

                # SECURITY: Parameterized query prevents SQL injection
                cursor.execute(
                    """
                    SELECT id, username, password_hash, email, created_at
                    FROM users
                    WHERE username = ?
                    """,
                    (username,)
                )

                result = cursor.fetchone()

                if result:
                    logger.debug(f"User '{username}' found")
                    return User(
                        id=result['id'],
                        username=result['username'],
                        password_hash=result['password_hash'],
                        email=result['email'],
                        created_at=datetime.fromisoformat(result['created_at'])
                    )

                logger.debug(f"User '{username}' not found")
                return None

        except sqlite3.Error as e:
            logger.error(f"Database error finding user '{username}': {str(e)}")
            return None

        except Exception as e:
            logger.error(f"Unexpected error finding user '{username}': {str(e)}")
            return None

    @staticmethod
    def find_by_id(user_id: int) -> Optional['User']:
        """
        Find user by ID using parameterized query.

        Args:
            user_id (int): User ID to search for

        Returns:
            Optional[User]: User instance if found, None otherwise

        Example:
            >>> user = User.find_by_id(123)
        """
        if not isinstance(user_id, int) or user_id <= 0:
            logger.warning(f"Invalid user_id for search: {user_id}")
            return None

        try:
            with get_db() as conn:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    SELECT id, username, password_hash, email, created_at
                    FROM users
                    WHERE id = ?
                    """,
                    (user_id,)
                )

                result = cursor.fetchone()

                if result:
                    return User(
                        id=result['id'],
                        username=result['username'],
                        password_hash=result['password_hash'],
                        email=result['email'],
                        created_at=datetime.fromisoformat(result['created_at'])
                    )

                return None

        except sqlite3.Error as e:
            logger.error(f"Database error finding user {user_id}: {str(e)}")
            return None

    def update_password(self, new_password: str) -> bool:
        """
        Update user password with secure hashing.

        SECURITY IMPROVEMENTS:
        - Hashes password before storage (DATA_ENCRYPTION)
        - Parameterized query prevents SQL injection (INPUT_VALIDATION)

        Args:
            new_password (str): New plain text password

        Returns:
            bool: True if successful, False otherwise

        Example:
            >>> user = User.find_by_username("john")
            >>> user.update_password("NewSecurePass456!")
            True
        """
        if not self.id:
            logger.error("Cannot update password for user without ID")
            return False

        try:
            # Hash the new password
            self.set_password(new_password)

            with get_db() as conn:
                cursor = conn.cursor()

                # SECURITY: Parameterized query prevents SQL injection
                cursor.execute(
                    "UPDATE users SET password_hash = ? WHERE id = ?",
                    (self.password_hash, self.id)
                )

                conn.commit()

                logger.info(f"Password updated for user {self.id}")
                return True

        except ValueError as e:
            logger.warning(f"Password validation failed for user {self.id}: {str(e)}")
            return False

        except sqlite3.Error as e:
            logger.error(f"Database error updating password for user {self.id}: {str(e)}")
            return False

        except Exception as e:
            logger.error(f"Unexpected error updating password for user {self.id}: {str(e)}")
            return False


class Session:
    """
    User session with secure token generation and expiration.

    SECURITY IMPROVEMENTS from vulnerable version:
    - Cryptographically secure token generation (uses secrets module)
    - Session expiration
    - Parameterized queries prevent SQL injection

    Attributes:
        id (int): Session ID
        user_id (int): Associated user ID
        token (str): Secure session token
        created_at (datetime): Session creation time
        expires_at (datetime): Session expiration time
    """

    def __init__(
        self,
        id: Optional[int] = None,
        user_id: int = 0,
        token: str = "",
        created_at: Optional[datetime] = None,
        expires_at: Optional[datetime] = None
    ):
        """
        Initialize Session instance.

        Args:
            id (int, optional): Session ID
            user_id (int): User ID
            token (str): Session token
            created_at (datetime, optional): Creation timestamp
            expires_at (datetime, optional): Expiration timestamp
        """
        self.id = id
        self.user_id = user_id
        self.token = token
        self.created_at = created_at or datetime.now()
        self.expires_at = expires_at or (datetime.now() + timedelta(hours=24))

    @staticmethod
    def create(user_id: int, expiration_hours: int = 24) -> Optional['Session']:
        """
        Create new session with cryptographically secure token.

        SECURITY IMPROVEMENTS:
        - Uses secrets module for cryptographically secure tokens
        - Includes expiration timestamp
        - Parameterized query prevents SQL injection

        Args:
            user_id (int): User ID to create session for
            expiration_hours (int): Hours until session expires (default: 24)

        Returns:
            Optional[Session]: Session instance if successful, None otherwise

        Example:
            >>> session = Session.create(user_id=123, expiration_hours=12)
            >>> print(session.token)
        """
        if not isinstance(user_id, int) or user_id <= 0:
            logger.warning(f"Invalid user_id for session creation: {user_id}")
            return None

        try:
            # SECURITY: Generate cryptographically secure token
            token = generate_token(32)

            created_at = datetime.now()
            expires_at = created_at + timedelta(hours=expiration_hours)

            with get_db() as conn:
                cursor = conn.cursor()

                # SECURITY: Parameterized query prevents SQL injection
                cursor.execute(
                    """
                    INSERT INTO sessions (user_id, token, created_at, expires_at)
                    VALUES (?, ?, ?, ?)
                    """,
                    (user_id, token, created_at, expires_at)
                )

                conn.commit()
                session_id = cursor.lastrowid

                logger.info(f"Session created for user {user_id} (expires in {expiration_hours}h)")

                return Session(
                    id=session_id,
                    user_id=user_id,
                    token=token,
                    created_at=created_at,
                    expires_at=expires_at
                )

        except sqlite3.Error as e:
            logger.error(f"Database error creating session for user {user_id}: {str(e)}")
            return None

        except Exception as e:
            logger.error(f"Unexpected error creating session for user {user_id}: {str(e)}")
            return None

    @staticmethod
    def find_by_token(token: str) -> Optional['Session']:
        """
        Find valid (non-expired) session by token.

        SECURITY: Only returns non-expired sessions

        Args:
            token (str): Session token

        Returns:
            Optional[Session]: Session if valid and not expired, None otherwise

        Example:
            >>> session = Session.find_by_token("abc123...")
            >>> if session:
            ...     print(f"Valid session for user {session.user_id}")
        """
        if not token:
            return None

        try:
            with get_db() as conn:
                cursor = conn.cursor()

                # SECURITY: Parameterized query, check expiration
                cursor.execute(
                    """
                    SELECT id, user_id, token, created_at, expires_at
                    FROM sessions
                    WHERE token = ? AND expires_at > ?
                    """,
                    (token, datetime.now())
                )

                result = cursor.fetchone()

                if result:
                    return Session(
                        id=result['id'],
                        user_id=result['user_id'],
                        token=result['token'],
                        created_at=datetime.fromisoformat(result['created_at']),
                        expires_at=datetime.fromisoformat(result['expires_at'])
                    )

                return None

        except sqlite3.Error as e:
            logger.error(f"Database error finding session: {str(e)}")
            return None

    def is_valid(self) -> bool:
        """
        Check if session is still valid (not expired).

        Returns:
            bool: True if session is valid, False if expired

        Example:
            >>> if session.is_valid():
            ...     print("Session is still active")
        """
        return datetime.now() < self.expires_at

    def revoke(self) -> bool:
        """
        Revoke (delete) this session.

        Returns:
            bool: True if successful, False otherwise

        Example:
            >>> session.revoke()  # Logout
        """
        if not self.id:
            return False

        try:
            with get_db() as conn:
                cursor = conn.cursor()

                cursor.execute("DELETE FROM sessions WHERE id = ?", (self.id,))
                conn.commit()

                logger.info(f"Session {self.id} revoked for user {self.user_id}")
                return True

        except sqlite3.Error as e:
            logger.error(f"Database error revoking session {self.id}: {str(e)}")
            return False
