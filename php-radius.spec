%define modname radius
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A13_%{modname}.ini

Summary:	Radius client library for PHP
Name:		php-%{modname}
Version:	1.2.4
Release:	%mkrel 10
Group:		Development/PHP
License:	BSD
URL:		http://pecl.php.net/package/radius
Source0:	%{modname}-%{version}.tar.bz2
Source1:	%{modname}.ini.bz2
BuildRequires:	php-devel >= 3:5.2.0
Provides:	php5-radius
Obsoletes:	php5-radius
Epoch:		1
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
This package is based on the libradius of FreeBSD, with some modifications and
extensions. This PECL provides full support for RADIUS authentication (RFC
2865) and RADIUS accounting (RFC 2866), works on Unix and on Windows. Its an
easy way to authenticate your users against the user-database of your OS (for
example against Windows Active-Directory via IAS). 

%prep

%setup -q -n %{modname}-%{version}

%build

phpize
%configure2_5x --with-libdir=%{_lib} \
    --with-%{modname}=shared,%{_prefix}

%make
mv modules/*.so .

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_libdir}/php/extensions
install -d %{buildroot}%{_sysconfdir}/php.d

cat > README.%{modname} << EOF
The %{name} package contains a dynamic shared object (DSO) for PHP. 
EOF

bzcat %{SOURCE1} > %{buildroot}%{_sysconfdir}/php.d/%{inifile}
install -m755 %{soname} %{buildroot}%{_libdir}/php/extensions/

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc examples CREDITS radius.conf README*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


