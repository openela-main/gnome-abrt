# TODO: https://fedoraproject.org/wiki/Packaging:AutoProvidesAndRequiresFiltering
#       rpmlint warns about private-shared-object-provides
#       can't use filter because the package doesn't met any of the required criteria
#         ! Noarch package       ... caused by libreport wrappers shared library
#         ! no binaries in $PATH ... caused by gnome-abrt python script in /usr/bin

Name:       gnome-abrt
Version:    1.2.6

Release:    6%{?dist}

Summary:    A utility for viewing problems that have occurred with the system

License:    GPLv2+
URL:        https://github.com/abrt/gnome-abrt
Source0:    https://github.com/abrt/%{name}/archive/%{version}/%{name}-%{version}.tar.gz

# git format-patch %%{Version} --topo-order -N -M;
# i=1; for p in `ls 0*.patch`; do printf "Patch%04d: %s\n" $i $p; ((i++)); done
Patch0001: 0001-Remove-Expert-mode-and-the-remaining-Analyze-code.patch
Patch0002: 0002-Mark-the-help-command-line-descriptions-for-translat.patch
Patch0003: 0003-Translation-updates.patch
Patch0004: 0004-Translation-updates.patch
Patch0005: 0005-Apply-the-new-packaging-guidelines.patch
# Patch0006: 0006-autogen-correctly-parse-buildrequires-from-spec-file.patch
Patch0007: 0007-pylint-fix-some-pylint-warnings.patch
Patch0008: 0008-Fix-incorrect-parsing-of-reported_to-file.patch
# Patch0009: 0009-spec-Fix-files-listed-twice.patch
Patch0010: 0010-pylint-R0205-Remove-explicit-object-inheritance.patch
# Patch0011: 0011-spec-Fix-python3-libreport-dependency.patch
Patch0012: 0012-views-Allow-reporting-non-reportable-problems.patch

# git is need for '%%autosetup -S git' which automatically applies all the
# patches above. Please, be aware that the patches must be generated
# by 'git format-patch'
BuildRequires: git

BuildRequires: intltool
BuildRequires: gettext
BuildRequires: libtool
BuildRequires: python3-devel
BuildRequires: desktop-file-utils
BuildRequires: asciidoc
BuildRequires: xmlto
BuildRequires: pygobject3-devel
BuildRequires: libreport-gtk-devel >= 2.6.0
BuildRequires: python3-libreport
BuildRequires: abrt-gui-devel >= 2.6.0
BuildRequires: gtk3-devel
BuildRequires: libX11-devel
BuildRequires: sed

%if 0%{?fedora}
# 2015-11-12 <jfilak>:
# I temporarily disabled pylint after discussion with rkuska and kalev. pylint
# cannot be built for Python-3.5 and gnome-abrt uses it only for 'make check'.
%bcond_without pylint
BuildRequires: python3-six
BuildRequires: python3-inotify
BuildRequires: python3-gobject
BuildRequires: python3-dbus
BuildRequires: python3-humanize
%else
%bcond_with pylint
%endif

%if %{with pylint}
BuildRequires: python3-pylint
%else
%define checkoption --with-nopylint
%endif

Requires:   python3-libreport
Requires:   python3-inotify
Requires:   python3-gobject
Requires:   python3-dbus
Requires:   xdg-utils
Requires:   python3-humanize

%description
A GNOME application allows users to browse through detected problems and
provides them with convenient way for managing these problems.


%prep
# http://www.rpm.org/wiki/PackagerDocs/Autosetup
# Default '__scm_apply_git' is 'git apply && git commit' but this workflow
# doesn't allow us to create a new file within a patch, so we have to use
# 'git am' (see /usr/lib/rpm/macros for more details)
%define __scm_apply_git(qp:m:) %{__git} am
%autosetup -S git


%build
autoconf
%configure %{?checkoption}
make


%install
make install DESTDIR=$RPM_BUILD_ROOT mandir=%{_mandir}
%find_lang %{name}

# remove all .la and .a files
find $RPM_BUILD_ROOT -name '*.la' -or -name '*.a' | xargs rm -f

desktop-file-install \
    --dir ${RPM_BUILD_ROOT}%{_datadir}/applications \
    --delete-original \
    ${RPM_BUILD_ROOT}%{_datadir}/applications/%{name}.desktop

# Switch hardcoded python3 shebangs into the %%{__python3} macro
sed -i '1s=^#!/usr/bin/python3\($\|\s\)=#!%{__python3}\1=' \
    %{buildroot}%{_bindir}/gnome-abrt

%check
%if %{with pylint}
make check
%endif


%files -f %{name}.lang
%doc COPYING README.md
%{python3_sitearch}/gnome_abrt
%{_datadir}/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/*
%{_datadir}/metainfo/*
%{_mandir}/man1/%{name}.1*
%{_datadir}/icons/hicolor/*/apps/*
%{_datadir}/icons/hicolor/*/status/*


%changelog
* Tue Mar 10 2020 Ernestas Kulik <ekulik@redhat.com> - 1.2.6-6
- Add patch for rhbz#1791655

* Tue Jul 17 2018 Matej Habrnal <mhabrnal@redhat.com> - 1.2.6-5
- pylint(R0205): Remove explicit object inheritance
- Fix incorrect parsing of reported_to file
- Apply the new packaging guidelines
- Mark the `--help' command line descriptions for translation
- Remove Expert mode and the remaining Analyze code

* Mon Jul 16 2018 Matej Habrnal <mhabrnal@redhat.com> - 1.2.6-4
- Switch hardcoded python3 shebangs into the %%{__python3}

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Sat Jan 06 2018 Igor Gnatenko <ignatenkobrain@fedoraproject.org> - 1.2.6-2
- Remove obsolete scriptlets

* Thu Nov 16 2017 Julius Milan <jmilan@redhat.com> 1.2.6-1
- Translation updates
- Satisfy pylint v1.7.1 warnings
- pylintrc: disable pylint no-else-return warnings
- Add fur, kk, nn languages into LINGUAS

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Wed Jul 12 2017 Rafal Luzynski <digitalfreak@lingonborough.com> 1.2.5-4
- New translations: Friulian, Kazakh, Norwegian Nynorsk
- Translation updates: Dutch, Finnish, Marathi

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.5-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.2.5-2
- Rebuild for Python 3.6

* Mon Oct 31 2016 Rafal Luzynski <digitalfreak@lingonborough.com> 1.2.5-1
- Translation updates
- Fix some small issues to please pylint
- Fix padding of the list items
- Update the project URL

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.4-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue Jun 28 2016 Rafal Luzynski <digitalfreak@lingonborough.com> 1.2.4-2
- Translation updates (Albanian)
- Resolves: #1347951

* Tue Jun 07 2016 Rafal Luzynski <digitalfreak@lingonborough.com> 1.2.4-1
- Translation updates (Russian, Slovak)
- Add new translation languages - Albanian
- One more fix for the format of a package version
- Align the header buttons position to the sidebar size

* Wed Apr 13 2016 Rafal Luzynski <digitalfreak@lingonborough.com> 1.2.3-3
- Correct format of the package version
- Translation updates

* Fri Apr 08 2016 Rafal Luzynski <digitalfreak@lingonborough.com> 1.2.3-2
- Translation updates

* Wed Mar 23 2016 Jakub Filak <jfilak@redhat.com> 1.2.3-1
- Translation updates
- Let main title of the crash wrap
- Label all kernel oops problems with "System"
- Disambiguate the word "System"
- Use context gettext
- Reword "Detected" to "First Detected"
- Use "Problem Reporting" as the program name in the About box
- Remove "Report problem with ABRT"
- Fix dim-label being applied to proper app icons
- Make "Select" button unsensitive when list is empty
- Make titlebar blue in selection mode
- Use dim-label style, not hard-coded colours for labels
- Remove "ABRT Configuration" dialogue
- Add search button
- Add more keywords to .desktop

* Thu Feb 18 2016 Jakub Filak <jfilak@redhat.com> - 1.2.2-1
- Translation updates
- Fix the plural/singular translations for fancydate -Rafal Luzynski <digitalfreak@lingonborough.com>
- Details pane: new design - Rafal Luzynski <digitalfreak@lingonborough.com>

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Dec 18 2015 Jan Beran <jberan@redhat.com> - 1.2.1-2
- Do not pass None to function expecting str object
- Add kudos to the AppData file
- Problem type included in the problem list: Rafal Luzynski <digitalfreak@lingonborough.com>
- Scroll whole details panel instead of its single widgets: Rafal Luzynski <digitalfreak@lingonborough.com>
- Fix broken build caused by pylint warning

* Thu Nov 19 2015 Jakub Filak <jfilak@redhat.com> - 1.2.1-1
- HTMLParseError replaced with generic Exception: Francesco Frassinelli <fraph24@gmail.com>
- Fix handling of the singular cases: Rafal Luzynski <digitalfreak@lingonborough.com>
- Don't scroll the sidebar horizontally: Rafal Luzynski <digitalfreak@lingonborough.com>
- Show HiDPI icons on HiDPI screens: Rafal Luzynski <digitalfreak@lingonborough.com>
- Get rid of the Gtk3 module loading warning
- Translation updates
- Resolves: #1283365

* Thu Nov 12 2015 Jakub Filak <jfilak@redhat.com> - 1.2.0-9
- Fix build with Python 3.5

* Thu Nov 12 2015 Jakub Filak <jfilak@redhat.com> - 1.2.0-8
- Temporarily stop using pylint and turn off 'make check'
- Rebuilt for Python3.5 rebuild

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Fri Nov 6 2015 Jakub Filak <jfilak@redhat.com> - 1.2.0-6
- Rebuilt for Python3.5 rebuild

* Fri Aug 14 2015 Matej Habrnal <mhabrnal@redhat.com> - 1.2.0-5
- Correct testing of return values from ABRT D-Bus API wrrapper

* Mon Jul 13 2015 Jakub Filak <jfilak@redhat.com> - 1.2.0-4
- Fix loading applicaton icons
- Fix an exception when searching for a bug ID
- Resolves: #1242080

* Thu Jun 18 2015 Matej Habrnal <mhabrnal@redhat.com> - 1.2.0-3
- Use UTF-8 encoding when working with user files
- Remove the Details button from the top bar in non-GNOME desktops

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 09 2015 Jakub Filak <jfilak@redhat.com> 1.2.0-1
- Enabled the Details also for the System problems
- Do not crash in the testing of availabitlity of XServer
- Remove a debug print introduced with port to Python3
- Fix 'Open problem's data directory'
- Quit Application on Ctrl+Q
- Translation updates
- Resolves: #1188002

* Mon May 11 2015 Matej Habrnal <mhabrnal@redhat.com> - 1.1.2-2
- Translations update

* Tue May 05 2015 Matej Habrnal <mhabrnal@redhat.com> - 1.1.2-1
- Add symbolic icon
- Use own window header also in GNOME Classic
- Let the theme handle the colour in the problems list
- Remove border's custom style in the problems list
- Resolves: #1193656

* Thu Apr 09 2015 Jakub Filak <jfilak@redhat.com> - 1.1.1-1
- Several bug fixes

* Tue Mar 17 2015 Jakub Filak <jfilak@redhat.com> - 1.1.0-2
- Fix a crash caused by i18n
- Fix a crash caused by problems without environment file
- Resolves: #1204524

* Tue Mar 17 2015 Jakub Filak <jfilak@redhat.com> - 1.1.0-1
- Switch to Python3
- Translation updates
- Search by Bug Tracker ID
- Always show an icon for problems
- Try to use environment to find the application
- Polished look

* Mon Oct 13 2014 Jakub Filak <jfilak@redhat.com> - 1.0.0-1
- New upstream release with updated look & feel

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.7-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Jul 22 2014 Jakub Filak <jfilak@redhat.com> - 0.3.7-4
- Teach the GUI to understand the Exec key format
- Put "About" and "Quit" into a section
- Do not close the report dialog with the main window
- Wrap words in "Report problem with ABRT" dialogue

* Tue Jul 15 2014 Jakub Filak <jfilak@redhat.com> - 0.3.7-3
- Properly handle UTF-8 problem filter input (apply the patch)

* Mon Jun 23 2014 Jakub Filak <jfilak@redhat.com> - 0.3.7-2
- Properly handle UTF-8 problem filter input

* Wed Jun 11 2014 Jakub Filak <jfilak@redhat.com> 0.3.7-1
- Fix XDG_RUNTIME_DIR not set messages by creating one
- Handle UTF-8 problem filter input
- Disable "no-member" check in pylintrc
- Fix issues uncovered by a newer version of pylint
- Do not crash in case of a DBus timeout
- Fix too long line
- Ignore problems without 'type' element
- Resolves: #1107429

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.3.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 05 2014 Jakub Filak <jfilak@redhat.com> 0.3.6-1
- Translation updates
- Merge pull request #51 from abrt/more_visual
- Use human readable type string everywhere
- Merge pull request #50 from abrt/visuals
- Display C/C++ instead of CCpp
- Truncate possibly long component name to 40 chars.
- Disable horizontal scrollbar on problem list
- Right-alignment of date entries
- Initialize gnome_abrt module before importing its submodules

* Mon Jan 13 2014 Jakub Filak <jfilak@redhat.com> 0.3.5-1
- Do not crash when a FileIcon cant be loaded
- Enable multiple problems selection
- Fix a typo in appdata - <mike.catanzaro@gmail.com>
- Update translations

* Thu Dec 19 2013 Jakub Filak <jfilak@redhat.com> 0.3.4-1
- Do not use deprecated GObject API
- Make gnome-abrt compatible with Python GObject < 3.7.2
- Do not fail if there is no Problem D-Bus service
- Make all labels selectable
- Run xdg-open for problem directory nonblocking
- Resolves: #1043025

* Wed Dec 18 2013 Jakub Filak <jfilak@redhat.com> 0.3.3-3
- Fix translations

* Mon Nov 04 2013 Jakub Filak <jfilak@redhat.com> 0.3.3-2
- Expand list of problems
- Resolves: #1025308

* Sat Oct 26 2013 Jakub Filak <jfilak@redhat.com> 0.3.3-1
- Make problem list resizable
- Make info about Reported state of problem more clear
- Less confusing message about missing Bugzilla ticket
- Resolves: #1018285

* Fri Oct 04 2013 Jakub Filak <jfilak@redhat.com> 0.3.2-1
- Fix a bug in SIGCHLD handler causing 100% CPU usage
- Show "yes" in Reported field only if no URL is available
- Load only the most recent reported to value
- Check if Application has valid name in filter fn
- Fix issues found by new pylint
- Resolves: #1009189, #1015609

* Thu Sep 12 2013 Jakub Filak <jfilak@redhat.com> 0.3.1-1
- Improve user experience
- Make About dialog transient for the main window
- Add AppData file
- Ship the 256x256 icon in the right place
- Recover from fork errors
- Add ABRT configure application menu
- Use absolute path in python shebang
- Recover from invalid time stamp values
- Use wrapped text for the bug report link
- Resolves: #1004276

* Fri Jul 26 2013 Jakub Filak <jfilak@redhat.com> 0.3.0-1
- Do not include url files twice
- Get rid of Stock Items usage
- Do not remove invalid problems while sorting the list
- Check if X display can be opened
- Fix a condition in the source changed notification handler
- Update Translations
- Skip inotify events for sub folders in dump location watcher
- Use GLib.io_add_watch() instead of IOChanell.add_watch()
- Fix a typo in macro name
- Remove shebang from non-executable scripts
- Remember missing elements and load them only once
- Download more problem elements in a single D-Bus call
- Improve data caching
- Display two sets of problems (My/System)
- Fix typo in dbus error message
- Don't crash if a new directory problem is invalid

* Mon May 06 2013 Jakub Filak <jfilak@redhat.com> 0.2.12-3
- Disable downloading of HTML titles

* Mon May 06 2013 Jakub Filak <jfilak@redhat.com> 0.2.12-2
- Fix a wrong path in contoller.py

* Fri May 03 2013 Jakub Filak <jfilak@redhat.com> 0.2.12-1
- Use 'N/A' instead of ??
- Use package name is neither component nor executable items are available
- Don't try to select a problem if the list is empty
- Catch InvalidProblem exception in sort function
- Handle DBus initialization errors gracefully
- Show HTML titles of URLs from reported_to element
- Updated translation
- Continue in handling of SIGCHLD after the first one is handled
- Fix two comma splices
- Fix wrong dialog flag names

* Mon Apr 22 2013 Jakub Filak <jfilak@redhat.com> 0.2.11-1
- Enable pylint check only on Fedora
- Fix bogus dates in chagelog
- Introduce expert mode and show 'Analyze' button in that mode
- Use last occurrence item for problems sorting
- Fix broken keyboard shortcuts
- Fix missing space typo - Martin Milata <mmilata@redhat.com>
- Compare all DesktopEntry.*() return values to None
- Display 'component' name instead of 'executable' if desktop file is missing
- Do not show scrollbar for long links
- Allow to disable pylint check in configure.ac
- Move manpage to volume 1 - Chris Lockfort <clockfort@csh.rit.edu>
- Move gnome_abrt module check to module's Makefile
- Disable 'Interface not implemented' pylint warning
- Configure pylint to produce parseable output

* Tue Apr  9 2013 Jakub Filak <jfilak@redhat.com> 0.2.10-2
- Make check only on fedora

* Wed Mar 27 2013 Jakub Filak <jfilak@redhat.com> 0.2.10-1
- Add the report dialog to the menu
- Add 'Report problem with ABRT' dialog
- Add VERSION and PACKAGE attributes to gnome_abrt module
- Rename attribute in errors.InvalidProblem
- Use IOChannel approach in order to make signal handling synchronous
- Add all python Requires to BuildRequires because of pylint
- Replace GNU style make pattern rules by implicit rules
- Remove left-over RELEASE varible from configure.ac
- Recover from DBus errors while sending command line
- Catch more exceptions and handle them correctly
- Add pylint check and fix problems uncoverend by pylint
- Filter out empyt strings from splitted cmdline
- Fix sytanx error
- Change the label "No oopses" to "No problems detected"
- Get rid of scrollbar around the text on the bottom of window in default size
- Fix appearance of scrolled widgets to no longer have white background
- Remove leftover shebang from non-executable script

* Mon Mar 18 2013 Jakub Filak <jfilak@redhat.com> 0.2.9-1
- Truncate long texts with ellipsis instead of auto-adjusting of window width
- Add a popopup menu for list of problems
- Use executable's basename as an application name instead of the full path
- Remove invalid problems from GUI tree view list
- Remove invalid problems from the dbus cache
- Robustize the processing of newly occurred problems
- Remove a left-over usage of the window member in OopsApplication
- Handle reaching inotify max watches better
- Update translation
- Don't allow reporting if the problem is not reportable
- Suggest reporting a bug if it wasn't reported yet
- Simplify the glade file and add a widget for messages
- Refactorize the function rendering a problem data
- A workaround for the bug in remote GtkApplications
- Allow only a single instance of gnome-abrt
- Fix bugs in main window in handler of configuration updates
- Resolves: #919796, #922656, #920417

* Mon Feb 25 2013 Jakub Filak <jfilak@redhat.com> 0.2.8-1
- Try harder when looking for icon and don't cache weak results
- Make controller more robust against invalid arguments
- Check return value of the get selection function
- Require correct version of libreport
- Return an empty list instead of None from OopsWindow.get_selected()
- Return an empty list instead of None from get_problems() in case of DBus error
- Get rid of unnecessary variable from the directory source
- Add a cmd line argument for selected problem id

* Fri Feb 08 2013 Jakub Filak <jfilak@redhat.com> - 0.2.7-1
- Fix failure in processing of dump directories from user's home
- Resolves: #908712

* Tue Jan 08 2013 Jakub Filak <jfilak@redhat.com> - 0.2.6-1
- Require libreport version 2.0.20 and greater
- Use DD api correctly
- Reflect changes in libreport
- Resolves: #890357

* Wed Nov 28 2012 Jakub Filak <jfilak@redhat.com> - 0.2.5-1
- Add licenses to all files
- Refresh view's source if InvalidProblem exception is caught during GUI update
- Properly handle removal of the first and the last problem from the list
- Use right tree model in searching for problems
- Use theme backround color as background for the link buttons
- Make the links to servers less moving
- Keep user's selection even if a source has changed
- Destroy abrt-handle-event zombies

* Mon Nov 12 2012 Jakub Filak <jfilak@redhat.com> - 0.2.4-1
- Fix label fields size
- Assure ownership of reported problem
- Remove unnecessary GtkEventBox
- Fix appearance of link button widget to no longer have a white background
- Update translations

* Fri Oct 05 2012 Jakub Filak <jfilak@redhat.com> - 0.2.3-1
- Generate version
- Add GNOME3 application menu
- Use correct D-Bus path to listen on for Crash signal
- Make path to abrt-handle-event configurable
- Fix a bug in running of subprocesses
- Refactorize directory problems implementation
- Don't print weired debug message
- Don't show the 'reconnecting to dbus' warning
- Don't show new root's crashes by default
- Fix indentation

* Fri Sep 21 2012 Jakub Filak <jfilak@redhat.com> - 0.2.2-1
- Lazy initialization of directory source
- Don't utilize CPU for 99%
- Code refactorization
- Add translation from the ABRT project
- Properly log exceptions
- Delete directory problems marked as invalid after refresh in inotify handler
- Declare directory problems deleted if its directory doesn't exist
- Fix indentation bug in icon look up algorithm
- Add --verbose command line argument
- Add directory name to error messages

* Mon Sep 17 2012 Jakub Filak <jfilak@redhat.com> - 0.2.1-4
- Fix a problem with desktop items without icons
- A bit better handling of uncaght exceptions

* Mon Sep 17 2012 Jakub Filak <jfilak@redhat.com> - 0.2.1-3
- Add cs and et translations

* Fri Sep 14 2012 Jakub Filak <jfilak@redhat.com> - 0.2.1-2
- Fixed problem with selection of problem after start up
- Corrected application icon look up algorithm
- Fixed problem with missing problems directory

* Fri Sep 14 2012 Jakub Filak <jfilak@redhat.com> - 0.2.1-1
- Detail button replaced by list of reported_to links
- Improved look (margins, icons, wider window by default)
- Implemented multiple delete
- Changed window tiple
- Double click and keyboard shortcuts

* Thu Sep 06 2012 Jakub Filak <jfilak@redhat.com> - 0.2-9
- Remove noarch because of binary wrappers
- Added support for adjusting libreport preferences

* Tue Aug 28 2012 Jakub Filak <jfilak@redhat.com> - 0.2-8
- Take ownership of all installed directories
- Correct paths to translated files

* Mon Aug 27 2012 Jakub Filak <jfilak@redhat.com> - 0.2-7
- Dropped versions from requires
- Simplified spec
- Removed pylint check from configure.ac
- Whitespace cleanup (rmarko@redhat.com)

* Fri Aug 24 2012 Jakub Filak <jfilak@redhat.com> - 0.2-6
- Use own icons set

* Fri Aug 24 2012 Jakub Filak <jfilak@redhat.com> - 0.2-5
- Reorganize source files
- Get rid of all rpmlint complaints

* Thu Aug 23 2012 Jakub Filak <jfilak@redhat.com> - 0.2-4
- Update GUI on various signals (new problem, problem changed, etc.)
- Sort problems by time in descending order
- Correct internationalization in date string generator

* Wed Aug 15 2012 Jakub Filak <jfilak@redhat.com> - 0.2-3
- Reconnect to DBus bus
- Default values for missing items
- Correct field for 'is_reported' flag

* Wed Aug 15 2012 Jakub Filak <jfilak@redhat.com> - 0.2-2
- Add missing files

* Wed Aug 15 2012 Jakub Filak <jfilak@redhat.com> - 0.2-1
- Problems filtering
- Errors handling
- Localization support

* Mon Aug 13 2012 Jakub Filak <jfilak@redhat.com> - 0.1-1
- Initial version
