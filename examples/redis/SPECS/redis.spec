Name:           redis
Version:        7.2.4
Release:        1%{?dist}
Summary:        In-memory key-value data store

License:        BSD
URL:            https://redis.io
Source0:        https://download.redis.io/releases/redis-%{version}.tar.gz
Source1:        redis.service
Source2:        redis.logrotate

BuildRequires:  gcc
BuildRequires:  make
Requires:       systemd

%description
Redis is an in-memory key-value data store with optional persistence.

%prep
%setup -q

%build
make BUILD_TLS=no

%install
rm -rf %{buildroot}

# Create directories
install -d %{buildroot}/usr/bin
install -d %{buildroot}/etc/redis
install -d %{buildroot}/var/lib/redis
install -d %{buildroot}/var/log/redis
install -d %{buildroot}/usr/lib/systemd/system
install -d %{buildroot}/etc/logrotate.d

# Install binaries
install -m 0755 src/redis-server %{buildroot}/usr/bin/
install -m 0755 src/redis-cli %{buildroot}/usr/bin/

# Install default config
install -m 0644 redis.conf %{buildroot}/etc/redis/redis.conf

# Install external files
install -m 0644 %{SOURCE1} %{buildroot}/usr/lib/systemd/system/redis.service
install -m 0644 %{SOURCE2} %{buildroot}/etc/logrotate.d/redis

%pre
getent group redis >/dev/null || groupadd -r redis
getent passwd redis >/dev/null || \
    useradd -r -g redis -d /var/lib/redis -s /sbin/nologin \
    -c "Redis user" redis

%post
systemctl daemon-reload
systemctl enable redis.service >/dev/null 2>&1 || :

%preun
if [ $1 -eq 0 ]; then
    systemctl disable redis.service >/dev/null 2>&1 || :
    systemctl stop redis.service >/dev/null 2>&1 || :
fi

%files
/usr/bin/redis-server
/usr/bin/redis-cli
%config(noreplace) /etc/redis/redis.conf
/usr/lib/systemd/system/redis.service
/etc/logrotate.d/redis
/var/lib/redis
/var/log/redis

%changelog
* Tue Feb 18 2026 Anand Siva <you@example.com> - 7.2.4-1
- Initial Redis RPM example

