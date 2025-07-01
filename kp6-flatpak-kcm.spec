#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.4.2
%define		qtver		5.15.2
%define		kpname		flatpak-kcm

Summary:	KDE Config Module for flatpak
Name:		kp6-%{kpname}
Version:	6.4.2
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	aaeab1e81be39fc069e1cecef22ad54e
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	cmake >= 3.16.0
BuildRequires:	flatpak-devel
BuildRequires:	kf6-kauth-devel
BuildRequires:	kf6-kconfigwidgets-devel
BuildRequires:	kf6-kcoreaddons-devel
BuildRequires:	kf6-ki18n-devel
BuildRequires:	kf6-kio-devel
BuildRequires:	kf6-kxmlgui-devel
BuildRequires:	ninja
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
Obsoletes:	kp5-%{kpname} < 6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
KDE Config Module for flatpak.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kpname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun


%files -f %{kpname}.lang
%defattr(644,root,root,755)
%{_libdir}/qt6/plugins/plasma/kcms/systemsettings/kcm_flatpak.so
%{_desktopdir}/kcm_flatpak.desktop
