from typing import Tuple
from pathlib import Path


class SmartClassifier:
    """
    Dosyaları ismine, uzantısına ve gerektiğinde içeriğine bakarak sınıflandıran
    iki aşamalı Yapay Zeka karar modülü.
    """

    def __init__(self, confidence_threshold: float = 0.70):
        """
        Sınıflandırıcıyı başlatır ve modelleri belleğe yükler.
        :param confidence_threshold: 1. Aşamanın başarılı sayılması için gereken minimum emin olma oranı.
        """
        self.confidence_threshold = confidence_threshold
        self._load_models()

    def _load_models(self) -> None:
        """
        Eğitilmiş makine öğrenimi modellerini (scikit-learn, joblib vb.) belleğe yükler.
        Not: Testlerde bu metot mock'lanarak atlanır.
        """
        # TODO: joblib.load('models/name_classifier.pkl') vb. eklenecek.
        pass

    def predict_category(self, file_path: str) -> str:
        """
        Dosyayı analiz eder ve hedef kategoriyi (klasör adını) döndürür.
        Önce hızlı analiz (Aşama 1) yapar, emin olamazsa derin analize (Aşama 2) geçer.
        """
        # 1 aşama
        category, confidence = self._predict_from_name(file_path)

        if confidence >= self.confidence_threshold:
            return category

        return self._predict_from_content(file_path)

    def _predict_from_name(self, file_path: str) -> Tuple[str, float]:
        """
        [Aşama 1] Dosya adından ve uzantısından tahmin yapar.
        Dönüş: (Tahmin Edilen Kategori, Emin Olma Oranı 0.0 - 1.0)
        """
        # TODO: Gerçek ML modeli (Feature Extractor ile) buraya entegre edilecek.
        # Şimdilik testlerin geçmesi için soyut bir arayüz sunuyoruz.

        return ("Unknown", 0.0)

    def _predict_from_content(self, file_path: str) -> Tuple[str, float]:
        """
        [Aşama 2] Dosyanın içeriğini (PDF, DOCX metinleri) okuyarak tahmin yapar.
        Dönüş: Tahmin Edilen Kategori
        """
        # TODO: Feature Extractor ile metin okunup ML modeline sokulacak.
        return "Unknown"
