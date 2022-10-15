#! /usr/bin/python3
import atheris
import sys
import io

with atheris.instrument_imports(exclude=["subprocess", "urllib", "urllib.parse"]):
    import isort


class SplitAwareFuzzedDataProvider(atheris.FuzzedDataProvider):
    def __init__(self, data, split_count: int):
        super(SplitAwareFuzzedDataProvider, self).__init__(data)
        self._chunk_size = len(data) // split_count

    def ConsumeByteSegment(self):
        return self.ConsumeBytes(self._chunk_size)

    def ConsumeStringSegment(self):
        return self.ConsumeString(self._chunk_size)


split_count = 4


@atheris.instrument_func
def TestOneInput(data):
    fdp = SplitAwareFuzzedDataProvider(data, split_count)

    try:
        isort.code(fdp.ConsumeStringSegment())

        # text_io = io.StringIO(fdp.ConsumeStringSegment())
        # isort.check_stream(text_io, True)
        #
        # isort.check_code(fdp.ConsumeStringSegment(), True)
        #
        # isort.find_imports_in_code(fdp.ConsumeStringSegment())
    except isort.exceptions.ISortError:
        pass


def main():
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()
