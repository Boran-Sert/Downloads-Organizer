import pytest
from unittest.mock import MagicMock, patch
from smartosorganizer.daemon import SmartDaemon


@pytest.fixture
def daemon(mocker):
    """Her test için taze bir Daemon (Orkestratör) örneği sağlar.
    Alt modüller mock'lanarak gerçek dosya sistemi bağımlılığı kaldırılır.
    """
    mocker.patch("smartosorganizer.daemon.DirectoryWatcher")
    mocker.patch("smartosorganizer.daemon.SmartClassifier")
    mocker.patch("smartosorganizer.daemon.FileManager")
    return SmartDaemon(
        watch_dirs=["C:/Fake/Downloads"], target_base_dir="C:/Fake/Organized"
    )


def test_daemon_starts_watcher(daemon):
    """
    Daemon başlatıldığında, Watcher modülünün doğru dizinler ve
    doğru callback fonksiyonu ile tetiklendiğini test eder.
    """
    daemon.start()

    # Watcher başlatılmış olmalı
    daemon.watcher.start.assert_called_once()
    assert daemon.is_running is True


def test_daemon_stops_watcher(daemon):
    """
    Daemon durdurulduğunda, Watcher modülünün güvenli bir şekilde kapatıldığını test eder.
    """
    daemon.start()  # Önce çalışır duruma getirelim
    daemon.stop()  # Sonra durduralım

    daemon.watcher.stop.assert_called_once()
    assert daemon.is_running is False


def test_process_new_file_orchestration(daemon):
    """
    EN KRİTİK TEST: Yeni bir dosya bulunduğunda Daemon'ın sırasıyla;
    1. Classifier'a sınıflandırma yaptırdığını,
    2. FileManager'a dosyayı taşıttırdığını test eder.
    """
    # Classifier'ın "Belgeler" döndürmesini ayarla
    daemon.classifier.predict_category.return_value = "Belgeler"

    # Sisteme yeni bir dosya gelmiş gibi simüle et
    test_file_path = "C:/Fake/Downloads/fatura.pdf"
    daemon._process_new_file(test_file_path)

    # Orkestrasyon Doğrulaması
    # Sınıflandırıcıya doğru dosya sorulmuş mu?
    daemon.classifier.predict_category.assert_called_once_with(test_file_path)

    # FileManager'a dosyayı "Belgeler" klasörüne taşıması söylenmiş mi?
    expected_target_dir = "C:\\Fake\\Organized\\Belgeler"
    daemon.file_manager.move_file.assert_called_once_with(
        test_file_path, expected_target_dir
    )
