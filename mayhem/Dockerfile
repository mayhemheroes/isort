FROM python:3.12-bullseye

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y clang
RUN pip3 install atheris

ADD . /src
WORKDIR /src
RUN SETUPTOOLS_SCM_PRETEND_VERSION=5.10.1 python3 -m pip install .

CMD ["/src/mayhem/fuzz_api.py"]
