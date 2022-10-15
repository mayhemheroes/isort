#! /usr/bin/python3
import atheris
import sys
import io

with atheris.instrument_imports():
    import isort



@atheris.instrument_func
def TestOneInput(data):

    try:
        isort.code(str(data))

    except isort.exceptions.ISortError:
        pass


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
