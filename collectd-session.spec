Summary:   collectd plugin for active ssh sessions
Name:      collectd-session
Version:   0.2.1
Release:   1%{?dist}
BuildArch: noarch
Source:    %{name}-%{version}.tgz
License:   ASL 2.0
URL:       https://gitlab.cern.ch/it-cm-lcs/collectd-session

Requires: collectd
Requires: python-utmp

%description
A python collectd plugin for active sessions. 
In particular it published KPI's for active ssh session in Cern and Non Cern 
network
summary.

%prep
%setup -q

%build
# Nothings to build

%install
mkdir -p %{buildroot}/usr/libexec/sensors
mkdir -p %{buildroot}/usr/share/collectd
install -m 0644 session.py       %{buildroot}/usr/libexec/sensors/session.py
%files
%dir /usr/libexec/sensors
/usr/libexec/sensors/session.py*

%doc README.md CHANGELOG.md

%changelog
* Mon Dec 4 2017 Steve Traylen <steve.traylen@cern.ch>
- New version.
