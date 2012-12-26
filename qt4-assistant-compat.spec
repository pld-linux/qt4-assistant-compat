#
# Conditional build:
%bcond_without	static_libs	# don't build static libraries
#
Summary:	Qt Assistant compatibility binary (legacy)
Summary(pl.UTF-8):	Program Qt Assistant (stara wersja)
Name:		qt4-assistant-compat
Version:	4.6.3
Release:	2
License:	LGPL v2.1 with Nokia Qt exception or GPL v3
Group:		X11/Development/Tools
Source0:	ftp://ftp.qt.nokia.com/qt/source/qt-assistant-qassistantclient-library-compat-src-%{version}.tar.gz
# Source0-md5:	a20148e0488d5c12ab35ccc107dcc64d
Source1:	QAssistantClient
Source2:	QtAssistant
Patch0:		%{name}-build-system.patch
URL:		http://qt.nokia.com/
BuildRequires:	QtCore-devel >= 4.7
BuildRequires:	QtGui-devel >= 4.7
BuildRequires:	QtNetwork-devel >= 4.7
BuildRequires:	qt4-linguist >= 4.7
BuildRequires:	qt4-qmake >= 4.7
BuildRequires:	sed >= 4.0
Obsoletes:	qt-assistant < %{version}-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_qtdir		%{_libdir}/qt4

%description
Qt is a complete C++ application development framework, which includes
a class library and tools for multiplatform development and
internationalization. Using Qt, a single source code tree can build
applications that run natively on different platforms (Windows,
Unix/Linux, Mac OS X, embedded Linux).

This package contains the Qt Assistant compatibility version, based on
Assistant Document Profile (.adp) files, and the associated
QtAssistantClient library, for compatibility with applications
providing help in that format.

New applications should use the new version of Qt Assistant introduced
in Qt 4.4, based on the Qt Help Framework also introduced in Qt 4.4,
instead.

%description -l pl.UTF-8
Qt oferuje kompletny system do tworzenia i rozwijania aplikacji w
języku C++, w którego skład wchodzi biblioteka z klasami oraz
wieloplatformowymi narzędziami do rozwijania i tłumaczenia aplikacji.
Z pomocą Qt jeden kod źródłowy może być natywnie uruchamiany na
różnych platformach (Windows, Unix/Linux, Mac OS X).

Ten pakiet zawiera starą wersję programu Qt Assistant, opartą na
plikach .adp (Assistant Document Profile) oraz powiązanej bibliotece
QtAssistantClient, służącą kompatybilności z aplikacjami
udostępniającymi pomoc w tym formacie.

Nowe aplikacje powinny używać nowej wersji programu Qt Assistant
wprowadzonej w Qt 4.4, opartej na szkielecie Qt Help, wprowadzonym
także w Qt 4.4.

%package -n QtAssistant-compat
Summary:	Qt AssistantClient compatibility library
Summary(pl.UTF-8):	Biblioteka kompatybilności Qt AssistantClient
Group:		X11/Libraries
Requires:	QtCore >= 4.7
Requires:	QtGui >= 4.7
Requires:	QtNetwork >= 4.7
#Provides:	QtAssistant = %{version}-2
Obsoletes:	QtAssistant < %{version}-2

%description -n QtAssistant-compat
Qt is a complete C++ application development framework, which includes
a class library and tools for multiplatform development and
internationalization. Using Qt, a single source code tree can build
applications that run natively on different platforms (Windows,
Unix/Linux, Mac OS X, embedded Linux).

This package contains the files necessary to run applications using
the deprecated QAssistantClient class, which is used together with the
legacy Assistant Document Profile (.adp) version of Qt Assistant.

This library is obsolete. It is provided to keep old source code
working. It is strongly advised against using it in new code. New code
should use the Qt Help Framework introduced in Qt 4.4 and/or the
version of Qt Assistant based on it (also introduced in Qt 4.4)
instead.

%description -n QtAssistant-compat -l pl.UTF-8
Qt oferuje kompletny system do tworzenia i rozwijania aplikacji w
języku C++, w którego skład wchodzi biblioteka z klasami oraz
wieloplatformowymi narzędziami do rozwijania i tłumaczenia aplikacji.
Z pomocą Qt jeden kod źródłowy może być natywnie uruchamiany na
różnych platformach (Windows, Unix/Linux, Mac OS X).

Ten pakiet zawiera pliki potrzebne do uruchamiania aplikacji
wykorzystujących przestarzałą klasę QAssistantClient, która jest
używana wraz ze starą wersją programu Qt Assistant, opartą na plikach
.adp (Assistant Document Profile).

Ta biblioteka jest przestarzała. Jest dostarczana tylko w celu
zachowania działania starego kodu, nie powinna być używana w nowym
kodzie. Nowe programy powinny wykorzystywać szkielet Qt Help
wprowadzony w Qt 4.4 oraz opartą na nim wersję programu Qt Assistant
(także wprowadzoną w Qt 4.4).

%package -n QtAssistant-compat-devel
Summary:	Qt AssistantClient compatibility library - development files
Summary(pl.UTF-8):	Biblioteka kompatybilności Qt AssistantClient - pliki programistyczne
Group:		X11/Development/Libraries
Requires:	QtAssistant-compat = %{version}-%{release}
Requires:	QtCore-devel >= 4.7
Requires:	QtGui-devel >= 4.7
Requires:	QtNetwork-devel >= 4.7
#Provides:	QtAssistant-devel = %{version}-2
Obsoletes:	QtAssistant-devel < %{version}-2

%description -n QtAssistant-compat-devel
Qt AssistantClient compatibility library - development files.

%description -n QtAssistant-compat-devel -l pl.UTF-8
Biblioteka kompatybilności Qt AssistantClient - pliki programistyczne.

%prep
%setup -q -n qt-assistant-qassistantclient-library-compat-version-%{version}
%patch0 -p1

%build
cd lib
qmake-qt4 \
	CONFIG+=create_prl \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcxxflags}" \
	QMAKE_LFLAGS_RELEASE="%{rpmldflags}"
%{__make}
cd ..
qmake-qt4
%{__make}
cd translations
lrelease-qt4 *.ts

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/qt4/mkspecs/features,%{_includedir}/qt4/Qt}

%{__make} -C lib install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

%{__make} install \
	INSTALL_ROOT=$RPM_BUILD_ROOT

cp -p features/assistant.prf $RPM_BUILD_ROOT%{_datadir}/qt4/mkspecs/features
cp -p %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{_includedir}/qt4/QtAssistant

# kill builddir
%{__sed} -i -e "s,$PWD/lib,%{_libdir}," $RPM_BUILD_ROOT%{_libdir}/lib*.prl

ln -sf ../%{_lib}/qt4/bin/assistant_adp $RPM_BUILD_ROOT%{_bindir}/assistant_adp

for file in translations/*.qm ; do
	[ ! -f $file ] && continue
	eval "`echo $file | sed -r 's:.*/([a-zA-Z]+(_[a-zA-Z]{3,})?)_(([a-z]{2}_[A-Z]{2})|([a-z]{2}))\.qm$:MOD=\1 ; lang=\3:'`"
	MOD=qt4-$MOD
	install	-d $RPM_BUILD_ROOT%{_localedir}/$lang/LC_MESSAGES
	cp $file $RPM_BUILD_ROOT%{_localedir}/$lang/LC_MESSAGES/$MOD.qm
done

cd $RPM_BUILD_ROOT%{_includedir}/qt4/Qt
ln -sf ../QtAssistant/* .
cd -

%clean
rm -rf $RPM_BUILD_ROOT

%post	-n QtAssistant-compat -p /sbin/ldconfig
%postun	-n QtAssistant-compat -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/assistant_adp
%attr(755,root,root) %{_qtdir}/bin/assistant_adp
%lang(de) %{_localedir}/de/LC_MESSAGES/qt4-assistant_adp.qm
%lang(ja) %{_localedir}/ja/LC_MESSAGES/qt4-assistant_adp.qm
%lang(pl) %{_localedir}/pl/LC_MESSAGES/qt4-assistant_adp.qm
%lang(ru) %{_localedir}/ru/LC_MESSAGES/qt4-assistant_adp.qm
%lang(zh_CN) %{_localedir}/zh_CN/LC_MESSAGES/qt4-assistant_adp.qm
%lang(zh_TW) %{_localedir}/zh_TW/LC_MESSAGES/qt4-assistant_adp.qm

%files -n QtAssistant-compat
%defattr(644,root,root,755)
%doc LGPL_EXCEPTION.txt
%attr(755,root,root) %{_libdir}/libQtAssistantClient.so.*.*
%attr(755,root,root) %ghost %{_libdir}/libQtAssistantClient.so.4

%files -n QtAssistant-compat-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libQtAssistantClient.so
%{_libdir}/libQtAssistantClient.prl
%{_includedir}/qt4/QtAssistant
%{_includedir}/qt4/Qt/QAssistantClient
%{_includedir}/qt4/Qt/QtAssistant
%{_includedir}/qt4/Qt/qassistantclient.h
%{_includedir}/qt4/Qt/qassistantclient_global.h
%{_pkgconfigdir}/QtAssistantClient.pc
%{_datadir}/qt4/mkspecs/features/assistant.prf
