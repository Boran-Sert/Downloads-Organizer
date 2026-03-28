import pytest
from unittest.mock import MagicMock

# Henüz yazmadığımız ama TDD gereği arayüzünü (interface) test ettiğimiz sınıflar
from smartosorganizer.core.watcher import DirectoryWatcher, NewFileEventHandler


@pytest.fixture
def mock_callback():
    """Yeni dosya bulunduğunda tetiklenecek sahte (mock) fonksiyon."""
    return MagicMock()


@pytest.fixture
def watch_dirs(tmp_path):
    """pytest'in tmp_path özelliğini kullanarak geçici test klasörleri oluşturur."""
    downloads = tmp_path / "Downloads"
    desktop = tmp_path / "Desktop"
    downloads.mkdir()
    desktop.mkdir()
    return [str(downloads), str(desktop)]


def test_watcher_initialization(watch_dirs, mock_callback):
    """Watcher'ın doğru dizinler ve callback fonksiyonu ile başlatıldığını kontrol eder."""
    watcher = DirectoryWatcher(directories=watch_dirs, on_file_detected=mock_callback)

    assert watcher.directories == watch_dirs
    assert watcher.on_file_detected == mock_callback
    assert watcher.observer is not None


def test_watcher_start_and_stop(mocker, watch_dirs, mock_callback):
    """Watcher'ın watchdog observer'ı doğru şekilde başlatıp durdurduğunu test eder."""
    # watchdog kütüphanesindeki Observer sınıfını mock'luyoruz
    mock_observer_class = mocker.patch("smartosorganizer.core.watcher.Observer")
    mock_observer_instance = mock_observer_class.return_value

    watcher = DirectoryWatcher(directories=watch_dirs, on_file_detected=mock_callback)

    # Başlatma testi
    watcher.start()
    mock_observer_instance.start.assert_called_once()
    assert mock_observer_instance.schedule.call_count == len(watch_dirs)

    # Durdurma testi
    watcher.stop()
    mock_observer_instance.stop.assert_called_once()
    mock_observer_instance.join.assert_called_once()


def test_new_file_event_handler_triggers_callback(mock_callback):
    """Yeni bir DOSYA oluşturulduğunda callback fonksiyonunun tetiklendiğini test eder."""
    handler = NewFileEventHandler(callback=mock_callback)

    # Mock bir dosya oluşturma olayı (FileCreatedEvent taklidi)
    mock_event = MagicMock()
    mock_event.is_directory = False
    mock_event.src_path = "/fake/path/test_document.pdf"

    handler.on_created(mock_event)

    # Callback doğru dosya yoluyla tam olarak bir kez çağrılmış olmalı
    mock_callback.assert_called_once_with("/fake/path/test_document.pdf")


def test_new_file_event_handler_ignores_directories(mock_callback):
    """Oluşturulan şey bir KLASÖR ise uygulamanın bunu görmezden geldiğini test eder."""
    handler = NewFileEventHandler(callback=mock_callback)

    # Mock bir klasör oluşturma olayı
    mock_event = MagicMock()
    mock_event.is_directory = True
    mock_event.src_path = "/fake/path/new_folder"

    handler.on_created(mock_event)

    # Klasör olduğu için sınıflandırma callback'i KESİNLİKLE çağrılmamalı
    mock_callback.assert_not_called()
