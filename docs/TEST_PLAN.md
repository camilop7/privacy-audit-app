# Test Strategy (TDD)

## Goals

- Keep system safe while iterating fast
- Run isolated tests before exposing real API

## Environments

- `dev`: local, with mock Tor and PostgreSQL
- `sandbox`: local Docker container, full feature test
- `prod`: cloud, locked with 2FA + admin roles

## Tests

- [ ] ✅ Scan a safe site
- [ ] ❌ Scan a broken/malicious site (expect error)
- [ ] 🧪 Upload malicious JS file (quarantine test)
- [ ] 👤 Create/read/update/delete users
- [ ] 🔐 Ensure JWT + permissions respected
