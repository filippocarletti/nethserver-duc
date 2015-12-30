Summary:    Analysis of space and usage of disk
Name:       nethserver-duc
Version: 1.3.3
Release: 1%{?dist}
License:    GPL
URL:        %{url_prefix}/%{name}
Source0:    %{name}-%{version}.tar.gz
BuildArch:  noarch

Requires:   nethserver-base
Requires:   duc >= 1.3.3

BuildRequires: nethserver-devtools

%description
Visualize the space and the usage of your disk.

%prep
%setup

%build
perl createlinks
install -d \
   root/%{_nseventsdir}/%{name}-update \
   root/var/cache/duc \
   root/usr/share/duc

%install
rm -rf %{buildroot}
(cd root; find . -depth -print | cpio -dump %{buildroot})
%{genfilelist} %{buildroot} > %{name}-%{version}-filelist

%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
%doc COPYING
%dir %{_nseventsdir}/%{name}-update
%dir /var/cache/duc
%dir /usr/share/duc

%changelog
* Mon Jul 06 2015 Giacomo Sanchietti <giacomo.sanchietti@nethesis.it> - 1.0.4-1
- Move out "Disk usage" from Dashboard - Enhancement #3204 [NethServer]

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
