# Security Policy

## Supported Versions

| Version | Supported |
|---|---|
| latest (`main`) | ✅ |

## Reporting a Vulnerability

Please **do not** open a public GitHub issue for security vulnerabilities.

Instead, report them via email to **ryanjbush@gmail.com** with the subject line `[SECURITY] Orion AI — <brief description>`.

Include:
- A description of the vulnerability and its potential impact
- Steps to reproduce
- Any suggested remediation if known

You can expect an acknowledgement within **48 hours** and a resolution timeline within **7 days** for critical issues.

## Agent Tool Safety

This platform allows agents to invoke registered tools. If you discover a prompt injection, tool misuse, or sandbox escape vulnerability that could allow an agent to execute unintended actions, treat this as **critical** and disclose immediately.

## API Key Safety

This project uses LLM API keys. **Never commit API keys to this repository.** Use `.env` files excluded via `.gitignore`. If a key has been accidentally committed, rotate it immediately.

## Scope

This project is a portfolio/demonstration platform and is not deployed as a public service.
