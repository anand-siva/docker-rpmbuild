# Redis RPM Example

This example demonstrates how to package Redis as an RPM using docker-rpmbuild.

## 1. Download Redis Source

From the root of the repo:

wget https://download.redis.io/releases/redis-7.2.4.tar.gz
mkdir -p rpmbuild/SOURCES
mv redis-7.2.4.tar.gz rpmbuild/SOURCES/

## 2. Copy Spec File

mkdir -p rpmbuild/SPECS
cp examples/redis/SPECS/redis.spec rpmbuild/SPECS/

## 3. Build Inside Docker

docker run --rm -it \
  -v "$PWD/rpmbuild:/home/builder/rpmbuild" \
  -w /home/builder/rpmbuild \
  docker-rpmbuild \
  rpmbuild -ba SPECS/redis.spec

## 4. Install

sudo rpm -ivh rpmbuild/RPMS/x86_64/redis-*.rpm

