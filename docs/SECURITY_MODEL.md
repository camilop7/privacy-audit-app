# Security Model

## Isolation

- All `.onion` traffic routed via Tor SOCKS proxy.
- Dangerous content never rendered client-side.

## Threat Model

| Vector             | Mitigation |
|--------------------|------------|
| Eval/Function() JS | Analyzer blocks and logs |
| File uploads       | Will sandbox in VM/Docker |
| Script injection   | Frontend uses React’s safety features |
| API abuse          | Protected by auth + rate limits (planned) |
| Real user exposure | Login & device info encrypted in DB |

## Plans

- TailsOS / Docker for dangerous payload testing
- Logging of blacklisted 3rd-party services
