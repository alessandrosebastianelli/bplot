"""
Build the distribution
"""
import shutil
import os


# Clean dist folder
shutil.rmtree(f'./build/', ignore_errors=True)
shutil.rmtree(f'./dist/', ignore_errors=True)
shutil.rmtree(f'./pyosv.egg-info/', ignore_errors=True)

# Build distribuition
os.system("python build_doc.py")
os.system("python setup.py sdist bdist_wheel")
os.system(f"python -m twine upload dist{os.sep}* --verbose")