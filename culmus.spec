Summary:	Free Hebrew Type1 fonts
Name:		culmus-fonts
Version:	0.101
Release:	1
Vendor:		Culmus Project

# This is intended to solve the upgrading problems introduced by 
# the version number "culmus-0.71" : since 71>8, this package
# would have had a lower version number
#
# To solve this I will use the epoch header. It is a slight abuse,
# and therefore I keep the epoch as 1, in case anybody needs
# the epoch for other uses (e.g:incorporating culmus as a part of a 
# larger package.
#
# Note that the version number will now be epoch:version-release, 
# instead of simply version-release

# Aug-15-2003 Maxim Iorsh:
# By request from RH, release numbers will be 90, 100, 110, etc.
# Minor releases could be added between them: 91, 92...
Epoch:		1

%define     fonts_dir  %{_datadir}/fonts/he/Type1
%define     doc_dir  %{_datadir}/doc/culmus-%{version}
%define     fcconf_dir  %{_sysconfdir}/fonts

Source0:	http://belnet.dl.sourceforge.net/sourceforge/culmus/culmus-%{version}.tar.gz

License:	GPL
Group:		System/Fonts/Type1
URL:		http://culmus.sourceforge.net/
BuildRoot:	%_tmppath/%name-%version-%release-root
BuildArch:	noarch
BuildRequires:	XFree86
# SuSE doesn't have chkfontpath. Strange.
# Prereq:		chkfontpath

%description
This version fixes the "tet" bug (see Mandrakesoft Bugzilla Bug 11502).

9 Hebrew font families. ASCII glyphs partially borrowed from
the URW and Bitstream fonts.  Those families provide a basic set of a
serif (Frank Ruehl), sans serif (Nachlieli) and monospaced (Miriam Mono)
fonts. Also included Miriam, Drugulin, Aharoni, David, Yehuda and Ellinia.

Install the culmus-fonts package if you need a set of Hebrew fonts.

%prep
%setup -n culmus-%{version}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{fonts_dir}
mkdir -p $RPM_BUILD_ROOT%{fcconf_dir}
mkdir -p $RPM_BUILD_ROOT/tmp
#cd fonts
/usr/X11R6/bin/xftcache . || touch XftCache
cp -f *.afm *.pfa $RPM_BUILD_ROOT%{fonts_dir}
install -m 644 fonts.scale $RPM_BUILD_ROOT%{fonts_dir}/
install -m 644 fonts.alias $RPM_BUILD_ROOT%{fonts_dir}/
install -m 644 local.conf $RPM_BUILD_ROOT%{fonts_dir}/
install -m 644 XftCache $RPM_BUILD_ROOT%{fonts_dir}/
install -m 644 culmus.conf $RPM_BUILD_ROOT%{fcconf_dir}/

mkfontdir $RPM_BUILD_ROOT%{fonts_dir}

%post
# if chkfontpath exists, execute it
if [ -x %{_sbindir}/chkfontpath ]; then
	%{_sbindir}/chkfontpath -q -a %{fonts_dir}
fi
# avoid making fc-cache a requirement
if which fc-cache >&/dev/null; then
  fc-cache
fi
# install /etc/fonts/local.conf, if it doesn't exist
# for example, in Red Hat.
if ! [ -f %{fcconf_dir}/local.conf ]; then
	cp %{fonts_dir}/local.conf %{fcconf_dir}/
fi
# add culmus.conf include entry to local.conf
if !(grep -q -e culmus.conf %{fcconf_dir}/local.conf); then
        sed -i -e '/<fontconfig>/a<include ignore_missing="yes">culmus.conf</include>' %{fcconf_dir}/local.conf
fi

%postun
if [ "$1" = "0" ]; then
# if chkfontpath exists, execute it
	if [ -x %{_sbindir}/chkfontpath ]; then
		%{_sbindir}/chkfontpath -q -r %{fonts_dir}
	fi
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(0644,root,root,0755)
%dir %{fonts_dir}
%doc CHANGES LICENSE LICENSE-BITSTREAM GNU-GPL
%config(noreplace) %{fonts_dir}/fonts.dir
%config(noreplace) %{fonts_dir}/fonts.scale
%config(noreplace) %{fonts_dir}/fonts.alias
%config(noreplace) %{fonts_dir}/XftCache
%config		   %{fcconf_dir}/culmus.conf
%{fonts_dir}/*.afm
%{fonts_dir}/*.pfa
%{fonts_dir}/local.conf

%changelog
* Sat Jun 12 2004 Maxim Iorsh <iorsh@math.technion.ac.il> 0.100-1
- /etc/fonts/local.conf is installed, if didn't exist previously

* Wed Jan 28 2004 Maxim Iorsh <iorsh@math.technion.ac.il> 0.93-1
- added custom configuration file /etc/fonts/culmus.conf
- made chkfontpath non-mandatory (SuSE 9 doesn't have it)

* Wed Sep 03 2003 Maxim Iorsh <iorsh@math.technion.ac.il> 0.90-2
- fixed issue about printing from Open Office

* Fri Aug 15 2003 Maxim Iorsh <iorsh@math.technion.ac.il> 0.90-1
- major release
- version numbers changed by request from O. Taylor (RH)

* Sun Mar 30 2003 Tzafrir Cohen <tzafrir@technion.ac.il> 0.8-2
- Fixed filename of tar source
- made fc-cache non-mandatory (to work on RH7.3 systems)
- used the macro doc in files list
- add an epoch to allow upgrades from culmus-0.71-1

* Thu Mar 20 2003 Maxim Iorsh <iorsh@math.technion.ac.il> 0.8-1
- Call fc-cache from %%post

* Thu Aug 29 2002 Tzafrir Cohen <tzafrir@technion.ac.il> 0.5-1
- created spec for version 0.5, based on URW package
