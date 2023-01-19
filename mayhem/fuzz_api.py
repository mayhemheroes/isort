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
