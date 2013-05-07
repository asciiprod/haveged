Summary:        A Linux entropy source using the HAVEGE algorithm
Name:           haveged
Version:        1.7a
Release:        0%{?dist}
License:        GPLv3+
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Group:          System Environment/Daemons
URL:            http://www.irisa.fr/caps/projects/hipsor/
Source0:        http://www.issihosts.com/haveged/%{name}-%{version}.tar.gz
Source1:        haveged.service
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd

# SystemV -> SystemD conversion
# This is actually needed for the %%triggerun script but Requires(triggerun)
# is not valid.  We can use %%post because this particular %%triggerun script
# should fire just after this package is installed.
Requires(post): systemd-sysv
# SystemV -> SystemD conversion


BuildRequires:  automake gdb coreutils glibc-common

%description
A Linux entropy source using the HAVEGE algorithm

Haveged is a user space entropy daemon which is not dependent upon the
standard mechanisms for harvesting randomness for the system entropy
pool. This is important in systems with high entropy needs or limited
user interaction (e.g. headless servers).
 
Haveged uses HAVEGE (HArdware Volatile Entropy Gathering and Expansion)
to maintain a 1M pool of random bytes used to fill /dev/random
whenever the supply of random bits in /dev/random falls below the low
water mark of the device. The principle inputs to haveged are the
sizes of the processor instruction and data caches used to setup the
HAVEGE collector. The haveged default is a 4kb data cache and a 16kb
instruction cache. On machines with a cpuid instruction, haveged will
attempt to select appropriate values from internal tables.

%package devel
Summary:   Headers and shared development libraries for HAVEGE algorithm
Group:     Development/Libraries
Requires:  %{name} = %{version}-%{release}

%description devel
Headers and shared object symbolic links for the HAVEGE algorithm

%prep
%setup -q

%build
#autoreconf -fiv
%configure
#SMP build is not working
#make %{?_smp_mflags}
make

%check
make check


%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot} INSTALL="install -p"

chmod 0644 COPYING README ChangeLog AUTHORS

#Install systemd service file
rm -rf %{buildroot}/etc/init.d
pushd $RPM_BUILD_ROOT
mkdir -p .%{_unitdir}
install -p -m644 %{SOURCE1} .%{_unitdir}/haveged.service
popd

# We don't ship .la files.
rm -rf %{buildroot}%{_libdir}/libhavege.*a

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig 
%systemd_post haveged.service

%preun
%systemd_preun haveged.service

%postun
/sbin/ldconfig
%systemd_postun_with_restart haveged.service

%files
%defattr(-, root, root, -)
%{_mandir}/man8/haveged.8*
%{_sbindir}/haveged
%{_unitdir}/haveged.service
%{_libdir}/*so.*
%doc COPYING README ChangeLog AUTHORS

%files devel
%defattr(-, root, root, -)
%{_mandir}/man3/libhavege.3*
%dir %{_includedir}/%{name}
%{_includedir}/%{name}/havege.h
%doc contrib/build/havege_sample.c
%{_libdir}/*.so


%changelog
* Sun Jan 13 2013 Jirka Hladky <hladky.jiri@gmail.com> - 1.7h-0
- Couple of minor updates
* Sat Jan 12 2013 Jirka Hladky <hladky.jiri@gmail.com> - 1.7g-0
- Updated to the version 1.7
- Version 1.7 brings developement libraries
- Added devel package
* Sat Oct 13 2012 Jirka Hladky <hladky.jiri@gmail.com> - 1.5-2
- BZ 850144
- Introduce new systemd-rpm macros in haveged spec file
- Fedora 19 changes the way how to work with services in spec files. 
- It introduces new macros - systemd_post, systemd_preun and systemd_postun; 
- which replace scriptlets from Fedora 18 and older
- see https://fedoraproject.org/wiki/Packaging:ScriptletSnippets#Systemd

* Tue Aug 14 2012 Jirka Hladky <hladky.jiri@gmail.com> - 1.5-1
- Update to the version 1.5
- Main new feature is a run time verification of the produced random numbers
- PIDFILE set to /run/haveged.pid
- converted README and man page to UTF-8. Informed the upstream to fix it.
* Wed Feb 15 2012 Jirka Hladky <hladky.jiri@gmail.com> - 1.4-3
- PIDFile should be stored at /run instead of the default location /var/run 
- There is  long term plan that directory /var/run will not further exist in the future Fedora versions
- Asked upstream to add -p <PID_FILE_location> switch to influence the location of the PID File
- Set PIDFile=/var/run/haveged.pid This is needed as long -p option is not implemented
- https://bugzilla.redhat.com/show_bug.cgi?id=770306#c10
* Wed Feb 15 2012 Jirka Hladky <hladky.jiri@gmail.com> - 1.4-2
- Updated systemd service file, https://bugzilla.redhat.com/show_bug.cgi?id=770306
* Tue Feb 14 2012 Jirka Hladky <hladky.jiri@gmail.com> - 1.4-1
- Update to the version 1.4
- Conversion to systemd, drop init script
* Sun Nov 06 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.3-2
- Fixed a bug on non x86 systems
* Sat Nov 05 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.3-1
- update from the upstream (1.3 stable)
* Mon Oct 03 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.3-0
-version 1.3 beta
* Fri Sep 30 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.2-4
- ppc64 build
* Mon Sep 26 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.2-3
- Cleaned spec file according to https://bugzilla.redhat.com/show_bug.cgi?id=739347#c11
* Sat Sep 24 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.2-2
- Added comment to explain why we need use Fedora specific start script
* Wed Sep 21 2011 Jirka Hladky <hladky.jiri@gmail.com> - 1.2-1
- Cleaned spec file according to https://bugzilla.redhat.com/show_bug.cgi?id=739347#c1
* Wed Sep 07 2011  Jirka Hladky <hladky.jiri@gmail.com> - 1.2-0
- Initial build
