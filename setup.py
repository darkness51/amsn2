import sys, os
from cx_Freeze import setup, Executable

amsn2path = ""
if amsn2path == "":
  amsn2path = os.getcwd()

base = None
if sys.platform == "win32":
  base = "Win32GUI"

buildOptions = dict(
  optimize = 0, # 2 for max
  #includes = [],
  excludes = ["amsn2", #we'll copy
              "papyon", #those later...
              "PyQt4.phonon",
              "PyQt4.QAxContainer",
              "PyQt4.Qsci",
              "PyQt4.QtDeclarative",
              "PyQt4.QtDesigner",
              "PyQt4.QtHelp",
              "PyQt4.QtMultimedia",
              "PyQt4.QtNetwork",
              "PyQt4.QtOpenGL",
              "PyQt4.QtScript",
              "PyQt4.QtScriptTools",
              "PyQt4.QtSql",
              "PyQt4.QtSvg",
              "PyQt4.QtTest",
              "PyQt4.QtWebKit",
              "PyQt4.QtXml",
              "PyQt4.QtXmlPatterns",
             ],
  packages = ["OpenSSL", 
              "gzip", 
              "io", 
              "uuid", 
              "platform", 
              "xml.etree.ElementTree", 
              "xml.etree.cElementTree", 
              "xml.dom.minidom", 
              "Crypto.Util.randpool",
              "Crypto.Hash.HMAC",
              "Crypto.Hash.SHA",
              "Crypto.Cipher.DES3",
              "imghdr",
              "hmac",
              "gobject",
              "cgi",
              "Image",
              "sip",
              "PyQt4.QtCore",
              "PyQt4.QtGui",
              "PyQt4.Qt",
              "PyQqt4.uic"
            ],
  include_files = [(os.path.join(amsn2path, "amsn2"), "amsn2"),
                   (os.path.join(amsn2path, "papyon"), "papyon")
                  ],
  path = sys.path + [amsn2path],
  base = base
)

exe = Executable(
  script = os.path.join(amsn2path, "amsn2.py"),
  icon = None,
  compress = True,
  copyDependentFiles = True,
  appendScriptToLibrary = True
)

setup(
  name = "aMSN2",
  version = "0.1",
  description = "aMSN 0.1",
  options = dict(
    build_exe = buildOptions
  ),
  executables = [exe]
)
