# syntax=docker/dockerfile:1.7
#
# Commit-image Dockerfile (SMALL form) — builds ON TOP of the org base image
# (ghcr.io/mayhemheroes/base). The base provides debian + clang/llvm + libFuzzer + Python 3 + the
# identities + the build-contract ENV. isort (PyCQA/isort) is a PURE-PYTHON package, so this image
# installs the Atheris harness's Python deps (atheris, the package itself) plus pytest into the
# base's system Python as root, then (as the non-root `mayhem` user) compiles the ELF launcher shims
# and runs the real pytest known-answer suite via build.sh / test.sh.
#
# Build (from the repo root):
#   DOCKER_BUILDKIT=1 docker build -f mayhem/Dockerfile \
#       --build-arg COMMIT=$(git rev-parse HEAD) \
#       [--build-arg SOURCE_DATE_EPOCH=$(date +%s)] \
#       -t isort-commit:test .

FROM ghcr.io/mayhemheroes/base:20260621

ARG COMMIT
ARG REPO_URL
# SOURCE_DATE_EPOCH stays an ARG (available to build.sh); never bake it as ENV — an empty value
# breaks clang. build.sh unsets it when empty.
ARG SOURCE_DATE_EPOCH
# Declared for parity with the build contract; isort has no native code to sanitize.
ARG SANITIZER_FLAGS

# Atheris (the libFuzzer harness engine — builds a native module against the base's clang/libFuzzer)
# and pytest (the build-time + verify-repo test oracle) go into the base's SYSTEM Python. PEP 668
# marks that interpreter externally-managed, so --break-system-packages. This is the (networked)
# install step; build.sh deliberately does NOT pip-install, so its offline PATCH-tier re-run stays
# air-gapped.
USER root
RUN pip install --no-cache-dir --break-system-packages 'atheris==3.1.0' pytest

# Source enters from the build CONTEXT (the CI checkout): the FULL repo (incl. .git history)
# is copied to /mayhem as `mayhem`; build.sh builds in place. (mayhem/Dockerfile.dockerignore keeps
# .git in the context so the commit image holds the full mayhem-branch history.)
WORKDIR /mayhem
COPY --chown=2000:2000 . /mayhem

# Install isort itself so the harness/oracle can `import isort`. isort uses hatchling + hatch-vcs;
# pin a pretend version so the build never needs to resolve a tag from git history. Also install the
# two in-repo example plugins (a shared profile + a sorting plugin via entry points) so the
# known-answer suite's plugin-machinery tests (issue #970 / #1732) exercise real behavior.
RUN SETUPTOOLS_SCM_PRETEND_VERSION=5.10.1 \
    pip install --no-cache-dir --break-system-packages \
        . ./example_shared_isort_profile ./example_isort_sorting_plugin

USER mayhem

# Compile the ELF launcher shims (Mayhem needs an ELF target, not a .py).
RUN bash mayhem/build.sh

# Run isort's real pytest known-answer suite at build time; a failing suite fails the build.
RUN if [ -f mayhem/test.sh ]; then bash mayhem/test.sh; else echo "no mayhem/test.sh"; fi

LABEL org.opencontainers.image.source="${REPO_URL}" \
      org.opencontainers.image.revision="${COMMIT}" \
      rlenv.tier="commit" \
      rlenv.source_date_epoch="${SOURCE_DATE_EPOCH}" \
      rlenv.user="mayhem"

USER mayhem
WORKDIR /mayhem
