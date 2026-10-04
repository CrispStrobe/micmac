#!/usr/bin/env python3
"""Run the checkout's native mm3d with native Tapioca detector/matcher defaults."""
import os
import sys
from pathlib import Path


def command(arguments, source_root=None):
    root = Path(source_root) if source_root is not None else Path(__file__).resolve().parents[2]
    arguments = list(arguments)
    if len(arguments) >= 2 and arguments[0] == "Tapioca" and arguments[1] in {
        "All", "Line", "MulScale", "File", "Graph"
    }:
        for key, value in (("Detect", "mm3d:Digeo"), ("Match", "mm3d:Ann")):
            if not any(arg.startswith(key + "=") for arg in arguments[2:]):
                arguments.append(key + "=" + value)
    return [str(root / "bin" / "mm3d"), *arguments]


if __name__ == "__main__":
    argv = command(sys.argv[1:])
    if not os.access(argv[0], os.X_OK):
        raise SystemExit("Build the native executable first: " + argv[0])
    os.execv(argv[0], argv)
