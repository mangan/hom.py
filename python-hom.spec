%global srcname hom.py
Name:		python-hom
Version:	1.4
Release:	1%{?dist}
BuildArch:	noarch
Summary:	Higher Order Messages for lists

License:	MIT
Source0:	%{srcname}-%{version}.tar.gz

BuildRequires:	python


%description
Higher Order Messages provides another level of abstraction to iterate over
list. Following OOP manner lists are iterated via special methods rather then
loops.


%prep
%setup -n %{srcname}-%{version}


%build
%{__python} setup.py build


%install
%{__python} setup.py install --skip-build --root %{buildroot}


%files
%{python_sitelib}/hom.py*
%{python_sitelib}/%{srcname}-*.egg-info


%changelog

