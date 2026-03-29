import pytest
from pathlib import Path
from smartosorganizer.core.file_manager import FileManager


@pytest.fixture
def file_manager():
    """Her test için temiz instance oluşturur"""
    return FileManager()


def test_ensure_directory_creates_folder_if_missing(tmp_path, file_manager):
    """Klasör yoksa file manager bunu oluşturur mu test eder"""
    target_dir = tmp_path / "Documents" / "PDF_Files"

    assert not target_dir.exists()

    file_manager.ensure_directory(str(target_dir))

    assert target_dir.exists()
    assert target_dir.is_dir()


def test_move_file_successfully(tmp_path, file_manager):
    """Dosyanın doğru bir şekilde taşınmasını kontrol eder"""
    source_dir = tmp_path / "Dowloands"
    target_dir = tmp_path / "Organized"
    source_dir.mkdir()
    target_dir.mkdir()

    test_file = source_dir / "test.txt"
    test_file.write_text("TEST")
    destination = file_manager.move_file(str(test_file), str(target_dir))

    assert not test_file.exists()
    assert Path(destination).exists()
    assert Path(destination).parent == target_dir


def test_move_file_handles_duplicate_names(tmp_path, file_manager):
    """Aynı isimde dosya varsa, isminin değiştirilerek taşındığını test eder."""
    source_dir = tmp_path / "Downloads"
    target_dir = tmp_path / "Organized"
    source_dir.mkdir()
    target_dir.mkdir()

    existing_file = target_dir / "report.docx"
    existing_file.write_text("old content")

    new_file = source_dir / "report.docx"
    new_file.write_text("new content")

    destination_path = file_manager.move_file(str(new_file), str(target_dir))

    assert existing_file.exists()
    assert Path(destination_path).exists()
    assert str(existing_file) != destination_path
    assert "report" in destination_path
