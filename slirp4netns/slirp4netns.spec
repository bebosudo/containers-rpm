%global git0 https://github.com/rootless-containers/%{name}
%global commit0 bbd6f25c70d5db2a1cd3bfb0416a8db99a75ed7e
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

# Used for comparing with latest upstream tag
# to decide whether to autobuild (non-rawhide only)
%global built_tag v0.4.0-beta.2

Name: slirp4netns
Version: 0.4.0
Release: 20.1.dev.git%{shortcommit0}%{?dist}
# no go-md2man in ppc64
ExcludeArch: ppc64
Summary: slirp for network namespaces
License: GPLv2
URL: %{git0}
Source0: %{git0}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: glib2-devel
BuildRequires: git
BuildRequires: libcap-devel
BuildRequires: make
%if 0%{?rhel} > 7 || 0%{?fedora}
BuildRequires: golang-github-cpuguy83-md2man
%else
BuildRequires: golang-github-cpuguy83-go-md2man
%endif

%description
slirp for network namespaces, without copying buffers across the namespaces.

%package devel
Summary: %{summary}
BuildArch: noarch

%description devel
%{summary}

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.

%prep
%autosetup -Sgit -n %{name}-%{commit0}

%build
./autogen.sh
./configure --prefix=%{_usr} --libdir=%{_libdir}
%{__make} generate-man

%install
make DESTDIR=%{buildroot} install install-man

%check

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.gz

%changelog
* Sun Aug 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-20.1.dev.gitbbd6f25
- autobuilt bbd6f25

* Thu Aug 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-19.1.dev.gited51817
- autobuilt ed51817

* Tue Jul 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-18.1.dev.gitaacef69
- autobuilt aacef69

* Tue Jul 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-17.1.dev.git1dfc6f6
- autobuilt 1dfc6f6

* Sun Jul 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-16.1.dev.git96ff33c
- autobuilt 96ff33c

* Sat Jul 27 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-15.1.dev.gitb911c9a
- autobuilt b911c9a

* Sat Jul 27 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-14.1.dev.gitd23723e
- autobuilt d23723e

* Fri Jul 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-13.1.dev.git10c0ee5
- autobuilt 10c0ee5

* Thu Jul 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-12.1.dev.git87a4bf7
- autobuilt 87a4bf7

* Wed Jul 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-11.1.dev.git85efff0
- autobuilt 85efff0

* Wed Jul 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-10.1.dev.git4f5a083
- autobuilt 4f5a083

* Tue Jul 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.0-9.1.dev.git62cbdd3
- bump to 0.4.0
- autobuilt 62cbdd3

* Tue Jul 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.3.0-8.1.dev.gitbf199bb
- autobuilt bf199bb

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.3.0-7.1.dev.git2f857ec
- autobuilt 5c690f7
- autobuilt 2f857ec

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.3.0-6.1.dev.gitd34e916
- autobuilt 5c690f7
- autobuilt d34e916

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.3.0-5.1.dev.git6612517
- autobuilt 5c690f7
- autobuilt 6612517

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.3.0-4.1.dev.gitf34ad90
- autobuilt 5c690f7
- autobuilt f34ad90

* Sun Jul 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.3.0-3.1.dev.git5c690f7
- autobuilt 5c690f7

* Wed Jul 10 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.3.0-2.1.dev.git4889f52
- built 4889f52
- hook up to autobuild

* Wed May 15 2019 Dan Walsh <dwalsh@fedoraproject.org> - v0.3.0-2
- Update to released version

* Wed Feb 27 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.3.0-1.alpha.2
- make version tag consistent with upstream

* Sun Feb 17 2019 Dan Walsh <dwalsh@fedoraproject.org> - v0.3.0-alpha.2
- Latest release

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 0.1-3.dev.git0037042
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Mon Aug 20 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1-2.dev.git0037042
- built 0037042

* Fri Jul 27 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.1-1.dev.gitc4e1bc5
- Resolves: #1609595 - initial upload
- First package for Fedora
