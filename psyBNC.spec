Summary:	Advanced IRC bouncer
Summary(pl):	Zaawansowane narzêdzie do tunelowania irc
Name:		psyBNC
Version:	2.3.1
Release:	1
License:	GPL
Group:		Networking/Utilities
Source0:	http://bluemoon.reverse.net/irc/bouncers/psybnc/%{name}%{version}.tar.gz
# Source0-md5:	d583ed4e3a98f71ac5ae8b5e4caf3424
Patch0:		psybnc-no_ssl.patch
Patch2:		psybnc-menuconf.patch
Patch3:		psybnc-lang-path.patch
URL:		http://www.psychoid.lam3rz.de/
BuildRequires:	ncurses-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Advanced IRC proxy.

%description -l pl
Tunel IRC o wielu mo¿liwo¶ciach.

%prep
%setup -q -n psybnc
%patch0 -p0
%patch2 -p0
%patch3 -p1

%build
%{__make} CC="%{__cc} %{rpmcflags}"
%{__make} CC="%{__cc} %{rpmcflags}" menuconfig

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name}/lang}
install psybnc $RPM_BUILD_ROOT%{_bindir}
install menuconf/menuconf $RPM_BUILD_ROOT%{_bindir}/psyconf
install lang/*.lng $RPM_BUILD_ROOT%{_datadir}/%{name}/lang/
mv psybnc.conf psybnc.conf.example

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README CHANGES psybncchk psybnc.conf.example
%attr(755,root,root) %{_bindir}/*
%{_datadir}/%{name}/*
