Summary:	Checkpoint/restore functionality for Linux in userspace
Summary(pl.UTF-8):	Funkcja checkpoint/restore w przestrzeni użytkownika dla Linuksa
Name:		criu
Version:	2.5
Release:	1
License:	GPL v2 (tools), LGPL v2.1 (library)
Group:		Applications/System
Source0:	http://download.openvz.org/criu/%{name}-%{version}.tar.bz2
# Source0-md5:	5d5115454d110adb744e885d82d2c1f6
Patch0:		%{name}-python.patch
URL:		http://criu.org/
BuildRequires:	asciidoc
BuildRequires:	libcap-devel
BuildRequires:	libnl-devel >= 1:3.2
BuildRequires:	pkgconfig
BuildRequires:	protobuf
BuildRequires:	protobuf-c-devel
BuildRequires:	protobuf-devel
BuildRequires:	python >= 2
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.697
BuildRequires:	sed >= 4.0
Requires:	%{name}-libs = %{version}-%{release}
Requires:	iproute2 >= 3.5
Requires:	uname(release) >= 3.11
ExclusiveArch:	%{x8664} %{arm} aarch64 ppc64
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_libexecdir	%{_prefix}/lib

%description
Checkpoint/Restore In Userspace, or CRIU, is a software tool for Linux
operating system. Using this tool, you can freeze a running
application (or part of it) and checkpoint it to a hard drive as a
collection of files. You can then use the files to restore and run the
application from the point it was frozen at. The distinctive feature
of the CRIU project is that it is mainly implemented in user space.

%description -l en.UTF-8
Checkpoint/Restore In Userspace, or CRIU (pronounced kree-oo, IPA:
/krɪʊ/, Russian: криу), is a software tool for Linux operating system.
Using this tool, you can freeze a running application (or part of it)
and checkpoint it to a hard drive as a collection of files. You can
then use the files to restore and run the application from the point
it was frozen at. The distinctive feature of the CRIU project is that
it is mainly implemented in user space.

%description -l pl.UTF-8
CRIU (Checkpoint/Restore In Userspace) to narzędzie programowe dla
systemu operacyjnego Linux. Przy jego użyciu można zamrozić działającą
aplikację (lub jej część) i zapisać migawkę na twardym dysku jako
zestaw plików. Następnie można użyć tych plików do odtworzenia i
uruchomienia aplikacji od miejsca, w którym została zamrożona.
Wyróżnikiem projektu CRIU jest to, że został zaimplementowany głównie
w przestrzeni użytkownika.

%package libs
Summary:	CRIU shared library
Summary(pl.UTF-8):	Biblioteka współdzielona CRIU
License:	LGPL v2.1
Group:		Libraries

%description libs
CRIU shared library.

%description libs -l pl.UTF-8
Biblioteka współdzielona CRIU.

%package devel
Summary:	Header files for CRIU library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki CRIU
License:	LGPL v2.1
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for CRIU library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki CRIU.

%package -n python-pycriu
Summary:	Python interface to CRIU
Summary(pl.UTF-8):	Pythonowy interfejs do CRIU
Group:		Libraries/Python
Requires:	%{name}-libs = %{version}-%{release}

%description -n python-pycriu
Python interface to CRIU. This package contains also crit utility.

%description -n python-pycriu -l pl.UTF-8
Pythonowy interfejs do CRIU. Ten pakiet zawiera także narzędzie crit.

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e 's#-O2 -g#$(OPT)#g' Makefile

%build
%define _make_opts \\\
	DEB_HOST_MULTIARCH= \\\
	CC="%{__cc}" \\\
	OPT="%{rpmcppflags} %{rpmcflags}" \\\
	PREFIX=%{_prefix} \\\
	LIBDIR=%{_libdir} \\\
	LOGROTATEDIR=%{_sysconfdir}/logrotate.d \\\
	LIBEXECDIR=%{_libexecdir} \\\
	PYSITESCRIPTDIR=%{py_sitescriptdir} \\\
	MANDIR=%{_mandir} \\\
	WERROR=0 \\\
	V=1
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# optional script, do not autogenerate bash dep
chmod -x $RPM_BUILD_ROOT%{_libexecdir}/%{name}/scripts/systemd-autofs-restart.sh

%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CREDITS README.md contrib
%attr(755,root,root) %{_sbindir}/criu
%{_mandir}/man8/criu.8*
%dir %{_libexecdir}/%{name}
%dir %{_libexecdir}/%{name}/scripts
%{_libexecdir}/%{name}/scripts/systemd-autofs-restart.sh

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcriu.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libcriu.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcriu.so
%{_includedir}/criu
%{_pkgconfigdir}/criu.pc

%files -n python-pycriu
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/crit
%{py_sitescriptdir}/pycriu
%{py_sitescriptdir}/crit-0.0.1-py*.egg-info
