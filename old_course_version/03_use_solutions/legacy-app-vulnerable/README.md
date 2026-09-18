# Legacy Application - VULNERABLE VERSION ⚠️

## ⚠️ SECURITY WARNING ⚠️

**THIS CODE CONTAINS INTENTIONAL SECURITY VULNERABILITIES FOR EDUCATIONAL PURPOSES ONLY**

This application is designed to demonstrate common security vulnerabilities and should **NEVER** be used in production or connected to real data.

---

## Purpose

This vulnerable version demonstrates multiple security anti-patterns that violate CLAUDE.md development rules. It serves as a teaching tool to help developers recognize and understand common security issues.

---

## Known Security Vulnerabilities

### 🔴 CRITICAL Violations of CLAUDE.md Rules

#### 1. Hardcoded Secrets (Violates: NO_SECRETS_IN_CODE)
**Files:** `app.py` (lines 13-17), `utils.py` (lines 11-12)

```python
# app.py
API_KEY = "sk_live_abc123xyz789"  # ❌ Hardcoded API key
DB_USER = "admin"                  # ❌ Hardcoded credentials
DB_PASS = "Password123"            # ❌ Hardcoded credentials

# utils.py
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"  # ❌ Hardcoded AWS credentials
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
```

**Impact:** Credentials exposed in source code, version control, and logs
**CLAUDE.md Rule:** NO_SECRETS_IN_CODE - Never hard-code credentials in source code

---

#### 2. SQL Injection Vulnerabilities (Violates: INPUT_VALIDATION)
**Files:** `app.py` (lines 26, 43, 64, 80)

```python
# ❌ String concatenation allows SQL injection
query = "SELECT * FROM users WHERE id = " + id
query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
query = f"SELECT * FROM users WHERE name LIKE '%{search_term}%'"
query = f"DELETE FROM users WHERE id = {user_id}"
```

**Impact:** Attackers can extract, modify, or delete any data in the database
**CLAUDE.md Rule:** INPUT_VALIDATION - Must sanitize and validate all user inputs

**Example Attack:**
```bash
# Extract all user data
curl "http://localhost:5000/users/1 OR 1=1--"

# Drop entire table
curl "http://localhost:5000/users/1; DROP TABLE users;--"
```

---

#### 3. Plain Text Password Storage (Violates: DATA_ENCRYPTION)
**Files:** `app.py` (line 37), `utils.py` (line 31)

```python
# ❌ Passwords stored in plain text
password = request.form['password']  # No hashing

# ❌ MD5 is cryptographically broken for passwords
return hashlib.md5(password.encode()).hexdigest()
```

**Impact:** All passwords compromised if database is breached
**CLAUDE.md Rule:** DATA_ENCRYPTION - Must implement data encryption for sensitive data

---

#### 4. Missing Authentication/Authorization (Violates: LEAST_PRIVILEGE)
**Files:** `app.py` (lines 72-85)

```python
@app.route('/admin/delete/<user_id>')
def delete_user(user_id):
    # ❌ No authentication check - anyone can delete users!
```

**Impact:** Unauthenticated users can delete any user account
**CLAUDE.md Rule:** LEAST_PRIVILEGE - Follow principle of least privilege

---

### 🟠 HIGH Priority Violations

#### 5. No Error Handling (Violates: ERROR_HANDLING)
**Files:** All files

```python
# ❌ No try-catch blocks, errors expose internal details
response = requests.post('https://api.emailservice.com/send',
                       headers=headers, json=data)
```

**Impact:** Application crashes expose stack traces and internal details
**CLAUDE.md Rule:** ERROR_HANDLING - Must include comprehensive error handling

---

#### 6. Poor Logging Practices (Violates: LOGGING)
**Files:** `utils.py` (lines 58-67)

```python
# ❌ Logs may contain sensitive data
logging.info(f"User {user_id} performed: {action}")

# ❌ World-readable log file
with open('/tmp/app.log', 'a') as f:
    f.write(f"User {user_id}: {action}\n")
```

**Impact:** Sensitive data in logs, insecure file permissions
**CLAUDE.md Rule:** LOGGING - Implement structured logging with appropriate levels

---

#### 7. Insecure Defaults (Violates: Multiple Rules)
**Files:** `app.py` (line 113)

```python
# ❌ Debug mode in production, binding to all interfaces
app.run(debug=True, host='0.0.0.0', port=5000)
```

**Impact:** Debug mode exposes code, running on all interfaces allows external access
**CLAUDE.md Rule:** Multiple violations

---

## How to Use This for Learning

1. **Review the code** and identify vulnerabilities
2. **Compare with the secure version** in `../legacy-app-secure/`
3. **Read SECURITY-COMPARISON.md** for side-by-side analysis
4. **Never deploy this code** - it's for educational purposes only

---

## For Instructors

Use this code to demonstrate:
- Why AI agents need up-to-date security knowledge
- How static code analysis can identify vulnerabilities
- The importance of following security best practices
- Real-world consequences of poor security practices

Point students to the secure version to see proper implementations.

---

## Comparison

| Vulnerability | This Version | Secure Version |
|---------------|--------------|----------------|
| Secrets | Hardcoded | Environment variables |
| SQL Injection | Vulnerable | Parameterized queries |
| Passwords | Plain text/MD5 | Argon2 hashing |
| Authentication | None | Proper auth checks |
| Error Handling | None | Comprehensive try-catch |
| Logging | Insecure | Structured with levels |
| Configuration | Hardcoded | Environment-based |

---

## DO NOT

- ❌ Use this code in production
- ❌ Connect to real databases
- ❌ Store real user data
- ❌ Deploy to public servers
- ❌ Commit real credentials

## DO

- ✅ Use for education and training
- ✅ Demonstrate vulnerability scanning
- ✅ Compare with secure version
- ✅ Learn from the mistakes
- ✅ Follow CLAUDE.md rules in real projects

---

## Related Files

- **Secure Version:** `../legacy-app-secure/`
- **Comparison Document:** `../SECURITY-COMPARISON.md`
- **CLAUDE.md Rules:** `/Users/csmith/.claude/CLAUDE.md`

---

**Last Updated:** 2025-10-27
**Purpose:** Educational demonstration of security vulnerabilities
