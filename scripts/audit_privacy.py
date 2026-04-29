from __future__ import annotations

import argparse
import html
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path


TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".yaml",
    ".yml",
    ".json",
    ".py",
    ".toml",
    ".cfg",
    ".ini",
    ".csv",
}

SKIP_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "node_modules",
}

SKIP_FILE_PREFIXES = ("~$",)

SELF_PATH = "scripts/audit_privacy.py"

PERSONAL_PATTERNS = [
    (re.compile(r"\bckkkk\b", re.I), "local Windows username"),
    (re.compile(r"\bk\s+c\b", re.I), "PPT author metadata from local machine"),
    (re.compile(r"C:\\Users\\[^\\\s<>\"']+", re.I), "absolute Windows user path"),
    (re.compile(r"D:\\Postgraduate\\[^\\\s<>\"']*", re.I), "local workspace path"),
    (re.compile(r"/Users/[^/\s<>\"']+", re.I), "absolute macOS user path"),
    (re.compile(r"/home/[^/\s<>\"']+", re.I), "absolute Linux user path"),
    (
        re.compile(
            r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
            re.I,
        ),
        "email address",
    ),
    (re.compile(r"(?<!\d)(?:\+?86[-\s]?)?1[3-9]\d{9}(?!\d)"), "China mobile phone number"),
]

SECRET_PATTERNS = [
    (re.compile(r"(?i)(api[_-]?key|secret|password|access[_-]?token)\s*[:=]\s*['\"]?[^'\"\s]{8,}"), "possible secret assignment"),
    (re.compile(r"(?i)bearer\s+[A-Za-z0-9._~+/=-]{20,}"), "bearer token"),
    (re.compile(r"sk-[A-Za-z0-9_-]{20,}"), "OpenAI-style API key"),
    (re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"), "GitHub token"),
]

THIRD_PARTY_TERMS = re.compile(r"\b(ELLMob|EventMob|Yusong Wang|ICLR 2026)\b", re.I)
THIRD_PARTY_ALLOWED_PATHS = (
    "THIRD_PARTY_NOTICES.md",
    "README.md",
    "marketing/",
    "examples/ellmob-demo/",
)


@dataclass
class Finding:
    path: str
    detail: str
    snippet: str


def normalize_path(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def is_skipped(path: Path) -> bool:
    return any(part in SKIP_DIRS for part in path.parts)


def is_third_party_allowed(rel: str) -> bool:
    return any(rel == item or rel.startswith(item) for item in THIRD_PARTY_ALLOWED_PATHS)


def snippet(text: str, start: int, end: int) -> str:
    left = max(0, start - 60)
    right = min(len(text), end + 80)
    value = text[left:right].replace("\n", " ")
    return re.sub(r"\s+", " ", value).strip()


def scan_text(rel: str, text: str) -> list[Finding]:
    findings: list[Finding] = []
    for pattern, label in [*PERSONAL_PATTERNS, *SECRET_PATTERNS]:
        for match in pattern.finditer(text):
            findings.append(Finding(rel, label, snippet(text, match.start(), match.end())))

    if THIRD_PARTY_TERMS.search(text) and not is_third_party_allowed(rel):
        match = THIRD_PARTY_TERMS.search(text)
        assert match is not None
        findings.append(
            Finding(
                rel,
                "third-party paper/demo term outside declared demo paths",
                snippet(text, match.start(), match.end()),
            )
        )

    return findings


def pptx_text_chunks(path: Path) -> list[tuple[str, str]]:
    chunks: list[tuple[str, str]] = []
    with zipfile.ZipFile(path) as archive:
        for name in archive.namelist():
            if not name.endswith((".xml", ".rels")):
                continue
            if not name.startswith(("docProps/", "ppt/slides/", "ppt/notesSlides/", "ppt/comments/", "ppt/_rels/")):
                continue
            raw = archive.read(name)
            text = raw.decode("utf-8", errors="replace")
            visible = html.unescape(re.sub(r"<[^>]+>", " ", text))
            visible = re.sub(r"\s+", " ", visible).strip()
            if visible:
                chunks.append((name, visible))
    return chunks


def scan_file(path: Path, root: Path) -> list[Finding]:
    rel = normalize_path(path, root)
    suffix = path.suffix.lower()

    if suffix == ".pptx":
        findings: list[Finding] = []
        for member, text in pptx_text_chunks(path):
            member_rel = f"{rel}!{member}"
            findings.extend(scan_text(member_rel, text))
        return findings

    if suffix in TEXT_EXTENSIONS:
        if rel == SELF_PATH:
            return []
        text = path.read_text(encoding="utf-8", errors="replace")
        return scan_text(rel, text)

    return []


def iter_files(root: Path) -> list[Path]:
    return [
        path
        for path in root.rglob("*")
        if path.is_file()
        and not is_skipped(path.relative_to(root))
        and not path.name.startswith(SKIP_FILE_PREFIXES)
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit repository files and PPTX internals for privacy leaks.")
    parser.add_argument("root", nargs="?", default=".", help="Repository root to scan.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    findings: list[Finding] = []
    for path in iter_files(root):
        findings.extend(scan_file(path, root))

    if findings:
        print("Privacy audit failed:\n")
        for item in findings:
            print(f"- {item.path}: {item.detail}")
            print(f"  {item.snippet}")
        return 1

    print("Privacy audit passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
