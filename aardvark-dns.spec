Summary:	Authoritative dns server for A/AAAA container records
Name:		aardvark-dns
Version:	1.17.0
Release:	1
License:	Apache v2.0
Group:		Applications/System
Source0:	https://github.com/containers/aardvark-dns/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	78c03b4c04c3a1c498de232aa0160c90
Source1:	https://github.com/containers/aardvark-dns/releases/download/v%{version}/%{name}-v%{version}-vendor.tar.gz
# Source1-md5:	3a97cb7f95cd5b494cbd04df1be53331
URL:		https://github.com/containers/aardvark-dns
BuildRequires:	cargo
BuildRequires:	rpmbuild(macros) >= 2.050
BuildRequires:	rust >= 1.86
%{?rust_req}
ExclusiveArch:	%{rust_arches}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Aardvark-dns is an authoritative dns server for A/AAAA container
records. It can forward other requests to configured resolvers.

%prep
%setup -q -a1

# use our offline registry
export CARGO_HOME="$(pwd)/.cargo"

mkdir -p "$CARGO_HOME"
cat >.cargo/config <<EOF
[source.crates-io]
registry = 'https://github.com/rust-lang/crates.io-index'
replace-with = 'vendored-sources'

[source.vendored-sources]
directory = '$PWD/vendor'
EOF

%build
export CARGO_HOME="$(pwd)/.cargo"

%cargo_build

%install
rm -rf $RPM_BUILD_ROOT
export CARGO_HOME="$(pwd)/.cargo"

install -D %cargo_objdir/aardvark-dns $RPM_BUILD_ROOT%{_libexecdir}/podman/aardvark-dns

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md RELEASE_NOTES.md
%attr(755,root,root) %{_libexecdir}/podman/aardvark-dns
