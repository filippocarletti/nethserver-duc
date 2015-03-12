# Disable byte compiling
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')

Summary:    Analysis of space and usage of disk
Name:       nethserver-duc
Version: 1.0.3
Release: 1%{?dist}
License:    GPL
URL:        %{url_prefix}/%{name}
Source0:    %{name}-%{version}.tar.gz
BuildArch:  noarch

Requires:   nethserver-base
Requires:   duc

BuildRequires: perl
BuildRequires: nethserver-devtools

%description
Visualize the space and the usage of your disk.

%prep
%setup

%build
perl createlinks

%install
rm -rf $RPM_BUILD_ROOT
(cd root; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
%{genfilelist} $RPM_BUILD_ROOT > %{name}-%{version}-filelist
echo "%doc COPYING" >> %{name}-%{version}-filelist
grep -v -E '(xml2json.pyc|xml2json.pyo)' %{name}-%{version}-filelist > tmp-filelist
mv tmp-filelist %{name}-%{version}-filelist

%post

%preun

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)

%changelog
* Thu Mar 12 2015 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.3-1
- DUC dashboard: wrong tab order - Bug #3077 [NethServer]

* Wed Mar 04 2015 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.2-1
- DUC indexing fails with empty backup property - Bug #3073 [NethServer]

* Tue Mar 03 2015 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.1-1
- DUC (Disk Usage): Backup directory visualized in the graph - Bug #3062 [NethServer]
- Disk usage dashboard panel misses some directories - Bug #3057 [NethServer]

* Thu Feb 19 2015 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.0-1
- Dashboard widget for disk utilization - Feature #2687 [NethServer]

* Mon Feb 9 2015 Edoardo Spadoni <edoardo.spadoni@nethesis.it> - 1.0
- first release
