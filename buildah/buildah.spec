%global with_bundled 1
%global with_debug 1

%if 0%{?with_debug}
%global _find_debuginfo_dwz_opts %{nil}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%if 0%{?centos}
%define gobuild(o:) \
go build -buildmode pie -compiler gc -tags="rpm_crashtraceback ${BUILDTAGS:-}" -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '%__global_ldflags'" -a -v -x %{?**};
%endif

%global provider github
%global provider_tld com
%global project containers
%global repo buildah
# https://github.com/containers/buildah
%global import_path %{provider}.%{provider_tld}/%{project}/%{repo}
%global git0 https://%{import_path}
%global commit0 6cc46567d1c7011bc99ac99ecc6239f2d3df0aa9
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

# Used for comparing with latest upstream tag
# to decide whether to autobuild (non-rawhide only)
%global built_tag v1.12.0

Name: %{repo}
Version: 1.12.0
Release: 2%{?dist}
Summary: A command line tool used for creating OCI Images
License: ASL 2.0
URL: https://%{name}.io
Source: %{git0}/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires: %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
BuildRequires: git
BuildRequires: glib2-devel
BuildRequires: libseccomp-static
BuildRequires: ostree-devel
BuildRequires: glibc-static
BuildRequires: go-md2man
BuildRequires: gpgme-devel
BuildRequires: device-mapper-devel
BuildRequires: btrfs-progs-devel
BuildRequires: libassuan-devel
BuildRequires: make
Requires: containers-common
%if 0%{?fedora}
Requires: crun >= 0.10-1
Recommends: container-selinux
Recommends: slirp4netns >= 0.3-0
Recommends: fuse-overlayfs
%else
#### DO NOT REMOVE - NEEDED FOR CENTOS
Requires: libseccomp >= 2.4.1-0
Requires: container-selinux
Requires: slirp4netns >= 0.3-0
%endif

%description
The %{name} package provides a command line tool which can be used to
* create a working container from scratch
or
* create a working container from an image as a starting point
* mount/umount a working container's root file system for manipulation
* save container's root file system layer to create a new image
* delete a working container or an image

%prep
%autosetup -Sgit -n %{name}-%{commit0}
sed -i 's/GOMD2MAN =/GOMD2MAN ?=/' docs/Makefile
sed -i '/docs install/d' Makefile

%build
mkdir _build
pushd _build
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s $(dirs +1 -l) src/%{import_path}
popd

mv vendor src

export GOPATH=$(pwd)/_build:$(pwd)
export BUILDTAGS='seccomp selinux'
export GO111MODULE=off
%gobuild -o %{name} %{import_path}/cmd/%{name}
GOMD2MAN=go-md2man %{__make} -C docs

%install
export GOPATH=$(pwd)/_build:$(pwd):%{gopath}
make DESTDIR=%{buildroot} PREFIX=%{_prefix} install install.completions
make DESTDIR=%{buildroot} PREFIX=%{_prefix} -C docs install

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_mandir}/man1/%{name}*
%dir %{_datadir}/bash-completion
%dir %{_datadir}/bash-completion/completions
%{_datadir}/bash-completion/completions/%{name}

%changelog
* Fri Dec 27 2019 Alberto Chiusole <bebo.sudo@gmail.com> - 1.12.0-3
- rebuild from fc31 testing for centos 7

* Fri Dec 13 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.12.0-2
- bump to v1.12.0
- autobuilt 6cc4656

* Fri Dec 06 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.11.6-2
- bump to v1.11.6
- autobuilt 9513cb8

* Wed Oct 30 2019 Lokesh Mandvekar <lsm5@redhat.com> - 1.11.4-3
- crun only for fedora ATM

* Mon Oct 28 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.11.4-2
- bump to v1.11.4
- autobuilt 21b4778

* Wed Oct 16 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.11.3-3
- update libseccomp dep for centos

* Fri Oct 04 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 1.11.3-2
- bump to v1.11.3
- autobuilt bdd78ad

* Tue Oct 01 2019 Debarshi Ray <rishi@fedoraproject.org> - 1.11.2-3.git0bafbfe
- Switch to crun for Cgroups v2 support

* Tue Sep 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.2-2.git0bafbfe
- bump to v1.11.2
- autobuilt 0bafbfe

* Thu Sep 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.1-2.git413bd1f
- bump to v1.11.1
- autobuilt 413bd1f

* Thu Sep 05 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.11.0-1.git2c5da1b
- built tag v1.11.0

* Mon Aug 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-0.16.dev.gita99139c
- autobuilt a99139c

* Mon Aug 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-0.15.dev.git2df08f0
- autobuilt 2df08f0

* Mon Aug 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-0.14.dev.git96a136e
- autobuilt 96a136e

* Sun Aug 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-0.13.dev.git7180312
- autobuilt 7180312

* Sat Aug 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-0.12.dev.git0dfb6f5
- autobuilt 0dfb6f5

* Fri Aug 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-0.11.dev.git60d5480
- autobuilt 60d5480

* Fri Aug 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-0.10.dev.git60c0088
- autobuilt 60c0088

* Fri Aug 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-0.9.dev.gitc953216
- autobuilt c953216

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-0.8.dev.gitf892eb6
- autobuilt f892eb6

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-0.7.dev.git95cb061
- autobuilt 95cb061

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-0.6.dev.gitf4cfe9c
- autobuilt f4cfe9c

* Wed Aug 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-0.5.dev.git03aa807
- autobuilt 03aa807

* Wed Aug 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-0.4.dev.gitbafcf88
- autobuilt bafcf88

* Tue Aug 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-0.3.dev.git232f7c6
- autobuilt 232f7c6

* Mon Aug 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-0.2.dev.git1de958d
- autobuilt 1de958d

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.11.0-0.1.dev.gitac5031d
- bump to 1.11.0
- autobuilt ac5031d

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-0.68.dev.git3117f5e
- autobuilt 3117f5e

* Thu Aug 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-0.67.dev.git4d017d6
- autobuilt 4d017d6

* Wed Jul 31 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-0.66.dev.gitc00f548
- autobuilt c00f548

* Wed Jul 31 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-0.65.dev.git677b771
- autobuilt 677b771

* Tue Jul 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-0.64.dev.gitb7a0ed0
- autobuilt b7a0ed0

* Tue Jul 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-0.63.dev.git5bab9b0
- autobuilt 5bab9b0

* Mon Jul 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-0.62.dev.git4ccb343
- autobuilt 4ccb343

* Mon Jul 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-0.61.dev.gita74bdd3
- autobuilt a74bdd3

* Sat Jul 27 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-0.60.dev.git6b214d2
- autobuilt 6b214d2

* Fri Jul 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-0.59.dev.git73401a4
- autobuilt 73401a4

* Wed Jul 24 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.9.3-0.58.dev.git6bd0551
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Jul 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-0.57.dev.git6bd0551
- autobuilt 6bd0551

* Fri Jul 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-0.56.dev.git555b5a5
- autobuilt 555b5a5

* Fri Jul 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.3-0.55.dev.git2110f05
- bump to 1.9.3
- autobuilt 2110f05

* Fri Jul 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-0.54.dev.gitd7dec37
- autobuilt d7dec37

* Fri Jul 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-0.53.dev.git5da3c8c
- autobuilt 5da3c8c

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-0.52.dev.git4ae0e14
- autobuilt 4ae0e14

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-0.51.dev.git8da4cb4
- autobuilt 8da4cb4

* Wed Jul 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-0.50.dev.gitbe51b9b
- autobuilt be51b9b

* Wed Jul 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-0.49.dev.gitb33b87b
- autobuilt b33b87b

* Wed Jul 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-0.48.dev.git16e3010
- autobuilt 16e3010

* Tue Jul 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-0.47.dev.gitbb5cbf1
- autobuilt bb5cbf1

* Tue Jul 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-0.46.dev.git2249ba3
- autobuilt 2249ba3

* Sun Jul 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.2-0.45.dev.gitd419737
- bump to 1.9.2
- autobuilt d419737

* Wed Jul 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.1-0.44.dev.git5d723ff
- autobuilt 5d723ff

* Sun Jul 07 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.1-0.43.dev.gite160a63
- built e160a63
- add centos conditionals
- use new name for go-md2man dep

* Sat Jun 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.1-0.42.dev.git1d11851
- autobuilt 1d11851

* Fri Jun 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.1-0.41.dev.git07aaf5e
- autobuilt 07aaf5e

* Thu Jun 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.1-0.40.dev.gitc22957b
- autobuilt c22957b

* Tue Jun 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.1-0.39.dev.git2c4f388
- autobuilt 2c4f388

* Sun Jun 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.1-0.38.dev.git0b84b23
- bump to 1.9.1
- autobuilt 0b84b23

* Sat Jun 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.37.dev.git77fa9dd
- autobuilt 77fa9dd

* Fri Jun 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.36.dev.gitdc7b50c
- autobuilt dc7b50c

* Thu Jun 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.35.dev.git2191ba6
- autobuilt 2191ba6

* Wed Jun 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.34.dev.gitdcbf193
- autobuilt dcbf193

* Tue Jun 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.33.dev.git78dcf2f
- autobuilt 78dcf2f

* Mon Jun 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.32.dev.git4ae0a69
- autobuilt 4ae0a69

* Sun Jun 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.31.dev.gitd172dd9
- autobuilt d172dd9

* Sat Jun 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.30.dev.git2da8755
- autobuilt 2da8755

* Fri Jun 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.29.dev.gitad4f235
- autobuilt ad4f235

* Thu Jun 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.28.dev.gite0306bb
- autobuilt e0306bb

* Wed Jun 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.27.dev.gitaa06a77
- autobuilt aa06a77

* Sun Jun 02 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-0.26.dev.gita086ec8
- build for all arches

* Sun Jun 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.25.dev.git7016ce6
- autobuilt 7016ce6

* Sat Jun 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.24.dev.git3104ddf
- autobuilt 3104ddf

* Fri May 31 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.23.dev.git53be3d3
- autobuilt 53be3d3

* Thu May 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.22.dev.git2a962f1
- autobuilt 2a962f1

* Wed May 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.21.dev.gitfa7f030
- autobuilt fa7f030

* Tue May 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.20.dev.gited77a92
- autobuilt ed77a92

* Sat May 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.19.dev.git8e48a65
- autobuilt 8e48a65

* Fri May 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.18.dev.git4e1ca7c
- autobuilt 4e1ca7c

* Fri May 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.17.dev.git00f5164
- autobuilt 00f5164

* Thu May 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.16.dev.gitbc9c276
- autobuilt bc9c276

* Tue May 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.15.dev.gitbcc5e51
- autobuilt bcc5e51

* Sun May 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.14.dev.git7793c51
- autobuilt 7793c51

* Sat May 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.13.dev.git3bf8547
- autobuilt 3bf8547

* Fri May 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.12.dev.git63808f9
- autobuilt 63808f9

* Thu May 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.11.dev.gitc0633e3
- autobuilt c0633e3

* Wed May 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.10.dev.git4c6b09c
- autobuilt 4c6b09c

* Tue May 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.9.dev.git7ae362b
- autobuilt 7ae362b

* Mon May 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.8.dev.git74a3195
- autobuilt 74a3195

* Sun May 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.7.dev.gitab8678a
- autobuilt ab8678a

* Sat May 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.6.dev.gitc654b18
- autobuilt c654b18

* Sat May 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.5.dev.gite9184ea
- autobuilt e9184ea

* Fri May 03 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.4.dev.git59da11d
- autobuilt 59da11d

* Thu May 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.3.dev.git78fb869
- autobuilt 78fb869

* Tue Apr 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.9.0-0.2.dev.git0e30da6
- autobuilt 0e30da6

* Sun Apr 28 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.9.0-0.1.dev.gitddbd805
- bump to v1.9.0-dev
- update release tag format for unreleased builds

* Wed Apr 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-41.dev.gitbdbedfd
- autobuilt bdbedfd

* Tue Apr 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-40.dev.gitb466cbd
- autobuilt b466cbd

* Sat Apr 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-39.dev.git2f0179f
- autobuilt 2f0179f

* Fri Apr 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-38.dev.git135542e
- autobuilt 135542e

* Thu Apr 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-37.dev.gite879079
- autobuilt e879079

* Wed Apr 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-36.dev.gitd8fe400
- autobuilt d8fe400

* Mon Apr 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-35.dev.gitfcc12bd
- autobuilt fcc12bd

* Sat Apr 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-34.dev.gitd43787b
- autobuilt d43787b

* Fri Apr 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-33.dev.git316bd0a
- autobuilt 316bd0a

* Wed Apr 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-32.dev.git021d607
- autobuilt 021d607

* Tue Apr 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-31.dev.git610eb7a
- autobuilt 610eb7a

* Sun Apr 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-30.dev.git25b7c11
- autobuilt 25b7c11

* Sat Apr 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-29.dev.git29a6c81
- autobuilt 29a6c81

* Fri Apr 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-28.dev.gitac66d78
- autobuilt ac66d78

* Mon Apr 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-27.dev.git9e1967a
- autobuilt 9e1967a

* Sat Mar 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-26.dev.git13d9142
- autobuilt 13d9142

* Fri Mar 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-25.dev.gita9bd025
- autobuilt a9bd025

* Thu Mar 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-24.dev.gitc933fe4
- autobuilt c933fe4

* Wed Mar 27 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-23.dev.git3d74031
- autobuilt 3d74031

* Mon Mar 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-22.dev.git03fae01
- autobuilt 03fae01

* Sat Mar 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-21.dev.gitd1c75ea
- autobuilt d1c75ea

* Fri Mar 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-20.dev.gitc6ae5c5
- autobuilt c6ae5c5

* Thu Mar 21 2019 Dan Walsh <dwalsh@redhat.com> - 1.8-19.dev.gitbe0c8d2
- Complile with SELinux enabled

* Thu Mar 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-18.dev.gitbe0c8d2
- autobuilt be0c8d2

* Wed Mar 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-17.dev.git9d6da3a
- autobuilt 9d6da3a

* Tue Mar 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-16.dev.git1ba9201
- autobuilt 1ba9201

* Sat Mar 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-15.dev.gita986f34
- autobuilt a986f34

* Fri Mar 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-14.dev.gitc691d09
- autobuilt c691d09

* Thu Mar 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-13.dev.git3b497ff
- autobuilt 3b497ff

* Wed Mar 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-12.dev.git3ba8822
- autobuilt 3ba8822

* Sun Mar 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-11.dev.git36605c2
- autobuilt 36605c2

* Sat Mar 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-10.dev.git984ea9b
- autobuilt 984ea9b

* Thu Mar 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-9.dev.git0a8ec97
- autobuilt 0a8ec97

* Wed Mar 06 2019 Dan Walsh <dwalsh@redhat.com> - 1.8-8.dev.git3afba37
- Add recommends for fuse-overlay and slirp4netns

* Wed Mar 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-7.dev.git3afba37
- autobuilt 3afba37

* Tue Mar 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-6.dev.git11dd219
- autobuilt 11dd219

* Fri Mar 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-5.dev.git8b1d11f
- autobuilt 8b1d11f

* Thu Feb 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-4.dev.git95a5089
- autobuilt 95a5089

* Tue Feb 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-3.dev.git6c1a4cc
- autobuilt 6c1a4cc

* Sat Feb 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.8-2.dev.git8c3d8b1
- bump to 1.8
- autobuilt 8c3d8b1

* Fri Feb 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-20.dev.git873f001
- autobuilt 873f001

* Thu Feb 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-19.dev.gitdb6e7bb
- autobuilt db6e7bb

* Wed Feb 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-18.dev.git1b02a7e
- autobuilt 1b02a7e

* Mon Feb 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-17.dev.git146a0fc
- autobuilt 146a0fc

* Sat Feb 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-16.dev.git80fcb24
- autobuilt 80fcb24

* Fri Feb 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-15.dev.git40d4d59
- autobuilt 40d4d59

* Thu Feb 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-14.dev.gite4c4d46
- autobuilt e4c4d46

* Sun Feb 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-13.dev.git711f9ea
- autobuilt 711f9ea

* Fri Feb 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-12.dev.git310363c
- autobuilt 310363c

* Wed Feb 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-11.dev.git50539b5
- autobuilt 50539b5

* Tue Feb 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-10.dev.gitad24f28
- autobuilt ad24f28

* Sat Feb 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-9.dev.git973bb88
- autobuilt 973bb88

* Fri Feb 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-8.dev.git03f6247
- autobuilt 03f6247

* Thu Jan 31 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.7-7.dev.gite702872
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Tue Jan 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-6.dev.gite702872
- autobuilt e702872

* Thu Jan 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-5.dev.gitf1cec50
- autobuilt f1cec50

* Tue Jan 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-4.dev.git4bcddb7
- autobuilt 4bcddb7

* Mon Jan 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-3.dev.git9b9ed1d
- autobuilt 9b9ed1d

* Sun Jan 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-2.dev.git7a85ca7
- bump to 1.7
- autobuilt 7a85ca7

* Sat Jan 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-2.dev.git5f95bd9
- bump to 1.6
- autobuilt 5f95bd9

* Fri Jan 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.7-2.dev.git0f114e9
- bump to 1.7
- autobuilt 0f114e9

* Thu Jan 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-33.dev.git66ff1dd
- autobuilt 66ff1dd

* Wed Jan 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-32.dev.gitd7e530e
- autobuilt d7e530e

* Tue Jan 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-31.dev.gitfe7e09c
- autobuilt fe7e09c

* Sun Jan 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-30.dev.gitfa86533
- autobuilt fa86533

* Sat Jan 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-29.dev.gitf6a0258
- autobuilt f6a0258

* Fri Jan 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-28.dev.git5d22f3c
- autobuilt 5d22f3c

* Thu Jan 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-27.dev.git1ef527c
- autobuilt 1ef527c

* Wed Jan 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-26.dev.git169a923
- autobuilt 169a923

* Tue Jan 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-25.dev.git48b44e5
- autobuilt 48b44e5

* Mon Jan 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-24.dev.gita4200ae
- autobuilt a4200ae

* Sun Jan 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-23.dev.gitbb710f3
- autobuilt bb710f3

* Sat Jan 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-22.dev.git8f05aa6
- autobuilt 8f05aa6

* Fri Jan 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-21.dev.git579f1d5
- autobuilt 579f1d5

* Thu Jan 03 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-20.dev.gite55a9f3
- autobuilt e55a9f3

* Tue Dec 25 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-1.nightly.git5f95bd99.dev.giteebbba2
- autobuilt eebbba2

* Thu Dec 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-1.nightly.git5f95bd98.dev.git4674656
- autobuilt 4674656

* Wed Dec 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-1.nightly.git5f95bd97.dev.gitdd3dff5
- autobuilt dd3dff5

* Sun Dec 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-1.nightly.git5f95bd96.dev.git96c68db
- autobuilt 96c68db

* Fri Dec 14 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-1.nightly.git5f95bd95.dev.gitde7f480
- autobuilt de7f480

* Wed Dec 12 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-1.nightly.git5f95bd94.dev.git90ea890
- autobuilt 90ea890

* Mon Dec 10 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-1.nightly.git5f95bd93.dev.gitdd0f4f1
- autobuilt dd0f4f1

* Sat Dec 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-1.nightly.git5f95bd92.dev.git1e1dc14
- autobuilt 1e1dc14

* Fri Dec 07 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-1.nightly.git5f95bd91.dev.git9c1d273
- autobuilt 9c1d273

* Thu Dec 06 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-1.nightly.git5f95bd90.dev.git5cca1d6
- autobuilt 5cca1d6

* Wed Dec 05 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-9.dev.git01f9ae2
- autobuilt 01f9ae2

* Tue Dec 04 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-8.dev.git9c65e56
- autobuilt 9c65e56

* Sun Dec 02 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-7.dev.gitb68a8e1
- autobuilt b68a8e1

* Sat Dec 01 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-6.dev.git2b582d3
- autobuilt 2b582d3

* Fri Nov 30 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-5.dev.git6e00183
- autobuilt 6e00183

* Thu Nov 29 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-4.dev.git93d8b9f
- autobuilt 93d8b9f

* Wed Nov 28 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-3.dev.git4126176
- autobuilt 4126176

* Fri Nov 23 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.6-2.dev.gitd5a3c52
- bump to 1.6
- autobuilt d5a3c52

* Thu Nov 22 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-12.dev.git25d89b4
- autobuilt 25d89b4

* Wed Nov 21 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-11.dev.git2ac987a
- autobuilt 2ac987a

* Tue Nov 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-10.dev.gitc9cb148
- autobuilt c9cb148

* Sat Nov 17 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-9.dev.git18309de
- autobuilt 18309de

* Fri Nov 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-8.dev.gitd7e0993
- autobuilt d7e0993

* Thu Nov 15 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-7.dev.gitdac7819
- autobuilt dac7819

* Tue Nov 13 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-6.dev.gitfb2b2bd
- autobuilt fb2b2bd

* Sat Nov 10 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-5.dev.git9add3c8
- autobuilt 9add3c8

* Fri Nov 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-4.dev.git74e0b6f
- autobuilt 74e0b6f

* Thu Nov 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-3.dev.git0ae8b51
- autobuilt 0ae8b51

* Wed Nov 07 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.5-2.dev.git7341758
- autobuilt 7341758

* Tue Oct 2 2018 Dan Walsh <dwalsh@redhat.com> - 1.5-1.dev.git87239ae
- bump to v1.5-dev Release

* Wed Sep 19 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.4-2.dev.git19e44f0
- autobuilt 19e44f0

* Sun Aug 12 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.4-1.dev.git0a7389c
- bump to v1.4-dev
- built 0a7389c

* Wed Aug 01 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.3-11.dev.git02f54e4
- autobuilt 02f54e4

* Tue Jul 31 2018 Florian Weimer <fweimer@redhat.com> - 1.3-10.dev.gitbe03809
- Rebuild with fixed binutils

* Sun Jul 29 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.3-9.dev.gitbe03809
- autobuilt be03809

* Sat Jul 28 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.3-8.dev.gitc18724e
- autobuilt c18724e

* Thu Jul 26 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.3-7.dev.git4976d8c
- autobuilt 4976d8c

* Wed Jul 25 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.3-6.dev.gite5f7539
- autobuilt e5f7539

* Mon Jul 23 2018 Dan Walsh <dwalsh@redhat.com> - 1.3-5.dev.dev.git826733a
- Change container-selinux Requires to Recommends

* Fri Jul 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.3-4.dev.git826733a
- autobuilt 826733a

* Thu Jul 19 2018 Dan Walsh <dwalsh@redhat.com> - 1.3-3.dev.git1215b16
- buildah does not require ostree

* Thu Jul 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.3-2.dev.git1215b16
- autobuilt 1215b16

* Tue Jul 17 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1.3-1.dev.gita9895bd
- bump to v1.3-dev
- built a9895bd

* Thu Jul 12 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2-25.dev.git3fb864b
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-24.git3fb864b
- autobuilt 3fb864b

* Sun Jul 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-23.git8be2b62
- autobuilt 8be2b62

* Sat Jul 07 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-22.gita885bc6
- autobuilt a885bc6

* Fri Jul 06 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-21.git733cd20
- autobuilt 733cd20

* Thu Jul 05 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-20.gita59fb7a
- autobuilt a59fb7a

* Tue Jul 03 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-19.git5c11c34
- autobuilt 5c11c34

* Mon Jul 02 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-18.git5cd9be6
- autobuilt 5cd9be6

* Sun Jul 01 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-17.git6f72599
- autobuilt 6f72599

* Sat Jun 30 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-16.git704adec
- autobuilt 704adec

* Fri Jun 29 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-15.gitb965fc4
- autobuilt b965fc4

* Thu Jun 28 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-14.git1acccce
- autobuilt 1acccce

* Wed Jun 27 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-13.git146c185
- autobuilt 146c185

* Tue Jun 26 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-12.git16a33bd
- autobuilt 16a33bd

* Mon Jun 25 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-11.git2ac95ea
- autobuilt 2ac95ea

* Sat Jun 23 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-10.git0143a44
- autobuilt 0143a44

* Thu Jun 21 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-9.git2441ff4
- autobuilt 2441ff4

* Wed Jun 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-8.gitda7be32
- autobuilt da7be32

* Tue Jun 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-7.git2064b29
- autobuilt 2064b29

* Mon Jun 18 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-6.git93d8606
- autobuilt 93d8606

* Fri Jun 15 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-5.gitfc438bb
- autobuilt fc438bb

* Thu Jun 14 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-4.git73820fc
- autobuilt 73820fc

* Wed Jun 13 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-3.git6c4bef7
- autobuilt 6c4bef7

* Tue Jun 12 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-2.git94c1e6d
- autobuilt 94c1e6d

* Mon Jun 11 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.2-1.gitb9983a6
- bump to 1.2
- autobuilt b9983a6

* Sun Jun 10 2018 Dan Walsh <dwalsh@redhat.com> 1.1-1
- Drop capabilities if running container processes as non root
- Print Warning message if cmd will not be used based on entrypoint
- Update 01-intro.md
- Shouldn't add insecure registries to list of search registries
- Report errors on bad transports specification when pushing images
- Move parsing code out of common for namespaces and into pkg/parse.go
- Add disable-content-trust noop flag to bud
- Change freenode chan to buildah
- runCopyStdio(): don't close stdin unless we saw POLLHUP
- Add registry errors for pull
- runCollectOutput(): just read until the pipes are closed on us
- Run(): provide redirection for stdio
- rmi, rm: add test
- add mount test
- Add parameter judgment for commands that do not require parameters
- Add context dir to bud command in baseline test
- run.bats: check that we can run with symlinks in the bundle path
- Give better messages to users when image can not be found
- use absolute path for bundlePath
- Add environment variable to buildah --format
- rm: add validation to args and all option
- Accept json array input for config entrypoint
- Run(): process RunOptions.Mounts, and its flags
- Run(): only collect error output from stdio pipes if we created some
- Add OnBuild support for Dockerfiles
- Quick fix on demo readme
- run: fix validate flags
- buildah bud should require a context directory or URL
- Touchup tutorial for run changes
- Validate common bud and from flags
- images: Error if the specified imagename does not exist
- inspect: Increase err judgments to avoid panic
- add test to inspect
- buildah bud picks up ENV from base image
- Extend the amount of time travis_wait should wait
- Add a make target for Installing CNI plugins
- Add tests for namespace control flags
- copy.bats: check ownerships in the container
- Fix SELinux test errors when SELinux is enabled
- Add example CNI configurations
- Run: set supplemental group IDs
- Run: use a temporary mount namespace
- Use CNI to configure container networks
- add/secrets/commit: Use mappings when setting permissions on added content
- Add CLI options for specifying namespace and cgroup setup
- Always set mappings when using user namespaces
- Run(): break out creation of stdio pipe descriptors
- Read UID/GID mapping information from containers and images
- Additional bud CI tests
- Run integration tests under travis_wait in Travis
- build-using-dockerfile: add --annotation
- Implement --squash for build-using-dockerfile and commit
- Vendor in latest container/storage for devicemapper support
- add test to inspect
- Vendor github.com/onsi/ginkgo and github.com/onsi/gomega
- Test with Go 1.10, too
- Add console syntax highlighting to troubleshooting page
- bud.bats: print "$output" before checking its contents
- Manage "Run" containers more closely
- Break Builder.Run()'s "run runc" bits out
- util.ResolveName(): handle completion for tagged/digested image names
- Handle /etc/hosts and /etc/resolv.conf properly in container
- Documentation fixes
- Make it easier to parse our temporary directory as an image name
- Makefile: list new pkg/ subdirectoris as dependencies for buildah
- containerImageSource: return more-correct errors
- API cleanup: PullPolicy and TerminalPolicy should be types
- Make "run --terminal" and "run -t" aliases for "run --tty"
- Vendor github.com/containernetworking/cni v0.6.0
- Update github.com/containers/storage
- Update github.com/projectatomic/libpod
- Add support for buildah bud --label
- buildah push/from can push and pull images with no reference
- Vendor in latest containers/image
- Update gometalinter to fix install.tools error
- Update troubleshooting with new run workaround
- Added a bud demo and tidied up
- Attempt to download file from url, if fails assume Dockerfile
- Add buildah bud CI tests for ENV variables
- Re-enable rpm .spec version check and new commit test
- Update buildah scratch demo to support el7
- Added Docker compatibility demo
- Update to F28 and new run format in baseline test
- Touchup man page short options across man pages
- Added demo dir and a demo. chged distrorlease
- builder-inspect: fix format option
- Add cpu-shares short flag (-c) and cpu-shares CI tests
- Minor fixes to formatting in rpm spec changelog
- Fix rpm .spec changelog formatting
- CI tests and minor fix for cache related noop flags
- buildah-from: add effective value to mount propagation

* Sat Jun 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-20.gitf449b28
- autobuilt f449b28

* Fri Jun 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-19.gitc306342
- autobuilt c306342

* Wed Jun 06 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-18.gitd3d097b
- autobuilt d3d097b

* Mon Jun 04 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-17.gitf90b6c0
- autobuilt f90b6c0

* Sun Jun 03 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-16.git70641ee
- autobuilt 70641ee

* Sat Jun 02 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-15.git03686e5
- autobuilt 03686e5

* Fri Jun 01 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-14.git73bfd79
- autobuilt 73bfd79

* Thu May 31 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-13.git5595d4d
- autobuilt 5595d4d

* Wed May 30 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-12.gitebb0d8e
- autobuilt ebb0d8e

* Tue May 29 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-11.git88affbd
- autobuilt 88affbd

* Fri May 25 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-10.git25f4e8e
- autobuilt 25f4e8e

* Thu May 17 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-9.git2749191
- autobuilt 2749191

* Wed May 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-8.git3e320b9
- autobuilt 3e320b9

* Tue May 15 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-7.git8515867
- autobuilt 8515867

* Sun May 13 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-6.gitce8d467
- autobuilt ce8d467

* Sat May 12 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-5.gitb9a1041
- autobuilt b9a1041

* Fri May 11 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-4.git2ea3e11
- autobuilt 2ea3e11

* Wed May 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-3.gitfe204e4
- autobuilt fe204e4

* Tue May 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1.0-2.git906ee37
- autobuilt 906ee37

* Mon May 07 2018 Dan Walsh <dwalsh@redhat.com> 1.0-1
- Remove buildah run cmd and entrypoint execution
- Add Files section with registries.conf to pertinent man pages
- Force "localhost" as a default registry
- Add --compress, --rm, --squash flags as a noop for bud
- Add FIPS mode secret to buildah run and bud
- Add config --comment/--domainname/--history-comment/--hostname
- Add support for --iidfile to bud and commit
- Add /bin/sh -c to entrypoint in config
- buildah images and podman images are listing different sizes
- Remove tarball as an option from buildah push --help
- Update entrypoint behaviour to match docker
- Display imageId after commit
- config: add support for StopSignal
- Allow referencing stages as index and names
- Add multi-stage builds support
- Vendor in latest imagebuilder, to get mixed case AS support
- Allow umount to have multi-containers
- Update buildah push doc
- buildah bud walks symlinks
- Imagename is required for commit atm, update manpage

* Mon May 07 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-25.gitdd02e70
- autobuilt dd02e70

* Sat May 05 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-24.git45772e8
- autobuilt 45772e8

* Fri May 04 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-23.git6fe2b55
- autobuilt 6fe2b55

* Wed May 02 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-22.gita4f5707
- autobuilt a4f5707

* Wed May 02 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-21.gite130f2b
- autobuilt commit e130f2b

* Tue May 01 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-20.gitadb8e6f
- autobuilt commit adb8e6f

* Sat Apr 28 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-19.gitc50c287
- autobuilt commit c50c287

* Fri Apr 27 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-18.gitca1704f
- autobuilt commit ca1704f

* Wed Apr 25 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-17.git49abf82
- autobuilt commit 49abf82

* Tue Apr 24 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-16.gitfdc3998
- autobuilt commit fdc3998

* Tue Apr 24 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-15.gitb16a1ea
- autobuilt commit b16a1ea

* Fri Apr 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-14.gitd84f05a
- autobuilt commit d84f05a

* Thu Apr 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-13.gite008b73
- autobuilt commit e008b73

* Thu Apr 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-12.git28a27a3
- autobuilt commit 28a27a3

* Tue Apr 17 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-11.git45a4b81
- autobuilt commit 45a4b81

* Tue Apr 17 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-10.git45a4b81
- autobuilt commit 45a4b81

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-9.git6421399
- autobuilt commit 6421399

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-8.git83d7d10
- autobuilt commit 83d7d10

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-7.git83d7d10
- autobuilt commit 83d7d10

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-6.git83d7d10
- autobuilt commit 83d7d10

* Mon Apr 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-5.git4339223
- autobuilt commit 4339223

* Mon Apr 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.16-4.git4339223
- autobuilt commit 4339223

* Mon Apr 09 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.16-3.git4339223
- autobuilt commit 4339223

* Sun Apr 08 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.16-2.git4743c2e
- autobuilt commit 4743c2e

* Wed Apr 4 2018 Dan Walsh <dwalsh@redhat.com> 0.16-1
- Add support for shell
- Vendor in latest containers/image
- docker-archive generates docker legacy compatible images
- Do not create $DiffID subdirectories for layers with no configs
- Ensure the layer IDs in legacy docker/tarfile metadata are unique
- docker-archive: repeated layers are symlinked in the tar file
- sysregistries: remove all trailing slashes
- Improve docker/* error messages
- Fix failure to make auth directory
- Create a new slice in Schema1.UpdateLayerInfos
- Drop unused storageImageDestination.{image,systemContext}
- Load a *storage.Image only once in storageImageSource
- Support gzip for docker-archive files
- Remove .tar extension from blob and config file names
- ostree, src: support copy of compressed layers
- ostree: re-pull layer if it misses uncompressed_digest|uncompressed_size
- image: fix docker schema v1 -> OCI conversion
- Add /etc/containers/certs.d as default certs directory
- Change image time to locale, add troubleshooting.md, add logo to other mds
- Allow --cmd parameter to have commands as values
- Document the mounts.conf file
- Fix man pages to format correctly
- buildah from now supports pulling images using the following transports:
- docker-archive, oci-archive, and dir.
- If the user overrides the storage driver, the options should be dropped
- Show Config/Manifest as JSON string in inspect when format is not set
- Adds feature to pull compressed docker-archive files

* Tue Feb 27 2018 Dan Walsh <dwalsh@redhat.com> 0.15-1
- Fix handling of buildah run command options

* Mon Feb 26 2018 Dan Walsh <dwalsh@redhat.com> 0.14-1
- If commonOpts do not exist, we should return rather then segfault
- Display full error string instead of just status
- Implement --volume and --shm-size for bud and from
- Fix secrets patch for buildah bud
- Fixes the naming issue of blobs and config for the dir transport by removing the .tar extension

* Sun Feb 25 2018 Peter Robinson <pbrobinson@fedoraproject.org> 0.13-2
- Build on ARMv7 too (Fedora supports containers on that arch too)

* Thu Feb 22 2018 Dan Walsh <dwalsh@redhat.com> 0.13-1
- Vendor in latest containers/storage
- This fixes a large SELinux bug.
- run: do not open /etc/hosts if not needed
- Add the following flags to buildah bud and from
            --add-host
            --cgroup-parent
            --cpu-period
            --cpu-quota
            --cpu-shares
            --cpuset-cpus
            --cpuset-mems
            --memory
            --memory-swap
            --security-opt
            --ulimit

* Mon Feb 12 2018 Dan Walsh <dwalsh@redhat.com> 0.12-1
- Added handing for simpler error message for Unknown Dockerfile instructions.
- Change default certs directory to /etc/containers/certs.dir
- Vendor in latest containers/image
- Vendor in latest containers/storage
- build-using-dockerfile: set the 'author' field for MAINTAINER
- Return exit code 1 when buildah-rmi fails
- Trim the image reference to just its name before calling getImageName
- Touch up rmi -f usage statement
- Add --format and --filter to buildah containers
- Add --prune,-p option to rmi command
- Add authfile param to commit
- Fix --runtime-flag for buildah run and bud
- format should override quiet for images
- Allow all auth params to work with bud
- Do not overwrite directory permissions on --chown
- Unescape HTML characters output into the terminal
- Fix: setting the container name to the image
- Prompt for un/pwd if not supplied with --creds
- Make bud be really quiet
- Return a better error message when failed to resolve an image
- Update auth tests and fix bud man page

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.11-3.git6bad262
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Feb 05 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.11-2
- Resolves: upstream gh#432
- enable debuginfo for non-fedora packages

* Tue Jan 16 2018 Dan Walsh <dwalsh@redhat.com> 0.11-1
- Add --all to remove containers
- Add --all functionality to rmi
- Show ctrid when doing rm -all
- Ignore sequential duplicate layers when reading v2s1
- Lots of minor bug fixes
- Vendor in latest containers/image and containers/storage

* Tue Dec 26 2017 Dan Walsh <dwalsh@redhat.com> 0.10-2
- Fix checkin

* Sat Dec 23 2017 Dan Walsh <dwalsh@redhat.com> 0.10-1
- Display Config and Manifest as strings
- Bump containers/image
- Use configured registries to resolve image names
- Update to work with newer image library
- Add --chown option to add/copy commands

* Sat Dec 2 2017 Dan Walsh <dwalsh@redhat.com> 0.9-1
- Allow push to use the image id
- Make sure builtin volumes have the correct label

* Thu Nov 16 2017 Dan Walsh <dwalsh@redhat.com> 0.8-1
- Buildah bud was failing on SELinux machines, this fixes this
- Block access to certain kernel file systems inside of the container

* Thu Nov 16 2017 Dan Walsh <dwalsh@redhat.com> 0.7-1
- Ignore errors when trying to read containers buildah.json for loading SELinux reservations
- Use credentials from kpod login for buildah

* Wed Nov 15 2017 Dan Walsh <dwalsh@redhat.com> 0.6-1
- Adds support for converting manifest types when using the dir transport
- Rework how we do UID resolution in images
- Bump github.com/vbatts/tar-split
- Set option.terminal appropriately in run

* Wed Nov 08 2017 Dan Walsh <dwalsh@redhat.com> 0.5-2
- Bump github.com/vbatts/tar-split
- Fixes CVE That could allow a container image to cause a DOS

* Tue Nov 07 2017 Dan Walsh <dwalsh@redhat.com> 0.5-1
- Add secrets patch to buildah
- Add proper SELinux labeling to buildah run
- Add tls-verify to bud command
- Make filtering by date use the image's date
- images: don't list unnamed images twice
- Fix timeout issue
- Add further tty verbiage to buildah run
- Make inspect try an image on failure if type not specified
- Add support for `buildah run --hostname`
- Tons of bug fixes and code cleanup

* Fri Sep 22 2017 Dan Walsh <dwalsh@redhat.com> 0.4-1.git9cbccf88c
- Add default transport to push if not provided
- Avoid trying to print a nil ImageReference
- Add authentication to commit and push
- Add information on buildah from man page on transports
- Remove --transport flag
- Run: do not complain about missing volume locations
- Add credentials to buildah from
- Remove export command
- Run(): create the right working directory
- Improve "from" behavior with unnamed references
- Avoid parsing image metadata for dates and layers
- Read the image's creation date from public API
- Bump containers/storage and containers/image
- Don't panic if an image's ID can't be parsed
- Turn on --enable-gc when running gometalinter
- rmi: handle truncated image IDs

* Tue Aug 15 2017 Josh Boyer <jwboyer@redhat.com> - 0.3-5.gitb9b2a8a
- Build for s390x as well

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-4.gitb9b2a8a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.3-3.gitb9b2a8a
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Thu Jul 20 2017 Dan Walsh <dwalsh@redhat.com> 0.3-2.gitb9b2a8a7e
- Bump for inclusion of OCI 1.0 Runtime and Image Spec

* Tue Jul 18 2017 Dan Walsh <dwalsh@redhat.com> 0.2.0-1.gitac2aad6
- buildah run: Add support for -- ending options parsing
- buildah Add/Copy support for glob syntax
- buildah commit: Add flag to remove containers on commit
- buildah push: Improve man page and help information
- buildah run: add a way to disable PTY allocation
- Buildah docs: clarify --runtime-flag of run command
- Update to match newer storage and image-spec APIs
- Update containers/storage and containers/image versions
- buildah export: add support
- buildah images: update commands
- buildah images: Add JSON output option
- buildah rmi: update commands
- buildah containers: Add JSON output option
- buildah version: add command
- buildah run: Handle run without an explicit command correctly
- Ensure volume points get created, and with perms
- buildah containers: Add a -a/--all option

* Wed Jun 14 2017 Dan Walsh <dwalsh@redhat.com> 0.1.0-2.git597d2ab9
- Release Candidate 1
- All features have now been implemented.

* Fri Apr 14 2017 Dan Walsh <dwalsh@redhat.com> 0.0.1-1.git7a0a5333
- First package for Fedora
