from distutils.core import setup
import py2exe

dist_dir = "CardStateMonitor"
csm_wx = dict(
    description = "Application used for HDBDE",
    script = "cardstate_app.py",
#other_resources = [(RT_MANIFEST, 1, manifest_template % dict(prog="test_wx"))],
    icon_resources = [(1, "my_icon.ico")],
    dest_base = "CardStateMonitor")

    
setup(
    options = {"py2exe": {"compressed": 1,
                          "dist_dir": dist_dir,
                          "optimize": 2,
                          "ascii": 1,
                          "bundle_files": 3}},
    data_files = [("lib", ["setting"]), ("icon", ["my_icon.ico"])],
    zipfile = "lib/pylib.zip",
    windows = [csm_wx],
 
    )