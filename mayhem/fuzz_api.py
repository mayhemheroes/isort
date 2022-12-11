#! /usr/bin/env python3
import atheris
import sys
import io

with atheris.instrument_imports(include=['isort']):
    import isort
    import isort.api
    import isort.exceptions


def TestOneInput(data):
    try:
        fdp = atheris.FuzzedDataProvider(data)
        isort.find_imports_in_code(fdp.ConsumeUnicode(fdp.ConsumeIntInRange(1, 1000)))
        isort.code(fdp.ConsumeUnicode(fdp.remaining_bytes()))
    except isort.exceptions.ISortError:
        pass


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
