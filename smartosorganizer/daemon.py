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

        # Alt modüllerin başlatılması (Composition)
        self.classifier = SmartClassifier()
        self.file_manager = FileManager()

        # Watcher'a "yeni dosya bulduğunda bu fonksiyonu çağır"
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

    def _process_new_file(self, file_path: str) -> None:
        """
        [KRİTİK İŞ AKIŞI] Watcher yeni dosya bulduğunda burası tetiklenir.
        1. Sınıflandırıcıya kategoriyi sorar.
        2. Hedef klasör yolunu oluşturur.
        3. Dosya yöneticisine taşıma emri verir.
        """
        # 1. Aşama: Yapay Zeka Kararı
        category = self.classifier.predict_category(file_path)

        # 2. Aşama: Hedef Dizin (Örn: C:/SmartOrganizer/Belgeler)
        target_dir = self.target_base_dir / category

        # 3. Aşama: Fiziksel Taşıma
        self.file_manager.move_file(file_path, str(target_dir))


# --- CLI ENTEGRASYONU İÇİN YARDIMCI FONKSİYONLAR ---

# Bellekte tek bir Daemon örneği (Singleton benzeri) tutmak için global değişken
_active_daemon: Optional[SmartDaemon] = None


def start_daemon() -> None:
    """CLI 'start' komutu tarafından çağrılır."""
    global _active_daemon
    if _active_daemon is None:
        # TODO: Şimdilik varsayılan kullanıcı yollarını alıyoruz (İleride config'e bağlanabilir)
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
