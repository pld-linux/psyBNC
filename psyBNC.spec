Summary:	Advanced IRC bouncer
Summary(pl):	Zaawansowane narzêdzie do tunelowania IRC
Name:		psyBNC
Version:	2.3.2.4
Release:	1
License:	GPL
Group:		Networking/Utilities
#Source0:	http://www.psychoid.lam3rz.de/%{name}%{version}.tar.gz
Source0:	http://www.psybnc.info/download/%{name}2.3.2-4.tar.gz
# Source0-md5:	f752aec57da0d08ee183b22f79b6b34f
Patch0:		psybnc-sslkey.patch
Patch1:		psybnc-gcc34.patch
Patch2:		psybnc-menuconf.patch
Patch3:		psybnc-lang-path.patch
URL:		http://www.psychoid.lam3rz.de/psybnc.html
BuildRequires:	ncurses-devel
BuildRequires:	openssl-tools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
psyBNC is an easy-to-use, multi-user, permanent IRC-Bouncer with many
features. Some of its features include symmetric ciphering of talk and
connections (Blowfish and IDEA), the possibility of linking multiple
bouncers to an internal network including a shared partyline, vhost-
and relay support to connected bouncers and an extensive online help
system. Many other helpful functions are included.

%description -l pl
psyBNC to ³atwe do u¿ycie, wielou¿ytkownikowe, sta³e ircowe proxy z
wieloma bajerami. Po¶ród nich: symetryczne szyfrowanie rozmów i
po³±czeñ (Blowfish i IDEA), mo¿liwo¶æ ³±czenia wielu proxy w
wewnêtrzn± sieæ, razem z wspó³dzielonym kana³em rozmów, wsparcie
vhostów i retransmisji do po³±czonych proxy, a tak¿e rozbudowany
system wbudowanej pomocy.

%prep
%setup -q -n psybnc
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p1

%build
# TODO:
# - BIGENDIAN detection is just opposite - is usage the same?
# - IPV6 detection relies on IPv6 socket support on builder

%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" << EOF






EOF

%{__make} menuconfig \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name}/{lang,key}}

install psybnc $RPM_BUILD_ROOT%{_bindir}
install menuconf/menuconf $RPM_BUILD_ROOT%{_bindir}/psyconf
install lang/*.lng $RPM_BUILD_ROOT%{_datadir}/%{name}/lang
install key/psybnc.{cert,key}.pem $RPM_BUILD_ROOT%{_datadir}/%{name}/key
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
%{_datadir}/%{name}/key
