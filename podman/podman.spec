%global with_devel 0
%global with_bundled 1
%global with_debug 1
%global with_check 0
%global with_unit_test 0

# Do not use the go-srpm-macros package, it breaks the build with no reason.
%define gobuild(o:) go build -buildmode pie -compiler gc -tags="rpm_crashtraceback ${BUILDTAGS:-}" -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n') -extldflags '-Wl,-z,relro -Wl,-z,now -specs=/usr/lib/rpm/redhat/redhat-hardened-ld '" -a -v -x %{?**};
%define gogenerate(o:) go generate %{?**};

%if 0%{?rhel} > 7 || 0%{?fedora}
%bcond_without varlink
%else
%bcond_with varlink
%endif

%if 0%{?with_debug}
%global _find_debuginfo_dwz_opts %{nil}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package %{nil}
%endif

%global provider github
%global provider_tld com
%global project containers
%global repo libpod
# https://github.com/containers/libpod
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path %{provider_prefix}
%global git0 https://%{provider}.%{provider_tld}/%{project}/%{repo}
%global commit0 f3ffda1e08f19e9a6a88484136b5eed76533f21a
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

# Used for comparing with latest upstream tag
# to decide whether to autobuild (non-rawhide only)
%global built_tag v1.6.2

Name: podman
%if 0%{?fedora}
Epoch: 2
%endif
Version: 1.6.2
Release: 3%{?dist}
Summary: Manage Pods, Containers and Container Images
License: ASL 2.0
URL: https://%{name}.io/
Source0: %{git0}/archive/%{commit0}/%{repo}-%{shortcommit0}.tar.gz
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires: %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}
BuildRequires: btrfs-progs-devel
BuildRequires: glib2-devel
BuildRequires: glibc-devel
BuildRequires: glibc-static
BuildRequires: git
BuildRequires: gpgme-devel
BuildRequires: libassuan-devel
BuildRequires: libgpg-error-devel
BuildRequires: libseccomp-devel
BuildRequires: libselinux-devel
BuildRequires: ostree-devel
BuildRequires: pkgconfig
BuildRequires: make
BuildRequires: systemd
BuildRequires: systemd-devel
%if 0%{?fedora} >= 31
BuildRequires: golang-github-cpuguy83-md2man
%else
BuildRequires: golang-github-cpuguy83-go-md2man
%endif

Requires: crun >= 0.10.2-1
Requires: containers-common
Requires: containernetworking-plugins >= 0.7.5-1
Requires: iptables
Requires: nftables
Requires: conmon

%if 0%{?rhel} > 7 || 0%{?fedora}
Recommends: %{name}-manpages = %{epoch}:%{version}-%{release}
Recommends: container-selinux
Recommends: slirp4netns >= 0.3.0-2
Recommends: fuse-overlayfs >= 0.3-8
Recommends: runc
Recommends: libvarlink-util
%else
Requires: %{name}-manpages = %{version}-%{release}
Requires: container-selinux
Requires: slirp4netns >= 0.3.0-2
Requires: runc >= 1.0.0-57
# varlink not in rhel 7
%endif

# vendored libraries
# awk '{print "Provides: bundled(golang("$1")) = "$2}' vendor.conf | sort
# [thanks to Carl George <carl@george.computer> for containerd.spec]
Provides: bundled(golang(github.com/Azure/go-ansiterm)) = 19f72df4d05d31cbe1c56bfc8045c96babff6c7e
Provides: bundled(golang(github.com/blang/semver)) = v3.5.0
Provides: bundled(golang(github.com/boltdb/bolt)) = master
Provides: bundled(golang(github.com/buger/goterm)) = 2f8dfbc7dbbff5dd1d391ed91482c24df243b2d3
Provides: bundled(golang(github.com/BurntSushi/toml)) = v0.2.0
Provides: bundled(golang(github.com/containerd/cgroups)) = 58556f5ad8448d99a6f7bea69ea4bdb7747cfeb0
Provides: bundled(golang(github.com/containerd/continuity)) = master
#Provides: bundled(golang(github.com/containernetworking/cni)) = v0.7.0-alpha1
Provides: bundled(golang(github.com/containernetworking/plugins)) = 1562a1e60ed101aacc5e08ed9dbeba8e9f3d4ec1
Provides: bundled(golang(github.com/containers/image)) = 85d7559d44fd71f30e46e43d809bfbf88d11d916
Provides: bundled(golang(github.com/containers/psgo)) = 5dde6da0bc8831b35243a847625bcf18183bd1ee
Provides: bundled(golang(github.com/containers/storage)) = 243c4cd616afdf06b4a975f18c4db083d26b1641
Provides: bundled(golang(github.com/coreos/go-iptables)) = 25d087f3cffd9aedc0c2b7eff25f23cbf3c20fe1
Provides: bundled(golang(github.com/coreos/go-systemd)) = v14
Provides: bundled(golang(github.com/cri-o/ocicni)) = master
Provides: bundled(golang(github.com/cyphar/filepath-securejoin)) = v0.2.1
Provides: bundled(golang(github.com/davecgh/go-spew)) = v1.1.0
Provides: bundled(golang(github.com/docker/distribution)) = 7a8efe719e55bbfaff7bc5718cdf0ed51ca821df
Provides: bundled(golang(github.com/docker/docker)) = 86f080cff0914e9694068ed78d503701667c4c00
Provides: bundled(golang(github.com/docker/docker-credential-helpers)) = d68f9aeca33f5fd3f08eeae5e9d175edf4e731d1
Provides: bundled(golang(github.com/docker/go-connections)) = 3ede32e2033de7505e6500d6c868c2b9ed9f169d
Provides: bundled(golang(github.com/docker/go-units)) = v0.3.2
Provides: bundled(golang(github.com/docker/libtrust)) = aabc10ec26b754e797f9028f4589c5b7bd90dc20
Provides: bundled(golang(github.com/docker/spdystream)) = ed496381df8283605c435b86d4fdd6f4f20b8c6e
Provides: bundled(golang(github.com/fatih/camelcase)) = f6a740d52f961c60348ebb109adde9f4635d7540
Provides: bundled(golang(github.com/fsnotify/fsnotify)) = 7d7316ed6e1ed2de075aab8dfc76de5d158d66e1
Provides: bundled(golang(github.com/fsouza/go-dockerclient)) = master
Provides: bundled(golang(github.com/ghodss/yaml)) = 04f313413ffd65ce25f2541bfd2b2ceec5c0908c
Provides: bundled(golang(github.com/godbus/dbus)) = a389bdde4dd695d414e47b755e95e72b7826432c
Provides: bundled(golang(github.com/gogo/protobuf)) = c0656edd0d9eab7c66d1eb0c568f9039345796f7
Provides: bundled(golang(github.com/golang/glog)) = 23def4e6c14b4da8ac2ed8007337bc5eb5007998
Provides: bundled(golang(github.com/golang/groupcache)) = b710c8433bd175204919eb38776e944233235d03
Provides: bundled(golang(github.com/golang/protobuf)) = 4bd1920723d7b7c925de087aa32e2187708897f7
Provides: bundled(golang(github.com/googleapis/gnostic)) = 0c5108395e2debce0d731cf0287ddf7242066aba
Provides: bundled(golang(github.com/google/gofuzz)) = 44d81051d367757e1c7c6a5a86423ece9afcf63c
Provides: bundled(golang(github.com/gorilla/context)) = v1.1
Provides: bundled(golang(github.com/gorilla/mux)) = v1.3.0
Provides: bundled(golang(github.com/hashicorp/errwrap)) = 7554cd9344cec97297fa6649b055a8c98c2a1e55
Provides: bundled(golang(github.com/hashicorp/golang-lru)) = 0a025b7e63adc15a622f29b0b2c4c3848243bbf6
Provides: bundled(golang(github.com/hashicorp/go-multierror)) = 83588e72410abfbe4df460eeb6f30841ae47d4c4
Provides: bundled(golang(github.com/imdario/mergo)) = 0.2.2
Provides: bundled(golang(github.com/json-iterator/go)) = 1.0.0
Provides: bundled(golang(github.com/kr/pty)) = v1.0.0
Provides: bundled(golang(github.com/mailru/easyjson)) = 03f2033d19d5860aef995fe360ac7d395cd8ce65
Provides: bundled(golang(github.com/mattn/go-runewidth)) = v0.0.1
Provides: bundled(golang(github.com/Microsoft/go-winio)) = 78439966b38d69bf38227fbf57ac8a6fee70f69a
Provides: bundled(golang(github.com/Microsoft/hcsshim)) = 43f9725307998e09f2e3816c2c0c36dc98f0c982
Provides: bundled(golang(github.com/mistifyio/go-zfs)) = v2.1.1
Provides: bundled(golang(github.com/mrunalp/fileutils)) = master
Provides: bundled(golang(github.com/mtrmac/gpgme)) = b2432428689ca58c2b8e8dea9449d3295cf96fc9
Provides: bundled(golang(github.com/Nvveen/Gotty)) = master
#Provides: bundled(golang(github.com/opencontainers/go-digest)) = v1.0.0-rc0
Provides: bundled(golang(github.com/opencontainers/image-spec)) = v1.0.0
Provides: bundled(golang(github.com/opencontainers/runc)) = b4e2ecb452d9ee4381137cc0a7e6715b96bed6de
Provides: bundled(golang(github.com/opencontainers/runtime-spec)) = d810dbc60d8c5aeeb3d054bd1132fab2121968ce
Provides: bundled(golang(github.com/opencontainers/runtime-tools)) = master
Provides: bundled(golang(github.com/opencontainers/selinux)) = b6fa367ed7f534f9ba25391cc2d467085dbb445a
Provides: bundled(golang(github.com/openshift/imagebuilder)) = master
Provides: bundled(golang(github.com/ostreedev/ostree-go)) = master
Provides: bundled(golang(github.com/pkg/errors)) = v0.8.0
Provides: bundled(golang(github.com/pmezard/go-difflib)) = 792786c7400a136282c1664665ae0a8db921c6c2
Provides: bundled(golang(github.com/pquerna/ffjson)) = d49c2bc1aa135aad0c6f4fc2056623ec78f5d5ac
Provides: bundled(golang(github.com/projectatomic/buildah)) = af5bbde0180026ae87b7fc81c2dc124aa73ec959
Provides: bundled(golang(github.com/seccomp/containers-golang)) = master
Provides: bundled(golang(github.com/seccomp/libseccomp-golang)) = v0.9.0
Provides: bundled(golang(github.com/sirupsen/logrus)) = v1.0.0
Provides: bundled(golang(github.com/spf13/pflag)) = 9ff6c6923cfffbcd502984b8e0c80539a94968b7
Provides: bundled(golang(github.com/stretchr/testify)) = 4d4bfba8f1d1027c4fdbe371823030df51419987
Provides: bundled(golang(github.com/syndtr/gocapability)) = e7cb7fa329f456b3855136a2642b197bad7366ba
Provides: bundled(golang(github.com/tchap/go-patricia)) = v2.2.6
Provides: bundled(golang(github.com/ulikunitz/xz)) = v0.5.4
Provides: bundled(golang(github.com/ulule/deepcopier)) = master
Provides: bundled(golang(github.com/urfave/cli)) = 934abfb2f102315b5794e15ebc7949e4ca253920
Provides: bundled(golang(github.com/varlink/go)) = master
Provides: bundled(golang(github.com/vbatts/tar-split)) = v0.10.2
Provides: bundled(golang(github.com/vishvananda/netlink)) = master
Provides: bundled(golang(github.com/vishvananda/netns)) = master
Provides: bundled(golang(github.com/xeipuuv/gojsonpointer)) = master
Provides: bundled(golang(github.com/xeipuuv/gojsonreference)) = master
Provides: bundled(golang(github.com/xeipuuv/gojsonschema)) = master
Provides: bundled(golang(golang.org/x/crypto)) = 81e90905daefcd6fd217b62423c0908922eadb30
Provides: bundled(golang(golang.org/x/net)) = c427ad74c6d7a814201695e9ffde0c5d400a7674
Provides: bundled(golang(golang.org/x/sys)) = master
Provides: bundled(golang(golang.org/x/text)) = f72d8390a633d5dfb0cc84043294db9f6c935756
Provides: bundled(golang(golang.org/x/time)) = f51c12702a4d776e4c1fa9b0fabab841babae631
Provides: bundled(golang(google.golang.org/grpc)) = v1.0.4
Provides: bundled(golang(gopkg.in/cheggaaa/pb.v1)) = v1.0.7
Provides: bundled(golang(gopkg.in/inf.v0)) = v0.9.0
Provides: bundled(golang(gopkg.in/mgo.v2)) = v2
Provides: bundled(golang(gopkg.in/square/go-jose.v2)) = v2.1.3
Provides: bundled(golang(gopkg.in/yaml.v2)) = v2
Provides: bundled(golang(k8s.io/api)) = 5ce4aa0bf2f097f6021127b3d879eeda82026be8
Provides: bundled(golang(k8s.io/apiextensions-apiserver)) = 1b31e26d82f1ec2e945c560790e98f34bb5f2e63
Provides: bundled(golang(k8s.io/apimachinery)) = 616b23029fa3dc3e0ccefd47963f5651a6543d94
Provides: bundled(golang(k8s.io/apiserver)) = 4d1163080139f1f9094baf8a3a6099e85e1867f6
Provides: bundled(golang(k8s.io/client-go)) = 7cd1d3291b7d9b1e2d54d4b69eb65995eaf8888e
Provides: bundled(golang(k8s.io/kube-openapi)) = 275e2ce91dec4c05a4094a7b1daee5560b555ac9
Provides: bundled(golang(k8s.io/utils)) = 258e2a2fa64568210fbd6267cf1d8fd87c3cb86e

%description
%{name} (Pod Manager) is a fully featured container engine that is a simple
daemonless tool.  %{name} provides a Docker-CLI comparable command line that
eases the transition from other container engines and allows the management of
pods, containers and images.  Simply put: alias docker=%{name}.
Most %{name} commands can be run as a regular user, without requiring
additional privileges.

%{name} uses Buildah(1) internally to create container images. Both tools
share image (not container) storage, hence each can use or manipulate images
(but not containers) created by the other.

%{summary}
%{repo} Simple management tool for pods, containers and images

%package docker
Summary: Emulate Docker CLI using %{name}
BuildArch: noarch
Requires: %{name} = %{epoch}:%{version}-%{release}
Conflicts: docker
Conflicts: docker-latest
Conflicts: docker-ce
Conflicts: docker-ee
Conflicts: moby-engine

%description docker
This package installs a script named docker that emulates the Docker CLI by
executes %{name} commands, it also creates links between all Docker CLI man
pages and %{name}.

%if 0%{?with_devel}
%package devel
Summary: Library for applications looking to use Container Pods
BuildArch: noarch
Provides: %{repo}-devel = %{epoch}:%{version}-%{release}

%if 0%{?with_check} && ! 0%{?with_bundled}
BuildRequires: golang(github.com/BurntSushi/toml)
BuildRequires: golang(github.com/containerd/cgroups)
BuildRequires: golang(github.com/containernetworking/plugins/pkg/ns)
BuildRequires: golang(github.com/containers/image/copy)
BuildRequires: golang(github.com/containers/image/directory)
BuildRequires: golang(github.com/containers/image/docker)
BuildRequires: golang(github.com/containers/image/docker/archive)
BuildRequires: golang(github.com/containers/image/docker/reference)
BuildRequires: golang(github.com/containers/image/docker/tarfile)
BuildRequires: golang(github.com/containers/image/image)
BuildRequires: golang(github.com/containers/image/oci/archive)
BuildRequires: golang(github.com/containers/image/pkg/strslice)
BuildRequires: golang(github.com/containers/image/pkg/sysregistries)
BuildRequires: golang(github.com/containers/image/signature)
BuildRequires: golang(github.com/containers/image/storage)
BuildRequires: golang(github.com/containers/image/tarball)
BuildRequires: golang(github.com/containers/image/transports/alltransports)
BuildRequires: golang(github.com/containers/image/types)
BuildRequires: golang(github.com/containers/storage)
BuildRequires: golang(github.com/containers/storage/pkg/archive)
BuildRequires: golang(github.com/containers/storage/pkg/idtools)
BuildRequires: golang(github.com/containers/storage/pkg/reexec)
BuildRequires: golang(github.com/coreos/go-systemd/dbus)
BuildRequires: golang(github.com/cri-o/ocicni/pkg/ocicni)
BuildRequires: golang(github.com/docker/distribution/reference)
BuildRequires: golang(github.com/docker/docker/daemon/caps)
BuildRequires: golang(github.com/docker/docker/pkg/mount)
BuildRequires: golang(github.com/docker/docker/pkg/namesgenerator)
BuildRequires: golang(github.com/docker/docker/pkg/stringid)
BuildRequires: golang(github.com/docker/docker/pkg/system)
BuildRequires: golang(github.com/docker/docker/pkg/term)
BuildRequires: golang(github.com/docker/docker/pkg/truncindex)
BuildRequires: golang(github.com/ghodss/yaml)
BuildRequires: golang(github.com/godbus/dbus)
BuildRequires: golang(github.com/mattn/go-sqlite3)
BuildRequires: golang(github.com/mrunalp/fileutils)
BuildRequires: golang(github.com/opencontainers/go-digest)
BuildRequires: golang(github.com/opencontainers/image-spec/specs-go/v1)
BuildRequires: golang(github.com/opencontainers/runc/libcontainer)
BuildRequires: golang(github.com/opencontainers/runtime-spec/specs-go)
BuildRequires: golang(github.com/opencontainers/runtime-tools/generate)
BuildRequires: golang(github.com/opencontainers/selinux/go-selinux)
BuildRequires: golang(github.com/opencontainers/selinux/go-selinux/label)
BuildRequires: golang(github.com/pkg/errors)
BuildRequires: golang(github.com/sirupsen/logrus)
BuildRequires: golang(github.com/ulule/deepcopier)
BuildRequires: golang(golang.org/x/crypto/ssh/terminal)
BuildRequires: golang(golang.org/x/sys/unix)
BuildRequires: golang(k8s.io/apimachinery/pkg/util/wait)
BuildRequires: golang(k8s.io/client-go/tools/remotecommand)
BuildRequires: golang(k8s.io/kubernetes/pkg/kubelet/container)
%endif

Requires: golang(github.com/BurntSushi/toml)
Requires: golang(github.com/containerd/cgroups)
Requires: golang(github.com/containernetworking/plugins/pkg/ns)
Requires: golang(github.com/containers/image/copy)
Requires: golang(github.com/containers/image/directory)
Requires: golang(github.com/containers/image/docker)
Requires: golang(github.com/containers/image/docker/archive)
Requires: golang(github.com/containers/image/docker/reference)
Requires: golang(github.com/containers/image/docker/tarfile)
Requires: golang(github.com/containers/image/image)
Requires: golang(github.com/containers/image/oci/archive)
Requires: golang(github.com/containers/image/pkg/strslice)
Requires: golang(github.com/containers/image/pkg/sysregistries)
Requires: golang(github.com/containers/image/signature)
Requires: golang(github.com/containers/image/storage)
Requires: golang(github.com/containers/image/tarball)
Requires: golang(github.com/containers/image/transports/alltransports)
Requires: golang(github.com/containers/image/types)
Requires: golang(github.com/containers/storage)
Requires: golang(github.com/containers/storage/pkg/archive)
Requires: golang(github.com/containers/storage/pkg/idtools)
Requires: golang(github.com/containers/storage/pkg/reexec)
Requires: golang(github.com/coreos/go-systemd/dbus)
Requires: golang(github.com/cri-o/ocicni/pkg/ocicni)
Requires: golang(github.com/docker/distribution/reference)
Requires: golang(github.com/docker/docker/daemon/caps)
Requires: golang(github.com/docker/docker/pkg/mount)
Requires: golang(github.com/docker/docker/pkg/namesgenerator)
Requires: golang(github.com/docker/docker/pkg/stringid)
Requires: golang(github.com/docker/docker/pkg/system)
Requires: golang(github.com/docker/docker/pkg/term)
Requires: golang(github.com/docker/docker/pkg/truncindex)
Requires: golang(github.com/ghodss/yaml)
Requires: golang(github.com/godbus/dbus)
Requires: golang(github.com/mattn/go-sqlite3)
Requires: golang(github.com/mrunalp/fileutils)
Requires: golang(github.com/opencontainers/go-digest)
Requires: golang(github.com/opencontainers/image-spec/specs-go/v1)
Requires: golang(github.com/opencontainers/runc/libcontainer)
Requires: golang(github.com/opencontainers/runtime-spec/specs-go)
Requires: golang(github.com/opencontainers/runtime-tools/generate)
Requires: golang(github.com/opencontainers/selinux/go-selinux)
Requires: golang(github.com/opencontainers/selinux/go-selinux/label)
Requires: golang(github.com/pkg/errors)
Requires: golang(github.com/sirupsen/logrus)
Requires: golang(github.com/ulule/deepcopier)
Requires: golang(golang.org/x/crypto/ssh/terminal)
Requires: golang(golang.org/x/sys/unix)
Requires: golang(k8s.io/apimachinery/pkg/util/wait)
Requires: golang(k8s.io/client-go/tools/remotecommand)
Requires: golang(k8s.io/kubernetes/pkg/kubelet/container)

Provides: golang(%{import_path}/cmd/%{name}/docker) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/cmd/%{name}/formats) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/libkpod) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/libpod) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/libpod/common) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/libpod/driver) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/libpod/layers) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/annotations) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/chrootuser) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/registrar) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/pkg/storage) = %{epoch}:%{version}-%{release}
Provides: golang(%{import_path}/utils) = %{epoch}:%{version}-%{release}

%description -n %{name}-devel
%{summary}

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test-devel
Summary:         Unit tests for %{name} package
%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires: %{name}-devel = %{epoch}:%{version}-%{release}

%if 0%{?with_check} && ! 0%{?with_bundled}
BuildRequires: golang(github.com/stretchr/testify/assert)
BuildRequires: golang(github.com/urfave/cli)
%endif

Requires: golang(github.com/stretchr/testify/assert)
Requires: golang(github.com/urfave/cli)

%description unit-test-devel
%{summary}
%{name} provides a library for applications looking to use the Container Pod
concept popularized by Kubernetes.

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%package tests
Summary: Tests for %{name}

Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: bats
Requires: jq

%description tests
%{summary}

This package contains system tests for %{name}

%if 0%{?rhel} > 7 || 0%{?fedora}
%package remote
Summary: (Experimental) Remote client for managing %{name} containers
Recommends: %{name}-manpages = %{epoch}:%{version}-%{release}

%description remote
Remote client for managing %{name} containers.

This experimental remote client is under heavy development. Please do not
run %{name}-remote in production.

%{name}-remote uses the varlink connection to connect to a %{name} client to
manage pods, containers and container images. %{name}-remote supports ssh
connections as well.
%endif

%package manpages
Summary: Man pages for the %{name} commands
BuildArch: noarch

%files manpages
%{_mandir}/man1/%{name}*.1*
%{_mandir}/man5/*.5*

%description manpages
Man pages for the %{name} commands

%prep
%autosetup -Sgit -n %{repo}-%{commit0}

%build
mkdir _build
pushd _build
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s ../../../../ src/%{import_path}
popd
ln -s vendor src
export GOPATH=$(pwd)/_build:$(pwd)
export GO111MODULE=off

%if 0%{?rhel} > 7 || 0%{?fedora}
%gogenerate ./cmd/%{name}/varlink/...
%endif

export BUILDTAGS="systemd
%if 0%{?rhel} > 7 || 0%{?fedora}
                  varlink
                  remoteclient
%endif
                  seccomp
                  exclude_graphdriver_devicemapper
                  $(hack/btrfs_installed_tag.sh)
                  $(hack/btrfs_tag.sh)
                  $(hack/libdm_tag.sh)
                  $(hack/ostree_tag.sh)
                  $(hack/selinux_tag.sh)"

%gobuild -o bin/%{name} %{import_path}/cmd/%{name}

%if 0%{?rhel} > 7 || 0%{?fedora}
%gobuild -o bin/%{name}-remote %{import_path}/cmd/%{name}
%endif

%install
sed -s 's/^runtime[ =].*"runc/runtime = "crun/' libpod.conf  -i
sed -i 's/install.remote: podman-remote/install.remote:/' Makefile
sed -i 's/install.bin: podman/install.bin:/' Makefile
rm -rf docs/containers-mounts.conf.5.md

install -dp %{buildroot}%{_unitdir}
PODMAN_VERSION=%{version} %{__make} PREFIX=%{buildroot}%{_prefix} ETCDIR=%{buildroot}%{_sysconfdir} \
        install.bin \
%if 0%{?rhel} > 7 || 0%{?fedora}
        install.remote \
%endif
        install.man \
        install.cni \
        install.systemd \
        install.completions \
        install.docker

mv pkg/hooks/README.md pkg/hooks/README-hooks.md

# install libpod.conf
install -dp %{buildroot}%{_datadir}/containers
install -p -m 644 %{repo}.conf %{buildroot}%{_datadir}/containers

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/

echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . \( -iname "*.go" -or -iname "*.s" \) \! -iname "*_test.go" | grep -v "vendor") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test-devel.file-list
for file in $(find . -iname "*_test.go" | grep -v "vendor") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test-devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

# https://bugzilla.redhat.com/show_bug.cgi?id=1657303#c3 varlink not in rhel 7
rm -f %{buildroot}/{%{_unitdir},%{_userunitdir}}/io.%{name}.{service,socket}

%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
# Since we aren't packaging up the vendor directory we need to link
# back to it somehow. Hack it up so that we can add the vendor
# directory from BUILD dir as a gopath to be searched when executing
# tests from the BUILDROOT dir.
ln -s ./ ./vendor/src # ./vendor/src -> ./vendor

export GOPATH=%{buildroot}/%{gopath}:$(pwd)/vendor:%{gopath}
%endif

%if ! 0%{?gotest:1}
%global gotest go test
%endif

%gotest %{import_path}/cmd/%{name}
%gotest %{import_path}/libkpod
%gotest %{import_path}/libpod
%gotest %{import_path}/pkg/registrar
%endif

install -d -p %{buildroot}/%{_datadir}/%{name}/test/system
cp -pav test/system %{buildroot}/%{_datadir}/%{name}/test/

%triggerpostun -- %{name} < 1.1
%{_bindir}/%{name} system renumber
exit 0

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE
%doc README.md CONTRIBUTING.md pkg/hooks/README-hooks.md install.md code-of-conduct.md transfer.md
%{_bindir}/%{name}
%{_datadir}/bash-completion/completions/*
# By "owning" the site-functions dir, we don't need to Require zsh
%dir %{_datadir}/zsh/site-functions
%{_datadir}/zsh/site-functions/_%{name}
%config(noreplace) %{_sysconfdir}/cni/net.d/87-%{name}-bridge.conflist
%{_datadir}/containers/%{repo}.conf

%if 0%{?rhel} > 7 || 0%{?fedora}
%{_unitdir}/io.%{name}.service
%{_unitdir}/io.%{name}.socket
%{_userunitdir}/io.%{name}.service
%{_userunitdir}/io.%{name}.socket
%endif

%{_usr}/lib/tmpfiles.d/%{name}.conf

%files docker
%{_bindir}/docker
%{_mandir}/man1/docker*.1*

%if 0%{?with_devel}
%files -n %{name}-devel -f devel.file-list
%license LICENSE
%doc README.md CONTRIBUTING.md pkg/hooks/README-hooks.md install.md code-of-conduct.md transfer.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files unit-test-devel -f unit-test-devel.file-list
%license LICENSE
%doc README.md CONTRIBUTING.md pkg/hooks/README-hooks.md install.md code-of-conduct.md transfer.md
%endif

%if 0%{?rhel} > 7 || 0%{?fedora}
%files remote
%license LICENSE
%{_bindir}/%{name}-remote
%endif

%files tests
%license LICENSE
%{_datadir}/%{name}/test

%changelog
* Sat Dec 28 2019 Alberto Chiusole <bebo.sudo@gmail.com> - 1.6.2-3
- Rebuild v1.6.2 for centos from fc31, using 1.4.4-4.el7 go build configs, without varlink

* Thu Oct 17 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-2
- bump to v1.6.2
- autobuilt f3ffda1

* Wed Oct 16 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.2-0.2.rc1
- bump to v1.6.2-rc1
- autobuilt 4d653f0

* Wed Oct 09 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.6.1-5
- remove polkit dependency for now

* Wed Oct 09 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.6.1-4
- Requires: crun >= 0.10.2-1 and polkit

* Tue Oct 08 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.6.1-3
- add Recommends: runc for fedora

* Wed Oct 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.1-2
- bump to v1.6.1
- autobuilt 233d95f

* Wed Oct 02 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.1-0.2.rc1
- bump to v1.6.1-rc1
- autobuilt a2fdb6e

* Tue Oct 01 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.6.0-4
- Requires: crun >= 0.10-1

* Tue Oct 01 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.6.0-3
- bump release tag

* Tue Oct 01 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.0-2
- bump to v1.6.0
- autobuilt b02b072

* Wed Sep 25 2019 RH Container Bot <rhcontainerbot@fedoraproject.org> - 2:1.6.0-0.2.rc2.git9181c65
- bump to v1.6.0-rc2
- autobuilt 9181c65

* Tue Sep 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.6.0-2.gitca5ff03
- bump to v1.6.0-rc1
- autobuilt ca5ff03

* Sat Sep 14 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.5.1-3.git0005792
- use v1.5.1 tag
- use conmon package as runtime dep

* Fri Sep 13 2019 Daniel J Walsh <dwalsh@redhat.com> - 2:1.5.1-2.18
- Grab specific version of crun or newer.

* Tue Aug 27 2019 Daniel J Walsh <dwalsh@redhat.com> - 2:1.5.1-2.17
- Require crun rather then runc
- Switch to crun by default for cgroupsV2 support

* Thu Aug 22 2019 Daniel J Walsh <dwalsh@redhat.com> - 2:1.5.1-2.16.dev.gitce64c14
- Move man5 man pages into podman-manpage package

* Tue Aug 13 2019 Dan Walsh <dwalsh@fedoraproject.org> - 2:1.5.1-1.16.dev.gitce64c14
- Add recommends libvarlink-util

* Tue Aug 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.16.dev.gitce64c14
- autobuilt ce64c14

* Tue Aug 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.15.dev.git7a859f0
- autobuilt 7a859f0

* Tue Aug 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.14.dev.git031437b
- autobuilt 031437b

* Tue Aug 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.13.dev.gitc48243e
- autobuilt c48243e

* Mon Aug 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.12.dev.gitf634fd3
- autobuilt f634fd3

* Mon Aug 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.11.dev.git3cf4567
- autobuilt 3cf4567

* Mon Aug 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.10.dev.git9bee690
- autobuilt 9bee690

* Mon Aug 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.9.dev.gitca7bae7
- autobuilt ca7bae7

* Mon Aug 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.8.dev.gitec93c9d
- autobuilt ec93c9d

* Mon Aug 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.7.dev.gitf18cfa4
- autobuilt f18cfa4

* Mon Aug 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.6.dev.git2348c28
- autobuilt 2348c28

* Sun Aug 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.5.dev.git1467197
- autobuilt 1467197

* Sun Aug 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.4.dev.git7bbaa36
- autobuilt 7bbaa36

* Sat Aug 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.3.dev.git3bc861c
- autobuilt 3bc861c

* Sat Aug 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.2.dev.git926901d
- autobuilt 926901d

* Fri Aug 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.5.1-0.1.dev.git2018faa
- bump to 1.5.1
- autobuilt 2018faa

* Fri Aug 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.99.dev.gitbb80586
- autobuilt bb80586

* Fri Aug 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.98.dev.gitd05798e
- autobuilt d05798e

* Fri Aug 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.97.dev.git4b91f60
- autobuilt 4b91f60

* Fri Aug 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.96.dev.gitdc38168
- autobuilt dc38168

* Fri Aug 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.95.dev.git00a20f7
- autobuilt 00a20f7

* Fri Aug 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.94.dev.git2a19036
- autobuilt 2a19036

* Fri Aug 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.93.dev.git76840f2
- autobuilt 76840f2

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.92.dev.git4349f42
- autobuilt 4349f42

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.91.dev.git202eade
- autobuilt 202eade

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.90.dev.git09cedd1
- autobuilt 09cedd1

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.89.dev.git3959a35
- autobuilt 3959a35

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.88.dev.git5701fe6
- autobuilt 5701fe6

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.87.dev.git31bfb12
- autobuilt 31bfb12

* Thu Aug 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.86.dev.git41de7b1
- autobuilt 41de7b1

* Wed Aug 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.85.dev.git35ecf49
- autobuilt 35ecf49

* Wed Aug 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.84.dev.git66ea32c
- autobuilt 66ea32c

* Tue Aug 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.83.dev.gitf0a5b7f
- autobuilt f0a5b7f

* Tue Aug 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.82.dev.gitb5618d9
- autobuilt b5618d9

* Mon Aug 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.81.dev.git3bffe77
- autobuilt 3bffe77

* Mon Aug 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.80.dev.git337358a
- autobuilt 337358a

* Mon Aug 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.79.dev.git626dfdb
- autobuilt 626dfdb

* Mon Aug 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.78.dev.gite2f38cd
- autobuilt e2f38cd

* Mon Aug 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.77.dev.gitb609de2
- autobuilt b609de2

* Sun Aug 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.76.dev.git389a7b7
- autobuilt 389a7b7

* Sun Aug 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.75.dev.gitd9ea4db
- autobuilt d9ea4db

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.74.dev.git140e08e
- autobuilt 140e08e

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.73.dev.git3cc9ab8
- autobuilt 3cc9ab8

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.72.dev.git5370c53
- autobuilt 5370c53

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.71.dev.git2cc5913
- autobuilt 2cc5913

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.70.dev.gite3240da
- autobuilt e3240da

* Fri Aug 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.69.dev.gite48dc50
- autobuilt e48dc50

* Thu Aug 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.68.dev.git1bbcb2f
- autobuilt 1bbcb2f

* Thu Aug 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.67.dev.gite1a099e
- autobuilt e1a099e

* Thu Aug 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.66.dev.gitafb493a
- autobuilt afb493a

* Thu Aug 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.65.dev.git6f62dac
- autobuilt 6f62dac

* Thu Aug 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.64.dev.gitee15e76
- autobuilt ee15e76

* Thu Aug 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.63.dev.git5056964
- autobuilt 5056964

* Thu Aug 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.62.dev.git3215ea6
- autobuilt 3215ea6

* Thu Aug 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.61.dev.gitccf4ec2
- autobuilt ccf4ec2

* Wed Jul 31 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.60.dev.gita622f8d
- autobuilt a622f8d

* Tue Jul 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.59.dev.git680a383
- autobuilt 680a383

* Tue Jul 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.58.dev.gite84ed3c
- autobuilt e84ed3c

* Tue Jul 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.57.dev.git1a00895
- autobuilt 1a00895

* Tue Jul 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.56.dev.git4196a59
- autobuilt 4196a59

* Tue Jul 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.55.dev.git040355d
- autobuilt 040355d

* Mon Jul 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.54.dev.git7d635ac
- autobuilt 7d635ac

* Mon Jul 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.53.dev.gitc3c45f3
- autobuilt c3c45f3

* Mon Jul 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.52.dev.git6665269
- autobuilt 6665269

* Mon Jul 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.51.dev.git2ca7861
- autobuilt 2ca7861

* Sun Jul 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.50.dev.git2c98bd5
- autobuilt 2c98bd5

* Fri Jul 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.49.dev.git0c4dfcf
- autobuilt 0c4dfcf

* Fri Jul 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.48.dev.giteca157f
- autobuilt eca157f

* Fri Jul 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.47.dev.git1910d68
- autobuilt 1910d68

* Fri Jul 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.46.dev.git4674d00
- autobuilt 4674d00

* Thu Jul 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.45.dev.gitdff82d9
- autobuilt dff82d9

* Thu Jul 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.44.dev.git5763618
- autobuilt 5763618

* Thu Jul 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.43.dev.git7c9095e
- autobuilt 7c9095e

* Wed Jul 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.42.dev.git2283471
- autobuilt 2283471

* Wed Jul 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.41.dev.git0917783
- autobuilt 0917783

* Wed Jul 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.40.dev.giteae9a00
- autobuilt eae9a00

* Wed Jul 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.39.dev.git3c6b111
- autobuilt 3c6b111

* Tue Jul 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.38.dev.git7dbc6d8
- autobuilt 7dbc6d8

* Tue Jul 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.37.dev.gitbb253af
- autobuilt bb253af

* Tue Jul 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.36.dev.gitce60c4d
- autobuilt ce60c4d

* Tue Jul 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.35.dev.git2674920
- autobuilt 2674920

* Mon Jul 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.34.dev.gita12a231
- autobuilt a12a231

* Mon Jul 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.33.dev.gitcf9efa9
- autobuilt cf9efa9

* Mon Jul 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.32.dev.git69f74f1
- autobuilt 69f74f1

* Mon Jul 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.31.dev.gitab7b47c
- autobuilt ab7b47c

* Mon Jul 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.30.dev.git3b52e4d
- autobuilt 3b52e4d

* Sun Jul 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.29.dev.gitd6b41eb
- autobuilt d6b41eb

* Sat Jul 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.28.dev.gita5aa44c
- autobuilt a5aa44c

* Sat Jul 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.27.dev.git8364552
- autobuilt 8364552

* Fri Jul 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.26.dev.git02140ea
- autobuilt 02140ea

* Fri Jul 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.25.dev.git398aeac
- autobuilt 398aeac

* Fri Jul 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.24.dev.gitdeb087d
- autobuilt deb087d

* Fri Jul 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.23.dev.gitb59abdc
- autobuilt b59abdc

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.22.dev.git2254a35
- autobuilt 2254a35

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.21.dev.git1065548
- autobuilt 1065548

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.20.dev.gitade0d87
- autobuilt ade0d87

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.19.dev.git22e62e8
- autobuilt 22e62e8

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.18.dev.gitadcde23
- autobuilt adcde23

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.17.dev.git456c045
- autobuilt 456c045

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.16.dev.git7488ed6
- autobuilt 7488ed6

* Thu Jul 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.15.dev.gitb2734ba
- autobuilt b2734ba

* Wed Jul 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.14.dev.git1c02905
- autobuilt 1c02905

* Wed Jul 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.13.dev.git04a9cb0
- autobuilt 04a9cb0

* Tue Jul 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.12.dev.gitfe83308
- autobuilt fe83308

* Tue Jul 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.11.dev.git400851a
- autobuilt 400851a

* Tue Jul 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.10.dev.gita449e9a
- autobuilt a449e9a

* Tue Jul 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.9.dev.git386ffd2
- autobuilt 386ffd2

* Tue Jul 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.8.dev.git7e4db44
- autobuilt 7e4db44

* Mon Jul 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.7.dev.gitd2291ec
- autobuilt d2291ec

* Sun Jul 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.6.dev.git456b6ab
- autobuilt 456b6ab

* Fri Jul 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.5.dev.gite2e8477
- built conmon 1de71ad

* Thu Jul 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.4.dev.gite2e8477
- autobuilt e2e8477

* Wed Jul 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.5-0.3.dev.gitdf3f5af
- autobuilt df3f5af

* Tue Jul 09 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.4.5-0.2.dev.gitcea0e93
- Resolves: #1727933 - containers-monuts.conf.5 moved to containers-common

* Sun Jul 07 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.4.5-0.1.dev.gitf7407f2
- bump to v1.4.5-dev
- use new name for go-md2man
- include centos conditionals

* Sun Jun 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.3-0.30.dev.git7c4e444
- autobuilt 7c4e444

* Sat Jun 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.3-0.29.dev.gitd9bdd3c
- autobuilt d9bdd3c

* Fri Jun 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.3-0.28.dev.git39fdf91
- autobuilt 39fdf91

* Thu Jun 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.3-0.27.dev.gitb4f9bc8
- autobuilt b4f9bc8

* Wed Jun 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.3-0.26.dev.git240b846
- bump to 1.4.3
- autobuilt 240b846

* Tue Jun 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.2-0.25.dev.git8bcfd24
- autobuilt 8bcfd24

* Sun Jun 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.2-0.24.dev.git670fc03
- autobuilt 670fc03

* Sat Jun 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.2-0.23.dev.git185b413
- bump to 1.4.2
- autobuilt 185b413

* Fri Jun 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.1-0.22.dev.git2784cf3
- autobuilt 2784cf3

* Thu Jun 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.1-0.21.dev.git77d1cf0
- autobuilt 77d1cf0

* Wed Jun 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.1-0.20.dev.gitf8a84fd
- autobuilt f8a84fd

* Tue Jun 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.1-0.19.dev.gitc93b8d6
- do not install /usr/libexec/crio - conflicts with crio

* Tue Jun 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.1-0.18.dev.gitc93b8d6
- autobuilt c93b8d6

* Mon Jun 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.1-0.17.dev.gitfcb7c14
- autobuilt fcb7c14

* Sun Jun 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.1-0.16.dev.git39f5ea4
- autobuilt 39f5ea4

* Sat Jun 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.4.1-0.15.dev.gitcae5af5
- bump to 1.4.1
- autobuilt cae5af5

* Fri Jun 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.2-0.14.dev.gitba36a5f
- autobuilt ba36a5f

* Fri Jun 07 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.3.2-0.13.dev.git6d285b8
- Resolves: #1716809 - use conmon v0.2.0

* Thu Jun 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.2-0.12.dev.git6d285b8
- autobuilt 6d285b8

* Wed Jun 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.2-0.11.dev.git3fb9669
- autobuilt 3fb9669

* Tue Jun 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.2-0.10.dev.git0ede794
- autobuilt 0ede794

* Sun Jun 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.2-0.9.dev.git176a41c
- autobuilt 176a41c

* Sat Jun 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.2-0.8.dev.git2068919
- autobuilt 2068919

* Fri May 31 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.2-0.7.dev.git558ce8d
- autobuilt 558ce8d

* Thu May 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.2-0.6.dev.gitc871653
- autobuilt c871653

* Wed May 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.2-0.5.dev.git8649dbd
- autobuilt 8649dbd

* Mon May 27 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.2-0.4.dev.git25f8c21
- autobuilt 25f8c21

* Sun May 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.2-0.3.dev.gitb1d590b
- autobuilt b1d590b

* Fri May 24 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.3.2-0.2.dev.git1ac06d8
- built commit 1ac06d8
- BR: systemd-devel
- correct build steps for %%{name}-remote

* Fri May 24 2019 Dan Walsh <dwalsh@fedoraproject.org> - 2:1.3.2-0.1.dev.git5296428
- Bump up to latest on master

* Fri May 10 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.3.1-0.1.dev.git9ae3221
- bump to v1.3.1-dev
- built 9ae3221
- correct release tag format for unreleased versions

* Thu Apr 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-21.dev.gitb01fdcb
- autobuilt b01fdcb

* Tue Apr 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-20.dev.gitd652c86
- autobuilt d652c86

* Sat Apr 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-19.dev.git9f92b21
- autobuilt 9f92b21

* Fri Apr 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-18.dev.gite4947e5
- autobuilt e4947e5

* Thu Apr 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-17.dev.gitbf5ffda
- autobuilt bf5ffda

* Wed Apr 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-16.dev.gita87cf6f
- autobuilt a87cf6f

* Tue Apr 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-15.dev.gitc1e2b58
- autobuilt c1e2b58

* Mon Apr 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-14.dev.git167ce59
- autobuilt 167ce59

* Sun Apr 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-13.dev.gitb926005
- autobuilt b926005

* Sat Apr 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-12.dev.git1572367
- autobuilt 1572367

* Fri Apr 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-11.dev.git387d601
- autobuilt 387d601

* Thu Apr 11 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-10.dev.git6cd6eb6
- autobuilt 6cd6eb6

* Wed Apr 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-9.dev.git60ef8f8
- autobuilt 60ef8f8

* Tue Apr 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-8.dev.gitc94903a
- autobuilt c94903a

* Sat Apr 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-7.dev.gitbc320be
- autobuilt bc320be

* Fri Apr 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-6.dev.gitbda28c6
- autobuilt bda28c6

* Thu Apr 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-5.dev.git4bda537
- autobuilt 4bda537

* Wed Apr 03 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.3.0-4.dev.gitad467ba
- Resolves: #1695492 - own /usr/libexec/podman

* Tue Apr 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-3.dev.gitad467ba
- autobuilt ad467ba

* Mon Apr 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.3.0-2.dev.gitcd35e20
- bump to 1.3.0
- autobuilt cd35e20

* Sun Mar 31 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-30.dev.git833204d
- autobuilt 833204d

* Sat Mar 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-29.dev.git7b73974
- autobuilt 7b73974

* Fri Mar 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-28.dev.gitfdf979a
- autobuilt fdf979a

* Thu Mar 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-27.dev.git850326c
- autobuilt 850326c

* Wed Mar 27 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-26.dev.gitfc546d4
- autobuilt fc546d4

* Mon Mar 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-25.dev.gitd0c6a35
- autobuilt d0c6a35

* Sat Mar 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-24.dev.git0458daf
- autobuilt 0458daf

* Fri Mar 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-23.dev.git68e3df3
- autobuilt 68e3df3

* Thu Mar 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-22.dev.gitc230f0c
- autobuilt c230f0c

* Wed Mar 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-21.dev.git537c382
- autobuilt 537c382

* Tue Mar 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-20.dev.gitac523cb
- autobuilt ac523cb

* Mon Mar 18 2019 Eduardo Santiago <santiago@redhat.com> - 2:1.2.0-19.dev.git6aa8078
- include zsh completion

* Fri Mar 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-18.dev.git31f11a8
- autobuilt 31f11a8

* Thu Mar 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-17.dev.git7426d4f
- autobuilt 7426d4f

* Wed Mar 13 2019 Eduardo Santiago <santiago@redhat.com> - 2:1.2.0-16.dev.git883566f
- new -tests subpackage

* Wed Mar 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-15.dev.git883566f
- autobuilt 883566f

* Tue Mar 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-14.dev.gitde0192a
- autobuilt de0192a

* Sun Mar 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-13.dev.gitd95f97a
- autobuilt d95f97a

* Sat Mar 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-12.dev.git9b21f14
- autobuilt 9b21f14

* Fri Mar 08 2019 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:1.2.0-11.dev.git1b2f867
- Resolves: #1686813 - conmon bundled inside podman rpm

* Fri Mar 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-10.dev.git1b2f867
- autobuilt 1b2f867

* Thu Mar 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-9.dev.git614409f
- autobuilt 614409f

* Wed Mar 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-8.dev.git40f7843
- autobuilt 40f7843

* Tue Mar 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-7.dev.git4b80517
- autobuilt 4b80517

* Mon Mar 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-6.dev.gitf3a3d8e
- autobuilt f3a3d8e

* Sat Mar 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-5.dev.git9adcda7
- autobuilt 9adcda7

* Fri Mar 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-4.dev.git9137315
- autobuilt 9137315

* Thu Feb 28 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-3.dev.git5afae0b
- autobuilt 5afae0b

* Wed Feb 27 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.2.0-2.dev.git623fcfa
- bump to 1.2.0
- autobuilt 623fcfa

* Tue Feb 26 2019 Dan Walsh <dwalsh@fedoraproject.org> - 2:1.0.1-39.dev.gitcf52144
* Tue Feb 26 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-38.dev.gitcf52144
- autobuilt cf52144

* Mon Feb 25 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-37.dev.git553ac80
- autobuilt 553ac80

* Sun Feb 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-36.dev.gitcc4addd
- autobuilt cc4addd

* Sat Feb 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-35.dev.gitb223d4e
- autobuilt b223d4e

* Fri Feb 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-34.dev.git1788add
- autobuilt 1788add

* Thu Feb 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-33.dev.git4934bf2
- autobuilt 4934bf2

* Wed Feb 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-32.dev.git3b88c73
- autobuilt 3b88c73

* Tue Feb 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-31.dev.git228d1cb
- autobuilt 228d1cb

* Mon Feb 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-30.dev.git3f32eae
- autobuilt 3f32eae

* Sun Feb 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-29.dev.git1cb16bd
- autobuilt 1cb16bd

* Sat Feb 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-28.dev.git0a521e1
- autobuilt 0a521e1

* Fri Feb 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-27.dev.git81ace5c
- autobuilt 81ace5c

* Thu Feb 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-26.dev.gitdfc64e1
- autobuilt dfc64e1

* Wed Feb 13 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-25.dev.gitee27c39
- autobuilt ee27c39

* Tue Feb 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-24.dev.git8923703
- autobuilt 8923703

* Sun Feb 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-23.dev.gitc86e8f1
- autobuilt c86e8f1

* Sat Feb 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-22.dev.gitafd4d5f
- autobuilt afd4d5f

* Fri Feb 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-21.dev.git962850c
- autobuilt 962850c

* Thu Feb 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-20.dev.gitf250745
- autobuilt f250745

* Wed Feb 06 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-19.dev.git650e242
- autobuilt 650e242

* Tue Feb 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-18.dev.git778f986
- autobuilt 778f986

* Sun Feb 03 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-17.dev.gitd5593b8
- autobuilt d5593b8

* Sat Feb 02 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-16.dev.gite6426af
- autobuilt e6426af

* Fri Feb 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-15.dev.gite97dc8e
- autobuilt e97dc8e

* Thu Jan 31 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-14.dev.git805c6d9
- autobuilt 805c6d9

* Wed Jan 30 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-13.dev.gitad5579e
- autobuilt ad5579e

* Tue Jan 29 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-12.dev.gitebe9297
- autobuilt ebe9297

* Thu Jan 24 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-11.dev.gitc9e1f36
- autobuilt c9e1f36

* Wed Jan 23 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-10.dev.git7838a13
- autobuilt 7838a13

* Tue Jan 22 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-9.dev.gitec96987
- autobuilt ec96987

* Mon Jan 21 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-8.dev.gitef2f6f9
- autobuilt ef2f6f9

* Sun Jan 20 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-7.dev.git579fc0f
- autobuilt 579fc0f

* Sat Jan 19 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-6.dev.git0d4bfb0
- autobuilt 0d4bfb0

* Fri Jan 18 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-5.dev.gite3dc660
- autobuilt e3dc660

* Thu Jan 17 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-4.dev.git0e3264a
- autobuilt 0e3264a

* Wed Jan 16 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-3.dev.git1b2f752
- autobuilt 1b2f752

* Tue Jan 15 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:1.0.1-2.dev.git6301f6a
- bump to 1.0.1
- autobuilt 6301f6a

* Mon Jan 14 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-3.dev.git140ae25
- autobuilt 140ae25

* Sat Jan 12 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-2.dev.git5c86efb
- bump to 0.12.2
- autobuilt 5c86efb

* Fri Jan 11 2019 bbaude <bbaude@redhat.com> - 1:1.0.0-1.dev.git82e8011
- Upstream 1.0.0 release

* Thu Jan 10 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-27.dev.git0f6535c
- autobuilt 0f6535c

* Wed Jan 09 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-26.dev.gitc9d63fe
- autobuilt c9d63fe

* Tue Jan 08 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-25.dev.gitfaa2462
- autobuilt faa2462

* Mon Jan 07 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-24.dev.gitb83b07c
- autobuilt b83b07c

* Sat Jan 05 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-23.dev.git4e0c0ec
- autobuilt 4e0c0ec

* Fri Jan 04 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-22.dev.git9ffd480
- autobuilt 9ffd480

* Thu Jan 03 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-21.dev.git098c134
- autobuilt 098c134

* Tue Jan 01 2019 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-20.dev.git7438b7b
- autobuilt 7438b7b

* Sat Dec 29 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-1.nightly.git5c86efb9.dev.git1aa55ed
- autobuilt 1aa55ed

* Thu Dec 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 2:0.12.2-1.nightly.git5c86efb8.dev.gitc50332d
- Enable python dependency generator

* Tue Dec 25 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-1.nightly.git5c86efb7.dev.gitc50332d
- autobuilt c50332d

* Mon Dec 24 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-1.nightly.git5c86efb6.dev.git8fe3050
- autobuilt 8fe3050

* Sun Dec 23 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-1.nightly.git5c86efb5.dev.git792f109
- autobuilt 792f109

* Sat Dec 22 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-1.nightly.git5c86efb4.dev.gitfe186c6
- autobuilt fe186c6

* Fri Dec 21 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-1.nightly.git5c86efb3.dev.gitfa998f2
- autobuilt fa998f2

* Thu Dec 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-1.nightly.git5c86efb2.dev.git6b059a5
- autobuilt 6b059a5

* Wed Dec 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-1.nightly.git5c86efb1.dev.gitc8eaf59
- autobuilt c8eaf59

* Tue Dec 18 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-1.nightly.git5c86efb0.dev.git68414c5
- autobuilt 68414c5

* Mon Dec 17 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-9.dev.gitb21d474
- autobuilt b21d474

* Sat Dec 15 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-8.dev.gitc086118
- autobuilt c086118

* Fri Dec 14 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-7.dev.git93b5ccf
- autobuilt 93b5ccf

* Thu Dec 13 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-6.dev.git508388b
- autobuilt 508388b

* Wed Dec 12 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-5.dev.git8a3361f
- autobuilt 8a3361f

* Tue Dec 11 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-4.dev.git235a630
- autobuilt 235a630

* Sat Dec 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-3.dev.git1f547b2
- autobuilt 1f547b2

* Fri Dec 07 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.12.2-2.dev.gita387c72
- bump to 0.12.2
- autobuilt a387c72

* Thu Dec 06 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-15.dev.git75b19ca
- autobuilt 75b19ca

* Wed Dec 05 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-14.dev.git320085a
- autobuilt 320085a

* Tue Dec 04 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-13.dev.git5f6ad82
- autobuilt 5f6ad82

* Sun Dec 02 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-12.dev.git41f250c
- autobuilt 41f250c

* Sat Dec 01 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-11.dev.git6b8f89d
- autobuilt 6b8f89d

* Thu Nov 29 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-10.dev.git3af62f6
- autobuilt 3af62f6

* Tue Nov 27 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-9.dev.git3956050
- autobuilt 3956050

* Mon Nov 26 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-8.dev.gite3ece3b
- autobuilt e3ece3b

* Sat Nov 24 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-7.dev.git78604c3
- autobuilt 78604c3

* Thu Nov 22 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-6.dev.git1fdfeb8
- autobuilt 1fdfeb8

* Wed Nov 21 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-5.dev.git23feb0d
- autobuilt 23feb0d

* Tue Nov 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-4.dev.gitea928f2
- autobuilt ea928f2

* Sat Nov 17 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-3.dev.gitcd5742f
- autobuilt cd5742f

* Fri Nov 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 2:0.11.2-2.dev.git236408b
- autobuilt 236408b

* Wed Nov 14 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:0.11.2-1.dev.git97bded4
- bump epoch cause previous version was messed up
- built 97bded4

* Tue Nov 13 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.11.20.11.2-1.dev.git79657161
- bump to 0.11.2
- autobuilt 7965716

* Sat Nov 10 2018 Dan Walsh <dwalsh@redhat.com> - 1:0.11.20.11.2-2.dev.git78e6d8e1
- Remove dirty flag from podman version


* Sat Nov 10 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.11.20.11.2-1.dev.git7965716.dev.git78e6d8e1
- bump to 0.11.2
- autobuilt 78e6d8e

* Fri Nov 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.11.20.11.2-1.dev.git7965716.dev.git78e6d8e.dev.gitf5473c61
- bump to 0.11.2
- autobuilt f5473c6

* Thu Nov 08 2018 baude <bbaude@redhat.com> - 1:0.11.1-1.dev.gita4adfe5
- Upstream 0.11.1-1

* Thu Nov 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.10.2-3.dev.git672f572
- autobuilt 672f572

* Wed Nov 07 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 1:0.10.2-2.dev.gite9f8aed
- autobuilt e9f8aed

* Sun Oct 28 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.10.2-1.dev.git4955572
- Resolves: #1643744 - build podman with ostree support
- bump to v0.10.2
- built commit 4955572

* Fri Oct 19 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.10.1.3-3.dev.gitdb08685
- consistent epoch:version-release in changelog

* Thu Oct 18 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.10.1.3-2.dev.gitdb08685
- correct epoch mentions

* Thu Oct 18 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.10.1.3-1.dev.gitdb08685
- bump to v0.10.1.3

* Thu Oct 11 2018 baude <bbaude@redhat.com> - 1:0.10.1-1.gitda5c894
- Upstream v0.10.1 release

* Fri Sep 28 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.9.4-3.dev.gite7e81e6
- built libpod commit e7e81e6
- built conmon from cri-o commit 2cbe48b

* Tue Sep 25 2018 Dan Walsh <dwalsh@redhat.com> - 1:0.9.4-2.dev.gitaf791f3
- Fix required version of runc

* Mon Sep 24 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.9.4-1.dev.gitaf791f3
- bump to v0.9.4
- built af791f3

* Wed Sep 19 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.9.3-2.dev.gitc3a0874
- autobuilt c3a0874

* Mon Sep 17 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.9.3-1.dev.git28a2bf8
- bump to v0.9.3
- built commit 28a2bf82

* Tue Sep 11 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.9.1.1-1.dev.git95dbcad
- bump to v0.9.1.1
- built commit 95dbcad

* Tue Sep 11 2018 baude <bbaude@redhat.com> - 1:0.9.1-1.dev.git123de30
- Upstream release of 0.9.1
- Do not build with devicemapper

* Tue Sep 4 2018 Dan Walsh <dwalsh@redhat.com> - 1:0.8.5-5.git65c31d4
- Fix required version of runc

* Tue Sep 4 2018 Dan Walsh <dwalsh@redhat.com> - 1:0.8.5-4.dev.git65c31d4
- Fix rpm -qi podman to show the correct URL

* Tue Sep 4 2018 Dan Walsh <dwalsh@redhat.com> - 1:0.8.5-3.dev.git65c31d4
- Fix required version of runc

* Mon Sep 3 2018 Dan Walsh <dwalsh@redhat.com> - 1:0.8.5-2.dev.git65c31d4
- Add a specific version of runc or later to require

* Thu Aug 30 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.8.5-1.dev.git65c31d4
- bump to v0.8.5-dev
- built commit 65c31d4
- correct min dep on containernetworking-plugins for upgrade from
containernetworking-cni

* Mon Aug 20 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.8.3-4.dev.git3d55721f
- Resolves: #1619411 - python3-podman should require python3-psutil
- podman-docker should conflict with moby-engine
- require nftables
- recommend slirp4netns and fuse-overlayfs (latter only for kernel >= 4.18)

* Sun Aug 12 2018 Dan Walsh <dwalsh@redhat.com> - 1:0.8.3-3.dev.git3d55721f
- Add podman-docker support
- Force cgroupfs for non root podman

* Sun Aug 12 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.8.3-2.dev.git3d55721f
- Requires: conmon
- use default %%gobuild

* Sat Aug 11 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 1:0.8.3-1.dev.git3d55721f
- bump to v0.8.3-dev
- built commit 3d55721f
- bump Epoch to 1, cause my autobuilder messed up earlier

* Wed Aug 01 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.8.10.8.1-1.dev.git1a439f91
- bump to 0.8.1
- autobuilt 1a439f9

* Tue Jul 31 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.8.10.8.1-1.dev.git1a439f9.dev.git5a4e5901
- bump to 0.8.1
- autobuilt 5a4e590

* Sun Jul 29 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.8.10.8.1-1.dev.git1a439f9.dev.git5a4e590.dev.git433cbd51
- bump to 0.8.1
- autobuilt 433cbd5

* Sat Jul 28 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.8.10.8.1-1.dev.git1a439f9.dev.git5a4e590.dev.git433cbd5.dev.git87d8edb1
- bump to 0.8.1
- autobuilt 87d8edb

* Fri Jul 27 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.7.4-7.dev.git3dd577e
- fix python package version

* Fri Jul 27 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 0.7.4-6.dev.git3dd577e
- Rebuild for new binutils

* Fri Jul 27 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.4-5.dev.git3dd577e
- autobuilt 3dd577e

* Thu Jul 26 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.4-4.dev.git9c806a4
- autobuilt 9c806a4

* Wed Jul 25 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.4-3.dev.gitc90b740
- autobuilt c90b740

* Tue Jul 24 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.7.4-2.dev.git9a18681
- pypodman package exists only if varlink

* Mon Jul 23 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.7.4-1.dev.git9a18681
- bump to v0.7.4-dev
- built commit 9a18681

* Mon Jul 23 2018 Dan Walsh <dwalsh@redhat.com> - 0.7.3-2.dev.git06c546e
- Add Reccommeds container-selinux

* Sun Jul 15 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.7.3-1.dev.git06c546e
- built commit 06c546e

* Sat Jul 14 2018 Dan Walsh <dwalsh@redhat.com> - 0.7.2-10.dev.git86154b6
- Add install of pypodman

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.7.2-9.dev.git86154b6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Thu Jul 12 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.2-8.dev.git86154b6
- autobuilt 86154b6

* Wed Jul 11 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.2-7.dev.git84cfdb2
- autobuilt 84cfdb2

* Tue Jul 10 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.2-6.dev.git4f9b1ae
- autobuilt 4f9b1ae

* Mon Jul 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.2-5.gitc7424b6
- autobuilt c7424b6

* Mon Jul 09 2018 Dan Walsh <dwalsh@redhat.com> - 0.7.2-4.gitf661e1d
- Add ostree support

* Mon Jul 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.2-3.gitf661e1d
- autobuilt f661e1d

* Sun Jul 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.2-2.git0660108
- autobuilt 0660108

* Sat Jul 07 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.2-1.gitca6ffbc
- bump to 0.7.2
- autobuilt ca6ffbc

* Fri Jul 06 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.1-6.git99959e5
- autobuilt 99959e5

* Thu Jul 05 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.1-5.gitf2462ca
- autobuilt f2462ca

* Wed Jul 04 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.1-4.git6d8fac8
- autobuilt 6d8fac8

* Tue Jul 03 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.1-3.git767b3dd
- autobuilt 767b3dd

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 0.7.1-2.gitb96be3a
- Rebuilt for Python 3.7

* Sat Jun 30 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.7.1-1.gitb96be3a
- bump to 0.7.1
- autobuilt b96be3a

* Fri Jun 29 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.5-6.gitd61d8a3
- autobuilt d61d8a3

* Thu Jun 28 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.5-5.gitfd12c89
- autobuilt fd12c89

* Wed Jun 27 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.5-4.git56133f7
- autobuilt 56133f7

* Tue Jun 26 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.5-3.git208b9a6
- autobuilt 208b9a6

* Mon Jun 25 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.5-2.gite89bbd6
- autobuilt e89bbd6

* Sat Jun 23 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.5-1.git7182339
- bump to 0.6.5
- autobuilt 7182339

* Fri Jun 22 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.4-7.git4bd0f22
- autobuilt 4bd0f22

* Thu Jun 21 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.4-6.git6804fde
- autobuilt 6804fde

* Wed Jun 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.4-5.gitf228cf7
- autobuilt f228cf7

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 0.6.4-4.git5645789
- Rebuilt for Python 3.7

* Tue Jun 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.4-3.git5645789
- autobuilt 5645789

* Mon Jun 18 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.4-2.git9e13457
- autobuilt 9e13457

* Sat Jun 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.4-1.gitb43677c
- bump to 0.6.4
- autobuilt b43677c

* Fri Jun 15 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.3-6.git6bdf023
- autobuilt 6bdf023

* Thu Jun 14 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.3-5.git65033b5
- autobuilt 65033b5

* Wed Jun 13 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.3-4.git95ea3d4
- autobuilt 95ea3d4

* Tue Jun 12 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.3-3.gitab72130
- autobuilt ab72130

* Mon Jun 11 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.3-2.git1e9e530
- autobuilt 1e9e530

* Sat Jun 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.3-1.gitb78e7e4
- bump to 0.6.3
- autobuilt b78e7e4

* Fri Jun 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-7.git1cbce85
- autobuilt 1cbce85

* Thu Jun 07 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-6.gitb1ebad9
- autobuilt b1ebad9

* Wed Jun 06 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-5.git7b2b2bc
- autobuilt 7b2b2bc

* Tue Jun 05 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-4.git14cf6d2
- autobuilt 14cf6d2

* Mon Jun 04 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-3.gitcae49fc
- autobuilt cae49fc

* Sun Jun 03 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-2.git13f7450
- autobuilt 13f7450

* Sat Jun 02 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.2-1.git22e6f11
- bump to 0.6.2
- autobuilt 22e6f11

* Fri Jun 01 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.1-4.gita9e9fd4
- autobuilt a9e9fd4

* Thu May 31 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.1-3.gita127b4f
- autobuilt a127b4f

* Wed May 30 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.1-2.git8ee0f2b
- autobuilt 8ee0f2b

* Sat May 26 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.6.1-1.git44d1c1c
- bump to 0.6.1
- autobuilt 44d1c1c

* Fri May 18 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.3-7.gitc54b423
- make python3-podman the same version as the main package
- build python3-podman only for fedora >= 28

* Fri May 18 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.3-6.gitc54b423
- autobuilt c54b423

* Wed May 16 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.3-5.git624660c
- built commit 624660c
- New subapackage: python3-podman

* Wed May 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.3-4.git9fcc475
- autobuilt 9fcc475

* Wed May 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.3-3.git0613844
- autobuilt 0613844

* Tue May 15 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.3-2.git45838b9
- autobuilt 45838b9

* Fri May 11 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.3-1.git07253fc
- bump to v0.5.3
- built commit 07253fc

* Fri May 11 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.2-5.gitcc1bad8
- autobuilt cc1bad8

* Wed May 09 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.2-4.git2526355
- autobuilt 2526355

* Tue May 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.2-3.gitfaa8c3e
- autobuilt faa8c3e

* Sun May 06 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.2-2.gitfa4705c
- autobuilt fa4705c

* Sat May 05 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.2-1.gitbb0e754
- bump to 0.5.2
- autobuilt bb0e754

* Fri May 04 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.1-5.git5ae940a
- autobuilt 5ae940a

* Wed May 02 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.1-4.git64dc803
- autobuilt commit 64dc803

* Wed May 02 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.1-3.git970eaf0
- autobuilt commit 970eaf0

* Tue May 01 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.5.1-2.git7a0a855
- autobuilt commit 7a0a855

* Sun Apr 29 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.5.1-1.giteda0fd7
- reflect version number correctly
- my builder script error ended up picking the wrong version number previously

* Sun Apr 29 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-5.giteda0fd7
- autobuilt commit eda0fd7

* Sat Apr 28 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-4.git6774425
- autobuilt commit 6774425

* Fri Apr 27 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-3.git39a7a77
- autobuilt commit 39a7a77

* Thu Apr 26 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-2.git58cb8f7
- autobuilt commit 58cb8f7

* Wed Apr 25 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de
- bump to 0.4.2
- autobuilt commit bef93de

* Tue Apr 24 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.4.4-1.git398133e
- use correct version number

* Tue Apr 24 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-22.git398133e
- autobuilt commit 398133e

* Sun Apr 22 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-21.gitcf1d884
- autobuilt commit cf1d884

* Fri Apr 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-20.git9b457e3
- autobuilt commit 9b457e3

* Fri Apr 20 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de9.git228732d
- autobuilt commit 228732d

* Thu Apr 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de8.gitf2658ec
- autobuilt commit f2658ec

* Thu Apr 19 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de7.git6a9dbf3
- autobuilt commit 6a9dbf3

* Tue Apr 17 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de6.git96d1162
- autobuilt commit 96d1162

* Tue Apr 17 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de5.git96d1162
- autobuilt commit 96d1162

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de4.git6c5ebb0
- autobuilt commit 6c5ebb0

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de3.gitfa8442e
- autobuilt commit fa8442e

* Mon Apr 16 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de2.gitfa8442e
- autobuilt commit fa8442e

* Sun Apr 15 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de1.gitfa8442e
- autobuilt commit fa8442e

* Sat Apr 14 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-1.gitbef93de0.git62b59df
- autobuilt commit 62b59df

* Fri Apr 13 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-9.git191da31
- autobuilt commit 191da31

* Thu Apr 12 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-8.git6f51a5b
- autobuilt commit 6f51a5b

* Wed Apr 11 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-7.git77a1665
- autobuilt commit 77a1665

* Tue Apr 10 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-6.git864b9c0
- autobuilt commit 864b9c0

* Tue Apr 10 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-5.git864b9c0
- autobuilt commit 864b9c0

* Tue Apr 10 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-4.git998fd2e
- autobuilt commit 998fd2e

* Sun Apr 08 2018 Lokesh Mandvekar (Bot) <lsm5+bot@fedoraproject.org> - 0.4.2-3.git998fd2e
- autobuilt commit 998fd2e

* Sun Apr 08 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.4.2-2.git998fd2e
- autobuilt commit 998fd2e

* Sun Apr 08 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.4.2-1.gitbef93de.git998fd2e
- bump to 0.4.2
- autobuilt commit 998fd2e

* Thu Mar 29 2018 baude <bbaude@redhat.com> - 0.3.5-2.gitdb6bf9e3
- Upstream release 0.3.5

* Tue Mar 27 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.3.5-1.git304bf53
- built commit 304bf53

* Fri Mar 23 2018 baude <bbaude@redhat.com> - 0.3.4-1.git57b403e
- Upstream release 0.3.4

* Fri Mar 16 2018 baude <bbaude@redhat.com> - 0.3.3-2.dev.gitbc358eb
- Upstream release 0.3.3

* Wed Mar 14 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0.3.3-1.dev.gitbc358eb
- built podman commit bc358eb
- built conmon from cri-o commit 712f3b8

* Fri Mar 09 2018 baude <bbaude@redhat.com> - 0.3.2-1.gitf79a39a
- Release 0.3.2-1

* Sun Mar 04 2018 baude <bbaude@redhat.com> - 0.3.1-2.git98b95ff
- Correct RPM version

* Fri Mar 02 2018 baude <bbaude@redhat.com> - 0.3.1-1-gitc187538
- Release 0.3.1-1

* Sun Feb 25 2018 Peter Robinson <pbrobinson@fedoraproject.org> 0.2.2-2.git525e3b1
- Build on ARMv7 too (Fedora supports containers on that arch too)

* Fri Feb 23 2018 baude <bbaude@redhat.com> - 0.2.2-1.git525e3b1
- Release 0.2.2

* Fri Feb 16 2018 baude <bbaude@redhat.com> - 0.2.1-1.git3d0100b
- Release 0.2.1

* Wed Feb 14 2018 baude <bbaude@redhat.com> - 0.2-3.git3d0100b
- Add dep for atomic-registries

* Tue Feb 13 2018 baude <bbaude@redhat.com> - 0.2-2.git3d0100b
- Add more 64bit arches
- Add containernetworking-cni dependancy
- Add iptables dependancy

* Mon Feb 12 2018 baude <bbaude@redhat.com> - 0-2.1.git3d0100
- Release 0.2

* Tue Feb 06 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0-0.3.git367213a
- Resolves: #1541554 - first official build
- built commit 367213a

* Fri Feb 02 2018 Lokesh Mandvekar <lsm5@fedoraproject.org> - 0-0.2.git0387f69
- built commit 0387f69

* Wed Jan 10 2018 Frantisek Kluknavsky <fkluknav@redhat.com> - 0-0.1.gitc1b2278
- First package for Fedora
