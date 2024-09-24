%global  qt_version 6.7.2

Summary: Qt6 - Qt Shader Tools module builds on the SPIR-V Open Source Ecosystem
Name:    qt6-qtshadertools
Version: 6.7.2
Release: 0%{?dist}

License: LGPL-3.0-only OR GPL-3.0-only WITH Qt-GPL-exception-1.0
Url:     http://www.qt.io
%global  majmin %(echo %{version} | cut -d. -f1-2)
%global  qt_version %(echo %{version} | cut -d~ -f1)

Source0: %{name}-%{version}.tar.bz2

BuildRequires: clang
BuildRequires: cmake
BuildRequires: ninja
BuildRequires: qt6-qtbase-devel >= %{qt_version}
BuildRequires: qt6-qtbase-private-devel
%{?_qt6:Requires: %{_qt6}%{?_isa} = %{_qt6_version}}
BuildRequires: pkgconfig(xkbcommon) >= 0.4.1

%description
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: qt6-qtbase-devel%{?_isa}
%description devel
%{summary}.


%prep
%autosetup -n %{name}-%{version}/upstream -p1


%build
%cmake_qt6

%cmake_build


%install
%cmake_install

# hardlink files to %{_bindir}, add -qt6 postfix to not conflict
mkdir -p %{buildroot}%{_bindir}
pushd %{buildroot}%{_qt6_bindir}
for i in * ; do
  case "${i}" in
    qsb)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}-qt6
      ;;
    *)
      ln -v  ${i} %{buildroot}%{_bindir}/${i}
      ;;
  esac
done
popd

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_qt6_libdir}
for prl_file in libQt6*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%license LICENSES/*
%{_bindir}/qsb-qt6
%{_qt6_bindir}/qsb
%{_qt6_libdir}/libQt6ShaderTools.so.6*


%files devel
%{_qt6_archdatadir}/mkspecs/modules/*.pri
%{_qt6_libdir}/qt6/modules/*.json
%{_qt6_headerdir}/QtShaderTools/
%{_qt6_libdir}/libQt6ShaderTools.prl
%{_qt6_libdir}/libQt6ShaderTools.so
%{_qt6_libdir}/cmake/Qt6BuildInternals/StandaloneTests/QtShaderToolsTestsConfig.cmake
%dir %{_qt6_libdir}/cmake/Qt6ShaderTools/
%{_qt6_libdir}/cmake/Qt6ShaderTools/*.cmake
%dir %{_qt6_libdir}/cmake/Qt6ShaderToolsTools/
%{_qt6_libdir}/cmake/Qt6ShaderToolsTools/*.cmake
%{_qt6_libdir}/qt6/metatypes/qt6*_metatypes.json
%{_qt6_libdir}/pkgconfig/Qt6ShaderTools.pc
