# Security Policy

## Supported versions

| Version | Supported |
| --- | --- |
| design.v1 (this repository) | Yes |

## Reporting a vulnerability

If you discover a security issue in tooling, examples, or documentation that
could expose secrets or enable unsafe agent behavior:

1. **Do not** open a public GitHub issue.
2. Email **harshitkhemani@gmail.com** with a description and reproduction steps.
3. Allow reasonable time for a fix before public disclosure.

`.design` files MUST NOT contain secrets, private tokens, or credentials.
Agents encountering secrets in a `.design` file SHOULD refuse to commit them
and warn the user.
