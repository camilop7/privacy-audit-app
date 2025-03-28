# 🧠 Privacy Audit App – Architecture Overview

## 🧱 Core Components

- **Frontend (React)**: Interface for scan input and viewing reports
- **Backend (FastAPI)**:
  - API endpoints for scans, auth, user data
  - Script & content analysis engine
  - Malware pattern detection
- **PostgreSQL DB**:
  - Users, scans, URLs, risk scores, audit trails
- **Tor Integration**:
  - SOCKS5 proxy routing via `127.0.0.1:9050`
  - Onion domain support

## 🏗️ Planned Additions

- File uploads (malware scan)
- ML module for JS classification
- Email phishing detection (TBD)
- Admin portal + user permission roles

## 🔐 Security Hardening

- 2FA auth (TOTP / email OTP)
- JWT auth with token expiration
- Sandbox risky requests (VM / Docker)
- Remove `eval`, `Function`, and external script execution
