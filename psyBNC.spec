%define		_mainver	2.3.2
%define		_subver		.7
%define		_distver	%(echo %{_subver} |tr . -)
Summary:	Advanced IRC bouncer
Summary(pl):	Zaawansowane narzêdzie do tunelowania IRC
Name:		psyBNC
Version:	%{_mainver}%{_subver}
Release:	1
License:	GPL
Group:		Networking/Utilities
#Source0:	http://www.psychoid.lam3rz.de/%{name}%{version}.tar.gz
Source0:	http://www.psybnc.at/download/beta/%{name}-%{_mainver}%{_distver}.tar.gz
# Source0-md5:	c475f14b1b3a9280a123142e6e344dd8
Patch0:		psybnc-sslkey.patch
Patch1:		psybnc-menuconf.patch
Patch2:		psybnc-lang-path.patch
Patch3:		psybnc-menuconf-runtime.patch
Patch4:		psybnc-helppath.patch
URL:		http://www.psybnc.at/
BuildRequires:	ncurses-devel
BuildRequires:	openssl-tools
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# psyconf reads the documentation files
%define	_noautocompressdoc	README FAQ CHANGES

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
%patch1 -p0
%patch2 -p1
#%patch3 -p1
%patch4 -p1
echo "#define OIDENTD" >> config.h

%build
# TODO:
# - BIGENDIAN detection is just opposite - is usage the same?
# - IPV6 detection relies on IPv6 socket support on builder

%{__make} menuconfig \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

yes '' | %{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/%{name}/{lang,{menu,}help},/etc/certs}

install psybnc $RPM_BUILD_ROOT%{_bindir}
install menuconf/menuconf $RPM_BUILD_ROOT%{_bindir}/psyconf
install menuconf/help/*.txt $RPM_BUILD_ROOT%{_datadir}/%{name}/menuhelp
install help/*.* $RPM_BUILD_ROOT%{_datadir}/%{name}/help
install lang/*.lng $RPM_BUILD_ROOT%{_datadir}/%{name}/lang
install key/psybnc.{cert,key}.pem $RPM_BUILD_ROOT/etc/certs
install psybnc.conf psybnc.conf.example
ln -s %{_docdir}/%{name}-%{version} $RPM_BUILD_ROOT%{_datadir}/%{name}/doc

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%groupadd -g 143 psybnc

%postun
if [ "$1" = "0" ]; then
	%groupremove bnc
fi

%files
%defattr(644,root,root,755)
%doc README CHANGES FAQ TODO SCRIPTING psybncchk psybnc.conf.example scripts/example/DEFAULT.SCRIPT
%config(noreplace) %verify(not md5 mtime size) %attr(644,root,psybnc) /etc/certs/psybnc.cert.pem
%config(noreplace) %verify(not md5 mtime size) %attr(640,root,psybnc) /etc/certs/psybnc.key.pem

%attr(755,root,root) %{_bindir}/*
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/lang
%{_datadir}/%{name}/lang/english.lng
%lang(de) %{_datadir}/%{name}/lang/german.lng
%lang(it) %{_datadir}/%{name}/lang/italiano.lng
%{_datadir}/%{name}/menuhelp
%{_datadir}/%{name}/help
%{_datadir}/%{name}/doc
