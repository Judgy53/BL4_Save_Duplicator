import base64
import json
import utils
import urllib.request

VERSION_FILE_URL = "https://api.github.com/repos/Judgy53/BL4_Save_Duplicator/contents/version.txt"
__current_version: str | None = None
__latest_version: str | None = None
# __latest_version = "1.1.0"  # Temporary hardcoded latest version for testing

def get_current_version() -> str | None:
    """Get the current version of the application."""
    global __current_version
    if __current_version is not None:
        return __current_version
    try:
        with open(utils.resource_path("version.txt"), "r") as version_file:
            __current_version = version_file.read().strip()
            print(f"Current version: {__current_version}")
            return __current_version
    except Exception as e:
        print(f"Error reading current version: {e}")
        return None

def get_latest_version() -> str | None:
    """Fetch the latest version of the application from the remote URL."""
    global __latest_version
    if __latest_version is not None:
        return __latest_version
    try:
        with urllib.request.urlopen(VERSION_FILE_URL) as response:
            data = json.loads(response.read().decode())
            __latest_version = base64.b64decode(data['content']).decode().strip()
            print(f"Latest version: {__latest_version}")
            return __latest_version
    except Exception as e:
        print(f"Error fetching latest version: {e}")
        return None

def is_update_available() -> bool:
    """Check if an update is available by comparing current and latest versions."""
    current_version = get_current_version()
    latest_version = get_latest_version()
    if current_version and latest_version:
        return current_version != latest_version
    return False
