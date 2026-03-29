import pytest
from smartosorganizer.daemon import SmartDaemon


@pytest.fixture
def daemon():
    """Her test için taze bir Daemon (Orkestratör) örneği sağlar."""
    return SmartDaemon(
        watch_dirs=["C:/Fake/Downloads"], target_base_dir="C:/Fake/Organized"
    )


def test_daemon_starts_watcher(daemon, mocker):
    """
    Daemon başlatıldığında, Watcher modülünün doğru dizinler ve
    doğru callback fonksiyonu ile tetiklendiğini test eder.
    """
    mock_watcher_class = mocker.patch("smartosorganizer.daemon.DirectoryWatcher")
    mock_watcher_instance = mock_watcher_class.return_value

    daemon.start()

    # Watcher başlatılmış olmalı
    mock_watcher_instance.start.assert_called_once()
    assert daemon.is_running is True


def test_daemon_stops_watcher(daemon, mocker):
    """
    Daemon durdurulduğunda, Watcher modülünün güvenli bir şekilde kapatıldığını test eder.
    """
    mock_watcher_class = mocker.patch("smartosorganizer.daemon.DirectoryWatcher")
    mock_watcher_instance = mock_watcher_class.return_value

    daemon.start()  # Önce çalışır duruma getirelim
    daemon.stop()  # Sonra durduralım

    mock_watcher_instance.stop.assert_called_once()
    assert daemon.is_running is False


def test_process_new_file_orchestration(daemon, mocker):
    """
    EN KRİTİK TEST: Yeni bir dosya bulunduğunda Daemon'ın sırasıyla;
    1. Classifier'a sınıflandırma yaptırdığını,
    2. FileManager'a dosyayı taşıttırdığını test eder.
    """
    # 1. Classifier'ı mock'la ve "Belgeler" kategorisi dönecek şekilde ayarla
    mock_classifier_class = mocker.patch("smartosorganizer.daemon.SmartClassifier")
    mock_classifier_instance = mock_classifier_class.return_value
    mock_classifier_instance.predict_category.return_value = "Belgeler"

    # 2. FileManager'ı mock'la
    mock_fm_class = mocker.patch("smartosorganizer.daemon.FileManager")
    mock_fm_instance = mock_fm_class.return_value

    # 3. Sisteme yeni bir dosya gelmiş gibi simüle et
    test_file_path = "C:/Fake/Downloads/fatura.pdf"
    daemon._process_new_file(test_file_path)

    # 4. Orkestrasyon Doğrulaması (Sıralama ve Parametreler)
    # Sınıflandırıcıya doğru dosya sorulmuş mu?
    mock_classifier_instance.predict_category.assert_called_once_with(test_file_path)

    # FileManager'a dosyayı "Belgeler" klasörüne taşıması söylenmiş mi?
    expected_target_dir = "C:/Fake/Organized/Belgeler"
    mock_fm_instance.move_file.assert_called_once_with(
        test_file_path, expected_target_dir
    )
