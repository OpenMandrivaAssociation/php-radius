%define modname radius
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A13_%{modname}.ini

Summary:	Radius client library for PHP
Name:		php-%{modname}
Version:	1.2.5
Release:	%mkrel 26
Group:		Development/PHP
License:	BSD
URL:		http://pecl.php.net/package/radius
Source0:	%{modname}-%{version}.tar.bz2
Source1:	%{modname}.ini
BuildRequires:	php-devel >= 3:5.2.0
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This package is based on the libradius of FreeBSD, with some modifications and
extensions. This PECL provides full support for RADIUS authentication (RFC
2865) and RADIUS accounting (RFC 2866), works on Unix and on Windows. Its an
easy way to authenticate your users against the user-database of your OS (for
example against Windows Active-Directory via IAS). 

%prep

%setup -q -n %{modname}-%{version}

cp %{SOURCE1} %{inifile}

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

install -m0644 %{inifile} %{buildroot}%{_sysconfdir}/php.d/%{inifile}
install -m0755 %{soname} %{buildroot}%{_libdir}/php/extensions/

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc examples CREDITS radius.conf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}
