import sys
import os
import shutil
import tempfile
import zipfile
import urllib

SQLITE_ZIP_URL = "https://sqlite.org/2016/sqlite-dll-win32-x86-3150000.zip"

# Directory that this file sits in:
current_path = os.path.dirname(os.path.abspath(__file__))

# Directory of assets:
assets_dir = os.path.join(current_path,'assets')

def find_dlls_dir():
    """
    Find the directory equivalent to 'C:\python27\DLLs' at the current running
    python.
    """

    for pdir in sys.path:
        dll_path = os.path.join(pdir,'sqlite3.dll')
        pyd_path = os.path.join(pdir,'_sqlite3.pyd')
        if os.path.isfile(dll_path) and os.path.isfile(pyd_path):
            return pdir

    raise SetupError('DLLs dir was not found. Aborting.')


def copy_sqlite3_pyd():
    """
    Copy _sqlite3.pyd from python dlls dir into assets dir
    """
    # Make sure that the assets_dir exists:
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)

    python_dir = os.path.dirname(sys.executable)
    sqlite3_pyd_dest_path = os.path.join(assets_dir,'_sqlite3.pyd')
    # If the file already exists, we remove it:
    if os.path.isfile(sqlite3_pyd_dest_path):
        os.remove(sqlite3_pyd_dest_path)

    dlls_dir = find_dlls_dir()
    sqlite3_pyd_path = os.path.join(dlls_dir,'_sqlite3.pyd')
    shutil.copyfile(sqlite3_pyd_path,sqlite3_pyd_dest_path)

def download_sqlite3_dll():
    """
    Download sqlite3.dll from sqlite releases page, if it does not exist yet on
    the assets dir.
    """
    # Make sure that the assets_dir exists:
    if not os.path.exists(assets_dir):
        os.makedirs(assets_dir)

    sqlite3_dll_path = os.path.join(assets_dir,'sqlite3.dll')
    if os.path.isfile(sqlite3_dll_path):
        # sqlite3.dll is already there. Nothing to do here.
        return

    temp_dir = tempfile.mkdtemp()
    zip_path = os.path.join(temp_dir,'sqlite3.zip')
    urllib.urlretrieve(SQLITE_ZIP_URL,zip_path)
    extracted_dir = os.path.join(temp_dir,'extracted')
    os.makedirs(extracted_dir)
    zipfile.ZipFile(zip_path).extractall(extracted_dir)

    shutil.copyfile(os.path.join(extracted_dir,'sqlite3.dll'),
            sqlite3_dll_path)

    shutil.rmtree(temp_dir)
