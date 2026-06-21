#!/usr/bin/env python3
"""File watcher that runs tests automatically on changes.

Usage:
    python .copilot/watch_tests.py

Monitors:
- tests/
- mailer/
- validators/

Runs pytest whenever a .py file changes.
"""

import os
import subprocess
import sys
import time
from typing import Set

WATCH_DIRS = ["tests", "mailer", "validators"]
WATCH_EXTENSIONS = [".py"]
DEBOUNCE_TIME = 1.0  # seconds


class FileWatcher:
    def __init__(self):
        self.watched_files: Set[str] = set()
        self.last_run = 0
        self.update_watched_files()

    def update_watched_files(self):
        """Scan and update list of watched files."""
        files = set()
        for watch_dir in WATCH_DIRS:
            if not os.path.exists(watch_dir):
                continue
            for root, dirs, filenames in os.walk(watch_dir):
                for fn in filenames:
                    if any(fn.endswith(ext) for ext in WATCH_EXTENSIONS):
                        files.add(os.path.join(root, fn))
        self.watched_files = files

    def get_mtimes(self) -> dict:
        """Get modification times of watched files."""
        mtimes = {}
        for fp in self.watched_files:
            if os.path.exists(fp):
                mtimes[fp] = os.path.getmtime(fp)
        return mtimes

    def has_changes(self, old_mtimes: dict, new_mtimes: dict) -> bool:
        """Check if any file has changed."""
        if len(old_mtimes) != len(new_mtimes):
            return True
        for fp, mtime in new_mtimes.items():
            if fp not in old_mtimes or old_mtimes[fp] != mtime:
                return True
        return False

    def run_tests(self):
        """Run pytest."""
        now = time.time()
        if now - self.last_run < DEBOUNCE_TIME:
            return
        self.last_run = now

        print("\n" + "=" * 60)
        print(f"⏱️  Zmiana wykryta o {time.strftime('%H:%M:%S')}")
        print("🧪 Uruchamiam pytest...")
        print("=" * 60 + "\n")

        cmd = [sys.executable, "-m", "pytest", "-q", "--tb=line"]
        result = subprocess.run(cmd)

        if result.returncode == 0:
            print("\n✅ Testy przeszły!")
        else:
            print("\n❌ Niektóre testy nie przeszły!")
        print("\n⏳ Czekam na następne zmiany...\n")

    def watch(self):
        """Watch for file changes."""
        mtimes = self.get_mtimes()

        print("\n" + "=" * 60)
        print("👁️  File Watcher uruchomiony")
        print(f"📁 Monitoruję: {', '.join(WATCH_DIRS)}")
        print(f"📊 Plików: {len(mtimes)}")
        print("⏳ Czekam na zmiany... (Ctrl+C aby wyjść)")
        print("=" * 60 + "\n")

        try:
            while True:
                new_mtimes = self.get_mtimes()
                if self.has_changes(mtimes, new_mtimes):
                    self.update_watched_files()
                    mtimes = self.get_mtimes()
                    self.run_tests()

                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n\n👋 Watcher wyłączony.")
            sys.exit(0)


if __name__ == "__main__":
    watcher = FileWatcher()
    watcher.watch()
