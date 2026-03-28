"""
Directory Watcher Module - Dosya sistemi izleme
Watchdog kütüphanesi kullanarak belirtilen dizinlerdeki yeni dosyaları izler.
"""

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class NewFileEventHandler(FileSystemEventHandler):
    """Yeni dosya oluşturulduğunda callback tetikleyen event handler."""

    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    def on_created(self, event):
        """Yeni bir dosya veya klasör oluşturulduğunda çağrılır."""
        if not event.is_directory:
            self.callback(event.src_path)


class DirectoryWatcher:
    """Belirtilen dizinleri izleyerek yeni dosyaları tespit eden sınıf."""

    def __init__(self, directories, on_file_detected):
        self.directories = directories
        self.on_file_detected = on_file_detected
        self.observer = Observer()
        self._handler = NewFileEventHandler(callback=on_file_detected)

    def start(self):
        """Dizin izlemeyi başlatır."""
        for directory in self.directories:
            self.observer.schedule(self._handler, directory, recursive=False)
        self.observer.start()

    def stop(self):
        """Dizin izlemeyi durdurur."""
        self.observer.stop()
        self.observer.join()
