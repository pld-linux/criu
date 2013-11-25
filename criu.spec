Summary:	checkpoint/restore functionality for Linux in userspace
Name:		criu
Version:	1.0
Release:	1
License:	GPL v2
Group:		Applications/System
Source0:	http://download.openvz.org/criu/%{name}-%{version}.tar.bz2
# Source0-md5:	67c4ca5ca36a3514f247e86743c9ceee
URL:		http://criu.org/
BuildRequires:	autoconf >= 2.50
BuildRequires:	protobuf-c-devel
BuildRequires:	rpmbuild(macros) >= 1.228
BuildRequires:	sed >= 4.0
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

%prep
%setup -q
sed -i -e 's#-O2#$(OPT)#g' Makefile*

%build
%{__make} \
	CC="%{__cc}" \
	OPT="%{rpmcppflags} %{rpmcflags}" \
	V=1 \
	WERROR=0

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	SBINDIR=/sbin \
	MANDIR=%{_mandir} \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CREDITS README
%attr(755,root,root) /sbin/criu
%{_mandir}/man8/criu.8*
