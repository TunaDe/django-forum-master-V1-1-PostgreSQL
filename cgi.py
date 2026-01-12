# Compatibility shim for Python versions where the stdlib 'cgi' module was removed.
# Django 3.1 imports parse_header from cgi for parsing Content-Type headers.
# This minimal implementation covers the needs for request header parsing.
from __future__ import annotations
from typing import Dict, Tuple

def parse_header(line: str) -> Tuple[str, Dict[str, str]]:
    if not line:
        return "", {}
    # Split on semicolons respecting simple quoted values
    parts = []
    buf = []
    in_quote = False
    i = 0
    while i < len(line):
        ch = line[i]
        if ch == '"':
            in_quote = not in_quote
            buf.append(ch)
        elif ch == ';' and not in_quote:
            parts.append(''.join(buf))
            buf = []
        else:
            buf.append(ch)
        i += 1
    if buf:
        parts.append(''.join(buf))

    parts = [p.strip() for p in parts if p.strip()]
    if not parts:
        return "", {}

    value = parts[0].strip().lower()
    params: Dict[str, str] = {}
    for p in parts[1:]:
        if '=' in p:
            k, v = p.split('=', 1)
            k = k.strip().lower()
            v = v.strip().strip('"')
            params[k] = v
        else:
            params[p.strip().lower()] = ""
    return value, params
