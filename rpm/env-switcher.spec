# -*- rpm-spec -*-
#
# Copyright (c) 2002-2004 The Trustees of Indiana University.  
#                         All rights reserved.
#
# This file is part of the Env-switcher software package.  For license
# information, see the LICENSE file in the top-level directory of the
# Env-switcher source distribution.
#
# $Id: env-switcher.spec.in,v 1.15 2004/03/07 22:06:54 jsquyres Exp $
#

#############################################################################
#
# Helpful Defines
#
#############################################################################

# This is an OSCAR-specific RPM specfile.  As such, it should not go
# in the "usual" location where binaries and things are installed --
# it needs to be rooted in an OSCAR-specific directory.  Specifying
# --prefix and --exec-prefix in the configure statement is not enough
# -- we have to override RPM's defaults and give it the specific
# prefix to use in several of its directories.

%define _prefix /opt/env-switcher
%define _sysconfdir /opt/env-switcher/etc
%define _datadir /opt/env-switcher/share
%define _mandir /opt/env-switcher/man
%define _modulefilesdir /opt/modules/oscar-modulefiles

# Defining these to nothing overrides the stupid automatic RH9
# functionality of making "debuginfo" RPMs.

%define debug_package %{nil}
%define __check_files %{nil}


#############################################################################
#
# Preamble Section
#
#############################################################################

Summary: Env-switcher package
Name: env-switcher
Version: 1.0.13
Release: 1
License: BSD
Group: Applications/Environment
Source: env-switcher-%{version}.tar.gz
URL: http://oscar.sourceforge.net/
Vendor: Open Cluster Group / OSCAR working group
Packager: Jeff Squyres <jsquyres@lam-mpi.org>
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Requires: modules-oscar tcl
Provides: switcher
AutoReqProv: no

%description 
The env-switcher package provides an convenient method for users to
switch between "similar" packages.  System- and user-level defaults
are maintained in data files and are examined at shell invocation time
to determine how the user's enviornment should be set up.

The canonical example of where this is helpful is using multiple
implementations of the Message Passing Interface (MPI).  This
typically requires that the user's "dot" files are set appropriately
on each machine that is used since rsh/ssh are typically used to
invoke commands on remote nodes.

The env-switcher package alleviates the need for users to manually
edit their fot files, and instead gives the user commandline control
to switch between multiple implementations of MPI.

While this package was specifically motivated by the use of multiple
MPI implementations on OSCAR clusters, there is nothing specific to
either OSCAR or MPI in env-switcher -- switching between mulitple MPI
implementations is only used in this description as an example.  As
such, it can be used in any environment for any "switching" kind of
purpose.


#############################################################################
#
# Prep Section
#
#############################################################################
%prep
%setup -q


#############################################################################
#
# Build Section
#
#############################################################################
%build
%configure --with-modulefiles=%{_modulefilesdir} --enable-suppress-errors
make all


#############################################################################
#
# Install Section
#
#############################################################################
%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

# Since this is a %config file, it has to exist
touch $RPM_BUILD_ROOT/%{_sysconfdir}/switcher.ini


#############################################################################
#
# Clean Section
#
#############################################################################
%clean
rm -rf $RPM_BUILD_ROOT


#############################################################################
#
# Post install Section
#
#############################################################################
%post

# Make switcher availabe in /bin because Mandrake >= 8.2 is stupid
# (root's .bashrc won't allow /etc/profile.d scripts to modify PATH).

if test "%{_bindir}" != "/bin"; then
    %__rm -f /bin/switcher
    ln -s %{_bindir}/switcher /bin
fi


#############################################################################
#
# Pre-uninstall Section
#
# Only execute this if this is the last instance of the env-switcher
# RPM that is being uninstalled (i.e., do *not* execute this if we're
# updgrading).
#
#############################################################################
%preun

if test "$1" = "0" -a "%{_bindir}" != "/bin" -a -L /bin/switcher; then
    %__rm -f /bin/switcher
fi


#############################################################################
#
# Files Section
#
#############################################################################
%files

%defattr(-,root,root)
%doc README LICENSE AUTHORS
%config %{_sysconfdir}/switcher.ini
%{_prefix}
%{_modulefilesdir}


#############################################################################
#
# ChangeLog
#
#############################################################################
%changelog
* Thu May 14 2004 Jeff Squyres <jsquyres@lam-mpi.org>
- Change switcher-reload to switcher_reload, because at least some flavors
  of sh/bash will barf when module's alias command makes that the name
  of a shell subroutine.

* Tue Oct 29 2002 Jeff Squyres <jsquyres@lam-mpi.org>
- Ensure that return value from switcher executable is properly
  propogated to the shell return status

* Sun Oct 27 2002 Jeff Squyres <jsquyres@lam-mpi.org>
- Added AUTHORS file to %doc list
- Added a few missing copyright notices

* Thu Sep 26 2002 Jeff Squyres <jsquyres@lam-mpi.org>
- Fixed an infinite loop corner case in the command line options parser
- The --show option now indicates what level each attribute was
  resolved at ("user" or "system")
- Cleaned up the perl in the "switcher" executable a lot via "use
  strict".

* Mon Aug 12 2002 Jeff Squyres <jsquyres@lam-mpi.org>
- Remove extraneous echo statements in scriptlets.
- Don't remove the sym link during "rpm -Uvh".
- Upgrade to version 1.0.6, release 1
- Have modulefile check for /bin/switcher before attempting to run the
  switcher command

* Sun Aug 11 2002 Jeff Squyres <jsquyres@lam-mpi.org>
- Depend on modules-oscar, not modules.
- Depend on perl-AppConfig, not libappconfig-perl.
- Remove "oscar" from the release number, per new OSCAR standards.

* Sat Jul 27 2002 Jeff Squyres <jsquyres@lam-mpi.org>
- Make a sym link from %{_bindir}/switcher to /bin/switcher because
  MDK >= 8.2 is stupid (root's .bashrc doesn't allow /etc/profile.d
  scripts to modify the path).
- Minor bug fixes ("module unload switcher" now works)
- Now install into /opt/env-switcher (vs. /opt/env-switcher-$version)
  to preserve the config file switcher.ini across rpm -Uvh
- Marked %{_sysconfdir}/switcher.ini as a %config file, and no longer
  forcibly remove it in $preun.

* Sat May 18 2002 Jeff Squyres <jsquyres@lam-mpi.org>
- Updated to env-switcher 1.0.2.

* Sat Apr 27 2002 Jeff Squyres <jsquyres@lam-mpi.org>
- Use %__rm macro in the %preun section
- Added some more requires (perl, tcl), just to be absolutely safe
- Changed the package name to env-switcher

* Sat Apr 21 2002 Jeff Squyres <jsquyres@lam-mpi.org>
- Fixed typo in %clean section

* Sun Apr 14 2002 Jeff Squyres <jsquyres@lam-mpi.org>
- Revamp the process to get the directories and version number into
  the specfile; automate the RPM building process better
- Change the %postun to %preun so that we get proper removal of the
  entire %{prefix} tree during rpm -e.

* Sat Apr 13 2002 Jeff Squyres <jsquyres@lam-mpi.org>
- Minor update to allow the removal of the last name on a tag to also
  remove that tag.
- Updated docs to say what this package does and how to use it.

* Sun Apr  7 2002 Jeff Squyres <jsquyres@lam-mpi.org>
- Initial try at a SPEC file for switcher.
