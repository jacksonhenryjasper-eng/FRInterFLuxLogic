import os
import platform
import shutil
from pathlib import Path
from typing import Dict, List


KNOWN_APPS = {
    "chrome": ("Google Chrome", ["google-chrome", "google-chrome-stable", "Chrome"]),
    "firefox": ("Mozilla Firefox", ["firefox", "Firefox"]),
    "safari": ("Safari", ["Safari"]),
    "edge": ("Microsoft Edge", ["msedge", "Microsoft Edge"]),
    "canva": ("Canva", ["Canva"]),
    "minecraft": ("Minecraft", ["Minecraft", "minecraft-launcher"]),
    "slack": ("Slack", ["slack", "Slack"]),
    "notion": ("Notion", ["notion", "Notion"]),
}


def _mac_application_names() -> set[str]:
    if platform.system() != "Darwin":
        return set()

    application_dirs = [Path("/Applications"), Path.home() / "Applications"]
    return {
        item.stem.lower()
        for directory in application_dirs
        if directory.is_dir()
        for item in directory.glob("*.app")
    }


def scan_installed_apps() -> List[dict]:
    """Discover known local apps without launching or inspecting their data."""
    mac_apps = _mac_application_names()
    discovered: List[dict] = []

    for app_id, (name, executable_names) in KNOWN_APPS.items():
        executable = next(
            (shutil.which(candidate) for candidate in executable_names if shutil.which(candidate)),
            None,
        )
        installed = bool(executable) or name.lower() in mac_apps or app_id in mac_apps
        if installed:
            discovered.append(
                {
                    "id": app_id,
                    "name": name,
                    "source": "local_device",
                    "status": "discovered",
                    "connectable": True,
                    "capabilities": ["observe", "act"],
                }
            )

    return discovered


class AppRegistry:
    def __init__(self) -> None:
        self._apps: Dict[str, dict] = {}

    def scan(self) -> List[dict]:
        for app in scan_installed_apps():
            self._apps[app["id"]] = app
        return self.list_apps()

    def list_apps(self) -> List[dict]:
        return list(self._apps.values())


app_registry = AppRegistry()
