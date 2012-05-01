%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif

Summary:        PAM bindings for Python
Name:           PyPAM
Version:        0.5.0
Release:        12%{?dist}
Source0:        http://www.pangalactic.org/PyPAM/%{name}-%{version}.tar.gz
Url:            http://www.pangalactic.org/PyPAM
Patch0:         PyPAM-dlopen.patch
Patch1:         PyPAM-0.5.0-dealloc.patch
Patch2:         PyPAM-0.5.0-nofree.patch
License:        LGPLv2
Group:          Development/Libraries
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
# This is just informative BR when someone looks at the spec
BuildRequires:  redhat-rpm-config
BuildRequires:  python2-devel pam-devel
Requires:       python
%filter_provides_in %{python_sitearch}/PAMmodule.so$
%filter_setup

%description
PAM (Pluggable Authentication Module) bindings for Python.

%prep
%setup -q
%patch0 -p1 -b .dlopen
%patch1 -p1 -b .dealloc
%patch2 -p1 -b .nofree
# remove prebuild rpm and others binaries
rm -rf build dist

%build
CFLAGS="$RPM_OPT_FLAGS -fno-strict-aliasing" %{__python} setup.py build

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install --root=$RPM_BUILD_ROOT
# Make sure we don't include binary files in the docs
chmod 644 examples/pamtest.py
rm -f examples/pamexample

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root, -)
%{python_sitearch}/PAMmodule.so
%{python_sitearch}/*.egg-info
%doc AUTHORS NEWS README ChangeLog COPYING INSTALL 
%doc examples 

%changelog
* Tue Feb 22 2011 Tomas Mraz <tmraz@redhat.com> 0.5.0-12
- 679557 - deallocate the conversation response only in case of error

* Wed Jan 19 2011 Tomas Mraz <tmraz@redhat.com> 0.5.0-11
- fix two bugs in the PAM object deallocation

* Mon Jan 17 2011 Tomas Mraz <tmraz@redhat.com> 0.5.0-9
- add -fno-strict-aliasing to CFLAGS

* Wed Jan 12 2011 Tomas Mraz <tmraz@redhat.com> 0.5.0-8
- initial build in RHEL-6

* Thu Aug 05 2010 Miroslav Suchý <msuchy@redhat.com> 0.5.0-7
- 612998 - PyPAM do not work with python3 (msuchy@redhat.com)

* Thu Aug 05 2010 Miroslav Suchý <msuchy@redhat.com> 0.5.0-6
- 612998 - fix condition for BR (msuchy@redhat.com)

* Thu Aug 05 2010 Miroslav Suchý <msuchy@redhat.com> 0.5.0-5
- 612998 - return back BR for python

* Thu Aug 05 2010 Miroslav Suchý <msuchy@redhat.com> 0.5.0-4
- 612998 - remove binaries. Just in case
- 612998 - filter provide PAMmodule.so()(64bit)
- 612998 - do not use INSTALLED_FILES feature, and enumerate files manualy
- 612998 - use %%{__python} in %%build section
- 612998 - fix buildrequires for PyPAM
- 612998 - add macros for rhel5

* Fri Jul 09 2010 Miroslav Suchý <msuchy@redhat.com> 0.5.0-3
- rebuild 

* Fri Jul 09 2010 Miroslav Suchý <msuchy@redhat.com> 0.5.0-2
- rebase PyPAM-dlopen.patch to latest source

* Fri Jul 09 2010 Miroslav Suchý <msuchy@redhat.com> 0.5.0-1
- rebase to PyPAM 0.5.0

* Fri Mar 06 2009 Devan Goodwin <dgoodwin@redhat.com> 0.4.2-26
- Fix bad patch whitespace.

* Fri Feb 27 2009 Dennis Gilmore 0.4.2-25
- rebuild to pick up ppc ppc64 ia64 arches

* Fri Feb 27 2009 Devan Goodwin <dgoodwin@redhat.com> 0.4.2-23
- Rebuild for new rel-eng tools.

* Fri May 16 2008 Michael Mraka <michael.mraka@redhat.com> 0.4.2-20
- fixed file ownership

* Tue Jun 22 2004 Mihai Ibanescu <misa@redhat.com> 0.4.2-5
- Rebuilt

* Fri Jul 11 2003 Mihai Ibanescu <misa@redhat.com>
- Adapted the original rpm to build with python 2.2
