from distutils.core import setup

import os
from glob import glob

if os.name == 'nt':
    import gobject
    import PyQt4
    import locale
    import py2exe

    version_id = "0.1"

    opts = {
        'py2exe': {
            'packages': ['amsn2'],
            'includes': ['locale', 'optparse', 'sip', 'gobject',
                         'PyQt4', 'PyQt4.QtCore', 'PyQt4.QtGui',
                         'os', 'Image',
                         'papyon', 'papyon.event', 'papyon.msnp2p'],
            'excludes': ["ltihooks", "gdk", 
                         "pywin.dialogs", "pywin.dialogs.list",
                         "Tkconstants","Tkinter","tcl",
                         "doctest","macpath","pdb",
                         "cookielib","ftplib","pickle",
                         "calendar","win32wnet","unicodedata"],
            'dll_excludes': ["libglade-2.0-0.dll", "w9xpopen.exe", "MSVCP90.dll"],
            'skip_archive': True,
            #'optimize': '2',
            'dist_dir': 'dist/',
        }
    }

    files = []
    #individual files
    #files.append( (".", ) )
    files.append( ("Microsoft.VC90.CRT", glob(r'c:\dev\ms-vc-runtime\*.*')) )

    setup(name="aMSN2",
      version=version_id,
      author="The aMSN2 Team",
      author_email="amsn-devel@lists.sourceforge.net",
      url="http://amsn-project.net",
      license="GNU General Public License version 2 (GPLv2)",
      requires = ['gobject', 'PyQt4'],
      windows=[{"script" : "amsn2.py"}],
      options=opts,
      data_files=files)

    print "Done! Files are here in dist/"
