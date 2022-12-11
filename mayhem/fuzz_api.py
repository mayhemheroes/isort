#! /usr/bin/python3
import atheris
import sys
import io

import isort
import isort.api
import isort.exceptions


@atheris.instrument_func
def TestOneInput(data):
    try:
        fdp = atheris.FuzzedDataProvider(data)
        isort.code(fdp.ConsumeUnicodeNoSurrogates(fdp.remaining_bytes()))

    except isort.exceptions.ISortError:
        pass


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
