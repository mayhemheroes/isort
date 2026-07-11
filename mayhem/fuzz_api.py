#! /usr/bin/env python3
"""Atheris fuzz harness for isort's public API.

Preserved from the original mayhemheroes/isort integration (target `api-fuzz`): feed
arbitrary text to isort.code() / isort.check_code() and let Atheris/libFuzzer hunt for
crashes the parser/sorter doesn't guard with ISortError. Launched by Mayhem via the
`/mayhem/isort-fuzz` ELF shim (mayhem/launcher.c), which exec()s `python3` on this file
forwarding the libFuzzer argv, so this process IS the libFuzzer target.
"""
import sys

import atheris

with atheris.instrument_imports(include=["isort"]):
    import isort
    import isort.api
    import isort.exceptions


def TestOneInput(data):
    try:
        fdp = atheris.FuzzedDataProvider(data)
        code = fdp.ConsumeUnicode(fdp.remaining_bytes())
        if fdp.ConsumeBool():
            isort.check_code(code)
        else:
            isort.code(code)
    except isort.exceptions.ISortError:
        pass


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
