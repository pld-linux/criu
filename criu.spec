Summary:	checkpoint/restore functionality for Linux in userspace
Name:		criu
Version:	1.3.1
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	http://download.openvz.org/criu/%{name}-%{version}.tar.bz2
# Source0-md5:	72331377375c136abbfebcfa3f5d3f90
URL:		http://criu.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	protobuf-c-devel
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	sed >= 4.0
Requires:	%{name}-libs = %{version}-%{release}
Requires:	iproute2 >= 3.6
Requires:	uname(release) >= 3.9
Requires(post,preun,postun):	systemd-units >= 38
Requires:	systemd-units >= 38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

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

%package libs
Summary:	CRIU shared library
Summary(pl.UTF-8):	Biblioteka współdzielona CRIU
Group:		Libraries

%description libs
CRIU shared library.

%description libs -l pl.UTF-8
Biblioteka współdzielona CRIU.

%package devel
Summary:	Header file for CRIU library
Summary(pl.UTF-8):	Plik nagłówkowy biblioteki CRIU
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header file for CRIU library.

%description devel -l pl.UTF-8
Plik nagłówkowy biblioteki CRIU.

%prep
%setup -q
sed -i -e 's#-O2#$(OPT)#g' Makefile*

%build
%{__make} \
	CC="%{__cc}" \
	OPT="%{rpmcppflags} %{rpmcflags}" \
	PREFIX=%{_prefix} \
	LOGROTATEDIR=%{_sysconfdir}/logrotate.d \
	SYSTEMDUNITDIR=%{systemdunitdir} \
	V=1 \
	WERROR=0

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	PREFIX="%{_prefix}" \
	LOGROTATEDIR=%{_sysconfdir}/logrotate.d \
	SYSTEMDUNITDIR=%{systemdunitdir} \
	MANDIR=%{_mandir} \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post
%systemd_post criu.service

%preun
%systemd_preun criu.service

%postun
%systemd_reload

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CREDITS README
%attr(755,root,root) %{_sbindir}/criu
%{_mandir}/man8/criu.8*
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/logrotate.d/criu-service
%{systemdunitdir}/criu.service
%{systemdunitdir}/criu.socket

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcriu.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libcriu.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcriu.so
%{_includedir}/criu
%{_pkgconfigdir}/criu.pc
