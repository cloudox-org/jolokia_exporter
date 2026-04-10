%global debug_package %{nil}
%global user prometheus
%global group prometheus

Name: jolokia_exporter
Version: 1.3.1
Release: 2%{?dist}
Summary: Prometheus exporter for jolokia metrics
License: MIT
URL:     https://github.com/jaxxstorm/jolokia_exporter

Source0: https://github.com/jaxxstorm/jolokia_exporter/releases/download/%{version}/%{name}_%{version}_Linux_x86_64.tar.gz
Source1: %{name}.unit
Source2: %{name}.default

%{?systemd_requires}
Requires(pre): shadow-utils

%description
Export jolokia metrics to Prometheus.

%prep
%setup -q -D -c %{name}_%{version}

%build
/bin/true

%install
mkdir -vp %{buildroot}%{_sharedstatedir}/prometheus
install -D -m 755 %{name} %{buildroot}%{_bindir}/%{name}
install -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/default/%{name}
install -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/%{name}.service

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
useradd -r -g prometheus -d %{_sharedstatedir}/prometheus -s /sbin/nologin -c "Prometheus services" prometheus
exit 0

%post
%systemd_post %{name}.service

%preun
%systemd_preun %{name}.service

%postun
%systemd_postun %{name}.service

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/default/%{name}
%dir %attr(755, %{user}, %{group}) %{_sharedstatedir}/prometheus
%{_unitdir}/%{name}.service

%changelog
* Fri Apr 10 2026 Ivan Garcia <igarcia@cloudox.org> - 1.3.1
- Initial packaging for the 1.13.1 branch
