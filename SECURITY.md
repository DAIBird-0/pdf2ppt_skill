# Security And Privacy

This project handles research PDFs and generated presentation artifacts. Treat those inputs as private unless the user explicitly says they are public.

Please do not report private papers or generated decks in public issues. Open a private advisory or contact the maintainer if a vulnerability could expose local files, paper contents, tokens, API keys, or personal metadata.

Before publishing or sharing outputs, run:

```bash
python scripts/audit_privacy.py .
```

The audit checks text files and PPTX internals for common personal information, absolute local paths, secrets, and undeclared demo content.

