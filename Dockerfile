FROM fedora:40

RUN dnf -y update && \
    dnf -y install rpm-build rpmdevtools make gcc tar gzip && \
    dnf -y clean all

# Create a builder user (optional but nice)
RUN useradd -m builder
USER builder
WORKDIR /home/builder
