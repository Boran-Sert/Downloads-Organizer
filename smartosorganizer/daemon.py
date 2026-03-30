from pathlib import Path
from typing import List, Optional

from smartosorganizer.core.watcher import DirectoryWatcher
from smartosorganizer.core.file_manager import FileManager
from smartosorganizer.ml.classifier import SmartClassifier


class SmartDaemon:
    """
    Sistemin ana orkestratörü. Modüller arası iletişimi sağlar.
    Kendi başına iş yapmaz, doğru zamanda doğru modüle emir verir.
    """

    def __init__(self, watch_dirs: List[str], target_base_dir: str):
        self.watch_dirs = watch_dirs
        self.target_base_dir = Path(target_base_dir)
        self.is_running = False

        self.classifier = SmartClassifier()
        self.file_manager = FileManager()

        self.watcher = DirectoryWatcher(
            directories=self.watch_dirs, on_file_detected=self._process_new_file
        )

    def start(self) -> None:
        """Hizmeti ve dosya dinleyicisini başlatır."""
        if not self.is_running:
            self.watcher.start()
            self.is_running = True

    def stop(self) -> None:
        """Hizmeti ve dosya dinleyicisini güvenli bir şekilde durdurur."""
        if self.is_running:
            self.watcher.stop()
            self.is_running = False

    def scan_directories(self) -> None:
        """
        İzlenen dizinlerde (Masaüstü, İndirilenler vb.) halihazırda bulunan
        tüm eski dosyaları tarar ve sınıflandırma sürecine sokar.
        """
        for watch_dir in self.watch_dirs:
            dir_path = Path(watch_dir)

            if not dir_path.exists():
                continue

            for file_path in dir_path.iterdir():
                if file_path.is_file():
                    self._process_new_file(str(file_path))

    def _process_new_file(self, file_path: str) -> None:
        """Watcher veya tarayıcı yeni dosya bulduğunda burası tetiklenir."""
        try:
            category = self.classifier.predict_category(file_path)
            target_dir = self.target_base_dir / category
            self.file_manager.move_file(file_path, str(target_dir))

        except PermissionError:
            # WinError 32: Dosya o an başka bir programda açıksa programı çökertme, sessizce atla.
            print(f"Uyarı: '{Path(file_path).name}' şu anda açık olduğu için atlandı.")

        except Exception as e:
            # Olası diğer beklenmedik hataları yakala ve arka plan hizmetinin çökmesini engelle.
            print(f"Hata: '{Path(file_path).name}' işlenirken bir sorun oluştu -> {e}")


_active_daemon: Optional[SmartDaemon] = None


def start_daemon() -> None:
    """CLI 'start' komutu tarafından çağrılır."""
    global _active_daemon
    if _active_daemon is None:
        user_home = Path.home()
        downloads_dir = str(user_home / "Downloads")
        desktop_dir = str(user_home / "Desktop")
        organized_dir = str(user_home / "SmartOrganizer")

        _active_daemon = SmartDaemon(
            watch_dirs=[downloads_dir, desktop_dir], target_base_dir=organized_dir
        )
        _active_daemon.start()


def stop_daemon() -> None:
    """CLI 'stop' komutu tarafından çağrılır."""
    global _active_daemon
    if _active_daemon is not None:
        _active_daemon.stop()
        _active_daemon = None


def get_daemon_status() -> str:
    """CLI 'status' komutu tarafından çağrılır."""
    if _active_daemon and _active_daemon.is_running:
        return "Çalışıyor"
    return "Durduruldu"


def scan_all_directories() -> None:
    """CLI 'scan' komutu tarafından çağrılır. Geriye dönük toplu tarama yapar."""
    user_home = Path.home()
    downloads_dir = str(user_home / "Downloads")
    desktop_dir = str(user_home / "Desktop")
    organized_dir = str(user_home / "SmartOrganizer")

    scanner_daemon = SmartDaemon(
        watch_dirs=[downloads_dir, desktop_dir], target_base_dir=organized_dir
    )
    scanner_daemon.scan_directories()
