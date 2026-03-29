import shutil
from pathlib import Path


class FileManager:
    """Dosya sistemi işlemlerini yöneten sınıf.
    Sadece dosya taşıma ve klasör oluşturma işlerinden sorumludur.
    """

    @staticmethod
    def ensure_directory(directory_path: str) -> None:
        """
        Belirtilen yoldaki klasörün var olduğundan emin olur, yoksa oluşturur.
        """
        path = Path(directory_path)
        path.mkdir(parents=True, exist_ok=True)

    def move_file(self, source_path: str, target_dir: str) -> str:
        """
        Dosyayı kaynak konumdan hedef klasöre güvenli bir şekilde taşır.
        İsim çakışması varsa dosya ismini otomatik olarak günceller.
        """
        source = Path(source_path)
        target_directory = Path(target_dir)

        if not source.exists() or not source.is_file():
            raise FileNotFoundError(f"Kaynak dosyası bulunamadı: {source_path}")

        self.ensure_directory(target_dir)
        target_path = self._generate_unique_filename(source, target_directory)

        shutil.move(str(source), str(target_path))

        return str(target_path)

    def _generate_unique_filename(self, source: Path, target_directory: Path) -> Path:
        """
        Hedef klasörde aynı isimde dosya varsa, benzersiz bir dosya adı üretir.
        """
        target_path = target_directory / source.name
        counter = 1

        while target_path.exists():
            new_name = f"{source.stem}_{counter}{source.suffix}"
            target_path = target_directory / new_name
            counter += 1

        return target_path
