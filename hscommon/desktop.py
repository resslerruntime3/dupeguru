# Created By: Virgil Dupras
# Created On: 2013-10-12
# Copyright 2015 Hardcoded Software (http://www.hardcoded.net)
#
# This software is licensed under the "GPLv3" License as described in the "LICENSE" file,
# which should be included with this package. The terms are also available at
# http://www.gnu.org/licenses/gpl-3.0.html

import os.path as op
import logging


class SpecialFolder:
    APPDATA = 1
    CACHE = 2


def open_url(url):
    """Open ``url`` with the default browser."""
    _open_url(url)


def open_path(path):
    """Open ``path`` with its associated application."""
    _open_path(str(path))


def reveal_path(path):
    """Open the folder containing ``path`` with the default file browser."""
    _reveal_path(str(path))


def special_folder_path(special_folder, appname=None, portable=False):
    """Returns the path of ``special_folder``.

    ``special_folder`` is a SpecialFolder.* const. The result is the special folder for the current
    application. The running process' application info is used to determine relevant information.

    You can override the application name with ``appname``. This argument is ingored under Qt.
    """
    return _special_folder_path(special_folder, appname, portable=portable)


try:
    # Normally, we would simply do "from cocoa import proxy", but due to a bug in pytest (currently
    # at v2.4.2), our test suite is broken when we do that. This below is a workaround until that
    # bug is fixed.
    import cocoa

    if not hasattr(cocoa, "proxy"):
        raise ImportError()
    proxy = cocoa.proxy
    _open_url = proxy.openURL_
    _open_path = proxy.openPath_
    _reveal_path = proxy.revealPath_

    def _special_folder_path(special_folder, appname=None, portable=False):
        if special_folder == SpecialFolder.CACHE:
            base = proxy.getCachePath()
        else:
            base = proxy.getAppdataPath()
        if not appname:
            appname = proxy.bundleInfo_("CFBundleName")
        return op.join(base, appname)

except ImportError:
    try:
        from PyQt5.QtCore import QUrl, QStandardPaths
        from PyQt5.QtGui import QDesktopServices
        from qtlib.util import get_appdata
        from core.util import executable_folder
        from hscommon.plat import ISWINDOWS, ISOSX
        import subprocess

        def _open_url(url):
            QDesktopServices.openUrl(QUrl(url))

        def _open_path(path):
            url = QUrl.fromLocalFile(str(path))
            QDesktopServices.openUrl(url)

        def _reveal_path(path):
            if ISWINDOWS:
                subprocess.run(["explorer", "/select,", op.abspath(path)])
            elif ISOSX:
                subprocess.run(["open", "-R", op.abspath(path)])
            else:
                _open_path(op.dirname(str(path)))

        def _special_folder_path(special_folder, appname=None, portable=False):
            if special_folder == SpecialFolder.CACHE:
                if ISWINDOWS and portable:
                    folder = op.join(executable_folder(), "cache")
                else:
                    folder = QStandardPaths.standardLocations(QStandardPaths.CacheLocation)[0]
            else:
                folder = get_appdata(portable)
            return folder

    except ImportError:
        # We're either running tests, and these functions don't matter much or we're in a really
        # weird situation. Let's just have dummy fallbacks.
        logging.warning("Can't setup desktop functions!")

        def _open_path(path):
            # Dummy for tests
            pass

        def _reveal_path(path):
            # Dummy for tests
            pass

        def _special_folder_path(special_folder, appname=None, portable=False):
            return "/tmp"
