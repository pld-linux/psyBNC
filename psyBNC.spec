Summary:	Advanced IRC bouncer
Summary(pl):	Zaawansowane narzêdzie do tunelowania IRC
Name:		psyBNC
Version:	2.3.1
Release:	4
License:	GPL
Group:		Networking/Utilities
Source0:	http://www.psychoid.lam3rz.de/%{name}%{version}.tar.gz
# Source0-md5:	fd519cc66b305e0bceacc03e7c4d2159
Patch0:		psybnc-no_ssl.patch
Patch2:		psybnc-menuconf.patch
Patch3:		psybnc-lang-path.patch
URL:		http://www.psychoid.lam3rz.de/psybnc.html
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
# TODO:
# - BIGENDIAN detection is just opposite - is usage the same?
# - IPV6 detection relies on IPv6 socket support on builder

%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%{__make} menuconfig \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name}/lang}

install psybnc $RPM_BUILD_ROOT%{_bindir}
install menuconf/menuconf $RPM_BUILD_ROOT%{_bindir}/psyconf
install lang/*.lng $RPM_BUILD_ROOT%{_datadir}/%{name}/lang
mv psybnc.conf psybnc.conf.example

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README CHANGES psybncchk psybnc.conf.example
%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/lang
%{_datadir}/%{name}/lang/english.lng
%lang(de) %{_datadir}/%{name}/lang/german.lng
%lang(it) %{_datadir}/%{name}/lang/italiano.lng
