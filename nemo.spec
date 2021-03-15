%global _internal_version 7c1dced

%define gir_major 3.0
%define gir_name        %mklibname %{name}-gir %{gir_major}
%define libnemo_extension    %mklibname %{name}-extension
%define libname_devel   %mklibname %{name} -d
%define date 20161212

Name:           nemo
Summary:        File manager for Cinnamon
Version:        4.8.6
Release:        1
License:        GPLv2+ and LGPLv2+
Group:          File tools
URL:            https://github.com/linuxmint/nemo
Source0:        https://github.com/linuxmint/nemo/archive/%{version}/%{name}-%{version}.tar.gz
Source100:	nemo.rpmlintrc

Requires:       gvfs
Requires:       adwaita-icon-theme
Requires:       cinnamon-desktop
Requires:       cinnamon-translations

BuildRequires:  gnome-common
BuildRequires:  intltool
BuildRequires:  rarian
BuildRequires:  python-polib
BuildRequires:  pkgconfig(exempi-2.0)
BuildRequires:  pkgconfig(gail-3.0)
BuildRequires:  pkgconfig(glib-2.0)
BuildRequires:  pkgconfig(gobject-introspection-1.0)
BuildRequires:  pkgconfig(gtk+-3.0)
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(gtk-doc)
BuildRequires:  pkgconfig(libexif)
BuildRequires:  pkgconfig(libnotify)
BuildRequires:  pkgconfig(libselinux)
BuildRequires:  pkgconfig(libxml-2.0)
BuildRequires:  pkgconfig(pango)
BuildRequires:  pkgconfig(pygobject-3.0)
BuildRequires:  pkgconfig(cinnamon-desktop)
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(x11)
BuildRequires:	pkgconfig(xapp)
BuildRequires:  meson
# needed for theme subpackage
BuildRequires:  gnome-themes-standard
BuildRequires:  python-gi


# the main binary links against libnemo-extension.so
# don't depend on soname, rather on exact version
Requires:       %{libnemo_extension} = %{version}-%{release}

%description
Nemo is the file manager and graphical shell for the Cinnamon desktop
that makes it easy to manage your files and the rest of your system.
It allows to browse directories on local and remote filesystems, preview
files and launch applications associated with them.
It is also responsible for handling the icons on the Cinnamon desktop.

%package -n %{libnemo_extension}
Summary: Nemo extensions library
License: LGPLv2+
Group: Development/GNOME and GTK+

%description -n %{libnemo_extension}
This package provides the libraries used by nemo extensions.

%package -n %{libname_devel}
Summary: Support for developing nemo extensions
License: LGPLv2+
Group: Development/GNOME and GTK+
Requires: %{libnemo_extension} = %{version}-%{release}
Requires: %{gir_name} = %{version}-%{release}

%description -n %{libname_devel}
This package provides libraries and header files needed
for developing nemo extensions.

%package -n adwaita-nemo
Summary: Nemo theme fix for Adwaita
Group: Graphical desktop/Cinnamon
Buildarch: noarch
Requires:  gnome-themes-standard

%description -n adwaita-nemo
Nemo theme fix for Adwaita

%package -n %{gir_name}
Summary:        GObject Introspection interface description for %{name}
Group:          System/Libraries
Requires:       %{libnemo_extension} = %{version}-%{release}

%description -n %{gir_name}
GObject Introspection interface description for %{name}.

%prep
%setup -q
%autopatch -p1

%build

%meson
%meson_build

%install
%meson_install

desktop-file-install --delete-original       \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications             \
  --add-only-show-in GNOME                                  \
  $RPM_BUILD_ROOT%{_datadir}/applications/*

# create extensions directoy
mkdir -p $RPM_BUILD_ROOT%{_libdir}/nemo/extensions-3.0/

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_libdir}/nemo/extensions-3.0/*.la
rm -f $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/icon-theme.cache
rm -f $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/.icon-theme.cache

# theme
mkdir -p $RPM_BUILD_ROOT%{_datadir}/themes/Adwaita-Nemo/gtk-3.0/apps
ln -s %{_datadir}/themes/Adwaita/backgrounds $RPM_BUILD_ROOT%{_datadir}/themes/Adwaita-Nemo/
ln -s %{_datadir}/themes/Adwaita/gtk-2.0 $RPM_BUILD_ROOT%{_datadir}/themes/Adwaita-Nemo/
ln -s %{_datadir}/themes/Adwaita/gtk-3.0/{gtk.gresource,settings.ini} $RPM_BUILD_ROOT%{_datadir}/themes/Adwaita-Nemo/gtk-3.0/
ln -s %{_datadir}/themes/Adwaita/metacity-1 $RPM_BUILD_ROOT%{_datadir}/themes/Adwaita-Nemo/
ln -s %{_datadir}/themes/Adwaita/index.theme $RPM_BUILD_ROOT%{_datadir}/themes/Adwaita-Nemo/index.theme

#find_lang %name

%files
%{_datadir}/nemo/
%{_datadir}/applications/*
%{_datadir}/mime/packages/nemo.xml
%{_bindir}/*
%{_datadir}/icons/hicolor/*/apps/nemo.png
%{_datadir}/icons/hicolor/*/actions/*.png
%{_datadir}/icons/hicolor/scalable/*/*.svg
%{_datadir}/icons/hicolor/48x48/status/progress-*.png
%{_datadir}/dbus-1/services/nemo.service
%{_datadir}/dbus-1/services/nemo.FileManager1.service
%{_mandir}/man1/nemo-connect-server.1.*
%{_mandir}/man1/nemo.1.*
%{_libexecdir}/nemo-convert-metadata
%{_libexecdir}/nemo-extensions-list
%{_datadir}/glib-2.0/schemas/*
%dir %{_libdir}/nemo/extensions-3.0/
%{_datadir}/polkit-1/actions/org.nemo.root.policy
%{_datadir}/gtksourceview-?.0/language-specs/nemo_action.lang


%files -n %{libnemo_extension}
%{_libdir}/libnemo-extension.so.*

%files -n adwaita-nemo
%{_datadir}/themes/Adwaita-Nemo/

%files -n %{libname_devel}
%{_includedir}/nemo/
%{_libdir}/pkgconfig/*
%{_libdir}/*.so
%{_datadir}/gir-1.0/*.gir

%files -n %{gir_name}
%{_libdir}/girepository-1.0/*.typelib
