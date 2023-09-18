# Copyright © 2023, Indiana University
# BSD 3-Clause License

"""
Patch the `jinja2` `collections.abc.Mapping` issue in Python 3.10, 3.11

Usage
-----

python patch_jinja.py

When to use
-----------

If you run `python -m flask --version` and see something like:

```
ImportError: cannot import name 'Mapping' from 'collections'
```
"""

import os
import sys


def get_major_minor():
    """Return (major_version: int, minor_version: int) tuple of the Python interpreter."""
    major, minor, *_ = sys.version_info
    return major, minor


if __name__ == "__main__":
    major, minor = get_major_minor()

    if (major, minor) == (3, 10):
        file_path = os.path.join(
            "venv", "lib", "python3.10", "site-packages", "jinja2", "tests.py"
        )
    elif (major, minor) == (3, 11):
        file_path = os.path.join(
            "venv", "lib", "python3.11", "site-packages", "jinja2", "tests.py"
        )
    else:
        sys.stderr.write("This should only be ran when using python-3.10 or 3.11")
        sys.exit(1)

    with open(file_path, mode="r", encoding="utf-8-sig", newline="") as fh:
        data = fh.read()

    with open(file_path, mode="w", encoding="utf-8-sig", newline="") as fh:
        fh.write(
            data.replace(
                "from collections import Mapping", "from collections.abc import Mapping"
            )
        )

    sys.stdout.write(f"Patched {file_path}\n")
    sys.exit(0)
