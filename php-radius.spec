%define modname radius
%define dirname %{modname}
%define soname %{modname}.so
%define inifile A13_%{modname}.ini

Summary:	Radius client library for PHP
Name:		php-%{modname}
Version:	1.2.5
Release:	28
Group:		Development/PHP
License:	BSD
URL:		http://pecl.php.net/package/radius
Source0:	%{modname}-%{version}.tar.bz2
Source1:	%{modname}.ini
Patch0:		radius-1.2.5-php54x.diff
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
%patch0 -p0

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


%changelog
* Sun May 06 2012 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-27mdv2012.0
+ Revision: 797035
- fix build
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-26
+ Revision: 761282
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-25
+ Revision: 696459
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-24
+ Revision: 695454
- rebuilt for php-5.3.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-23
+ Revision: 646675
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-22mdv2011.0
+ Revision: 629855
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-21mdv2011.0
+ Revision: 628176
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-20mdv2011.0
+ Revision: 600522
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-19mdv2011.0
+ Revision: 588859
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-18mdv2010.1
+ Revision: 514645
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-17mdv2010.1
+ Revision: 485423
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-16mdv2010.1
+ Revision: 468243
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-15mdv2010.0
+ Revision: 451350
- rebuild

* Sun Jul 19 2009 Raphaël Gertz <rapsys@mandriva.org> 1:1.2.5-14mdv2010.0
+ Revision: 397585
- Rebuild

* Wed Jul 08 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-13mdv2010.0
+ Revision: 393458
- rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-12mdv2010.0
+ Revision: 377020
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-11mdv2009.1
+ Revision: 346599
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-10mdv2009.1
+ Revision: 341790
- rebuilt against php-5.2.9RC2

* Thu Jan 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-9mdv2009.1
+ Revision: 323044
- rebuild

* Fri Dec 05 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-8mdv2009.1
+ Revision: 310299
- rebuilt against php-5.2.7

* Fri Jul 18 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-7mdv2009.0
+ Revision: 238423
- rebuild

* Fri May 02 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-6mdv2009.0
+ Revision: 200261
- rebuilt for php-5.2.6

* Mon Feb 04 2008 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-5mdv2008.1
+ Revision: 162148
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sun Nov 11 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-4mdv2008.1
+ Revision: 107711
- restart apache if needed

* Sat Sep 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-3mdv2008.0
+ Revision: 77569
- rebuilt against php-5.2.4

* Thu Jun 14 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-2mdv2008.0
+ Revision: 39517
- use distro conditional -fstack-protector

* Thu Jun 07 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.5-1mdv2008.0
+ Revision: 36538
- fix build
- 1.2.5

* Fri Jun 01 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.4-10mdv2008.0
+ Revision: 33870
- rebuilt against new upstream version (5.2.3)

* Thu May 03 2007 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.4-9mdv2008.0
+ Revision: 21350
- rebuilt against new upstream version (5.2.2)


* Thu Feb 08 2007 Oden Eriksson <oeriksson@mandriva.com> 1.2.4-8mdv2007.0
+ Revision: 117608
- rebuilt against new upstream version (5.2.1)

* Wed Nov 08 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.4-7mdv2007.0
+ Revision: 78098
- rebuilt for php-5.2.0
- Import php-radius

* Mon Aug 28 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.4-6
- rebuilt for php-5.1.6

* Thu Jul 27 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.4-5mdk
- rebuild

* Sat May 06 2006 Oden Eriksson <oeriksson@mandriva.com> 1.2.4-4mdk
- rebuilt for php-5.1.3

* Sun Jan 15 2006 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.4-3mdk
- rebuilt against php-5.1.2

* Wed Nov 30 2005 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.4-2mdk
- rebuilt against php-5.1.1

* Sat Nov 26 2005 Oden Eriksson <oeriksson@mandriva.com> 1:1.2.4-1mdk
- rebuilt against php-5.1.0
- fix versioning

* Sun Oct 02 2005 Oden Eriksson <oeriksson@mandriva.com> 5.1.0_1.2.4-0.RC1.1mdk
- rebuilt against php-5.1.0RC1

* Wed Sep 07 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.5_1.2.4-1mdk
- rebuilt against php-5.0.5 (Major security fixes)

* Fri May 27 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4_1.2.4-1mdk
- rename the package

* Sun Apr 17 2005 Oden Eriksson <oeriksson@mandriva.com> 5.0.4_1.2.4-1mdk
- 5.0.4

* Sun Mar 20 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_1.2.4-2mdk
- use the %%mkrel macro

* Sat Feb 12 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 5.0.3_1.2.4-1mdk
- initial Mandrakelinux package

* Sat Feb 12 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_1.2.4-3mdk
- rebuilt against a non hardened-php aware php lib

* Sat Jan 15 2005 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_1.2.4-2mdk
- rebuild due to hardened-php-0.2.6
- cleanups

* Thu Dec 16 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.10_1.2.4-1mdk
- rebuild for php 4.3.10

* Sat Oct 02 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.9_1.2.4-1mdk
- rebuild for php 4.3.9

* Thu Jul 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.8_1.2.4-1mdk
- rebuilt for php-4.3.8

* Tue Jul 13 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7_1.2.4-2mdk
- remove redundant provides

* Tue Jun 15 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.7_1.2.4-1mdk
- rebuilt for php-4.3.7

* Mon May 24 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6_1.2.4-2mdk
- use the %%configure2_5x macro
- move scandir to /etc/php.d

* Thu May 06 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 4.3.6_1.2.4-1mdk
- fix url
- built for php 4.3.6

