Summary:	Advanced IRC bouncer
Summary(pl):	Zaawansowane narz�dzie do tunelowania IRC
Name:		psyBNC
Version:	2.3.2.4
Release:	1.20
License:	GPL
Group:		Networking/Utilities
#Source0:	http://www.psychoid.lam3rz.de/%{name}%{version}.tar.gz
Source0:	http://www.psybnc.info/download/%{name}2.3.2-4.tar.gz
# Source0-md5:	f752aec57da0d08ee183b22f79b6b34f
Patch0:		psybnc-sslkey.patch
Patch1:		psybnc-gcc34.patch
Patch2:		psybnc-menuconf.patch
Patch3:		psybnc-lang-path.patch
Patch4:		psybnc-menuconf-runtime.patch
Patch5:		psybnc-helppath.patch
URL:		http://www.psychoid.lam3rz.de/psybnc.html
BuildRequires:	ncurses-devel
BuildRequires:	openssl-tools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_sysconfdir /etc/%{name}

# psyconf reads the documentation files
%define	_noautocompressdoc	README FAQ CHANGES

%define	groupid	143

%description
psyBNC is an easy-to-use, multi-user, permanent IRC-Bouncer with many
features. Some of its features include symmetric ciphering of talk and
connections (Blowfish and IDEA), the possibility of linking multiple
bouncers to an internal network including a shared partyline, vhost-
and relay support to connected bouncers and an extensive online help
system. Many other helpful functions are included.

%description -l pl
psyBNC to �atwe do u�ycie, wielou�ytkownikowe, sta�e ircowe proxy z
wieloma bajerami. Po�r�d nich: symetryczne szyfrowanie rozm�w i
po��cze� (Blowfish i IDEA), mo�liwo�� ��czenia wielu proxy w
wewn�trzn� sie�, razem z wsp�dzielonym kana�em rozm�w, wsparcie
vhost�w i retransmisji do po��czonych proxy, a tak�e rozbudowany
system wbudowanej pomocy.

%prep
%setup -q -n psybnc
%patch0 -p1
%patch1 -p1
%patch2 -p0
%patch3 -p1
%patch4 -p1
%patch5 -p1

%build
# TODO:
# - BIGENDIAN detection is just opposite - is usage the same?
# - IPV6 detection relies on IPv6 socket support on builder

yes '' | %{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%{__make} menuconfig \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name}/{lang,{menu,}help},%{_sysconfdir}}

install psybnc $RPM_BUILD_ROOT%{_bindir}
install menuconf/menuconf $RPM_BUILD_ROOT%{_bindir}/psyconf
install menuconf/help/*.txt $RPM_BUILD_ROOT%{_datadir}/%{name}/menuhelp
install help/*.* $RPM_BUILD_ROOT%{_datadir}/%{name}/help
install lang/*.lng $RPM_BUILD_ROOT%{_datadir}/%{name}/lang
install key/psybnc.{cert,key}.pem $RPM_BUILD_ROOT%{_sysconfdir}
install psybnc.conf psybnc.conf.example
ln -s %{_docdir}/%{name}-%{version} $RPM_BUILD_ROOT%{_datadir}/%{name}/doc

%clean
rm -rf $RPM_BUILD_ROOT

%pre
if [ -n "`/usr/bin/getgid psybnc`" ]; then
	if [ "`/usr/bin/getgid psybnc`" != %{groupid} ]; then
		echo "Error: group psybnc doesn't have gid=%{groupid}. Correct this before installing %{name}." 1>&2
		exit 1
	fi
else
	/usr/sbin/groupadd -g %{groupid} psybnc
fi

%postun
if [ "$1" = "0" ]; then
	%groupremove bnc
fi

%files
%defattr(644,root,root,755)
%doc README CHANGES FAQ TODO SCRIPTING psybncchk psybnc.conf.example scripts/example/DEFAULT.SCRIPT
%dir %attr(750,root,psybnc) %{_sysconfdir}
%config(noreplace) %verify(not size mtime md5) %attr(644,root,psybnc) %{_sysconfdir}/psybnc.cert.pem
%config(noreplace) %verify(not size mtime md5) %attr(640,root,psybnc) %{_sysconfdir}/psybnc.key.pem

%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/lang
%{_datadir}/%{name}/lang/english.lng
%lang(de) %{_datadir}/%{name}/lang/german.lng
%lang(it) %{_datadir}/%{name}/lang/italiano.lng
%{_datadir}/%{name}/menuhelp
%{_datadir}/%{name}/help
%{_datadir}/%{name}/doc
