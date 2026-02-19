# docker-rpmbuild

Minimal Docker image for building RPMs with Fedora tooling.

## What is this?

This repo builds a Fedora 40 based image with the standard RPM build toolchain
(`rpm-build`, `rpmdevtools`, `gcc`, `make`, `tar`, `gzip`). It is intended for
running `rpmbuild` against a mounted `rpmbuild` tree from your host.

## Build the image

From the repo root:

```sh
docker build -t docker-rpmbuild .
```

## Basic usage

Use a local `rpmbuild/` directory and run `rpmbuild` inside the container:

```sh
mkdir -p rpmbuild/{SOURCES,SPECS}
docker run --rm -it \
  -v "$PWD/rpmbuild:/home/builder/rpmbuild" \
  -w /home/builder/rpmbuild \
  docker-rpmbuild \
  rpmbuild -ba SPECS/your.spec
```

## Example: build Redis

The `examples/redis` folder includes a working spec file and a walkthrough.
Below is a compact version of the same flow using that example.

```sh
mkdir -p rpmbuild/SOURCES
wget https://download.redis.io/releases/redis-7.2.4.tar.gz
mv redis-7.2.4.tar.gz rpmbuild/SOURCES/
cp examples/redis/SOURCES/redis.service rpmbuild/SOURCES/
cp examples/redis/SOURCES/redis.logrotate rpmbuild/SOURCES/

mkdir -p rpmbuild/SPECS
cp examples/redis/SPECS/redis.spec rpmbuild/SPECS/

docker run --rm -it \
  -v "$PWD/rpmbuild:/home/builder/rpmbuild" \
  -w /home/builder/rpmbuild \
  docker-rpmbuild \
  rpmbuild -ba SPECS/redis.spec

sudo rpm -ivh rpmbuild/RPMS/x86_64/redis-*.rpm
```

For more detail, see `examples/redis/README.md`.

## Final rpmbuild state

```bash
└── rpmbuild
    ├── BUILD
    ├── BUILDROOT
    ├── RPMS
    │   └── aarch64
    │       ├── redis-7.2.4-1.fc40.aarch64.rpm
    │       ├── redis-debuginfo-7.2.4-1.fc40.aarch64.rpm
    │       └── redis-debugsource-7.2.4-1.fc40.aarch64.rpm
    ├── SOURCES
    │   ├── redis-7.2.4.tar.gz
    │   ├── redis.logrotate
    │   └── redis.service
    ├── SPECS
    │   └── redis.spec
    └── SRPMS
        └── redis-7.2.4-1.fc40.src.rpm
```
