%global with_debug 0
%global with_check 0

%if 0%{?with_debug}
%global _find_debuginfo_dwz_opts %{nil}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package %{nil}
%endif

%global provider github
%global provider_tld com
%global project containers
%global repo conmon
# https://github.com/containers/conmon
%global import_path %{provider}.%{provider_tld}/%{project}/%{repo}
%global commit0 5ca7df27cb3a6f1edaab1a40fcc61cc6c16d9308
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global git0 https://%{import_path}

# Used for comparing with latest upstream tag
# to decide whether to autobuild (non-rawhide only)
#%%global built_tag v2.0.2

Name: %{repo}
Epoch: 2
Version: 2.0.8
Release: 1%{?dist}
Summary: OCI container runtime monitor
License: ASL 2.0
URL: %{git0}
Source0: %{git0}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz
BuildRequires: gcc
BuildRequires: git
BuildRequires: glib2-devel

%description
%{summary}.

%prep
%autosetup -Sgit -n %{name}-%{commit0}

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
