%global with_debug 0
%global with_check 0

%if 0%{?with_debug}
%global _find_debuginfo_dwz_opts %{nil}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package %{nil}
%endif

%define provider github
%define provider_tld com
%define project containers
%define repo conmon
# https://github.com/containers/conmon
%define import_path %{provider}.%{provider_tld}/%{project}/%{repo}
%define commit0 7a830be343876ac381c965c7429a7fb9b3d7a609
%define shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%define git0 https://%{import_path}

# Used for comparing with latest upstream tag
# to decide whether to autobuild (non-rawhide only)
%define built_tag v2.0.11
%define built_tag_strip %(b=%{built_tag}; echo ${b:1})

Name: %{repo}
Epoch: 2
Version: 2.0.11
Release: 1%{?dist}
Summary: OCI container runtime monitor
License: ASL 2.0
URL: %{git0}
Source0: %{url}/archive/%{built_tag}.tar.gz
BuildRequires: gcc
BuildRequires: git
BuildRequires: glib2-devel

%description
%{summary}.

%prep
%autosetup -Sgit -n %{name}-%{built_tag_strip}

%build
%{__make} all

%install
%{__make} PREFIX=%{buildroot}%{_prefix} install install.crio

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_libexecdir}/crio/%{name}

%changelog
* Wed Mar 11 2020 Alberto Chiusole <bebo.sudo@gmail.com> - 2:2.0.11-1
- update to 2.0.11


* Mon Dec 16 2019 Jindrich Novy <jnovy@redhat.com> - 2:2.0.8-1
- bump to v2.0.8

* Mon Oct 21 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.0.2-1
- bump to v2.0.2

* Wed Sep 25 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.0.1-1
- Resolves: #1753594, #1753671
- bump to v2.0.1

* Tue Sep 10 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.0.0-2
- remove BR: go-md2man since no manpages yet

* Tue Sep 10 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.0.0-1
- bump to v2.0.0

* Fri May 31 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:0.2.0-1
- initial package
