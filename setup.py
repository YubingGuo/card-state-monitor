from distutils.core import setup
import py2exe
import sys
import os
sys.path.append(os.getcwd()+'\\src')

dist_dir = "bin"
csm_wx = dict(
    description = "Application used for HDBDE",
    script = "src/cardstate_app.py",
    icon_resources = [(1, "res/my_icon.ico")],
    dest_base = "CardStateMonitor")

    
setup(
    options = {"py2exe": {"compressed": 1,
                          "dist_dir": dist_dir,
                          "optimize": 2,
                          "ascii": 1,
                          "bundle_files": 3}},
    data_files = [("setting", ["setting/setting"]), ("res", ["res/my_icon.ico"])],
    zipfile = "lib/pylib.zip",
    windows = [csm_wx],
    )