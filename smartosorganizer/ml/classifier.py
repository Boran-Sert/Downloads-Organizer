import joblib
from typing import Tuple
from pathlib import Path

from smartosorganizer.ml.feature_extractor import FeatureExtractor

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_MODELS_DIR = BASE_DIR / "models"


class SmartClassifier:
    """
    Dosyaları ismine, uzantısına ve gerektiğinde içeriğine bakarak sınıflandıran
    iki aşamalı Yapay Zeka karar modülü.
    """

    def __init__(self, confidence_threshold: float = 0.70, models_dir: str = None):
        self.confidence_threshold = confidence_threshold
        # Eğer dışarıdan özel bir yol verilmediyse, mutlak yolu kullan
        self.models_dir = Path(models_dir) if models_dir else DEFAULT_MODELS_DIR

        self.name_model = None
        self.content_model = None

        self._load_models()

    def _load_models(self) -> None:
        """Eğitilmiş scikit-learn modellerini belleğe yükler."""
        name_model_path = self.models_dir / "name_classifier.pkl"
        content_model_path = self.models_dir / "content_classifier.pkl"

        # Model dosyaları varsa yükle (Yoksa ilk kurulumda hata vermemesi için koruma)
        if name_model_path.exists():
            self.name_model = joblib.load(name_model_path)

        if content_model_path.exists():
            self.content_model = joblib.load(content_model_path)

    def predict_category(self, file_path: str) -> str:
        """Önce hızlı analiz (Aşama 1) yapar, emin olamazsa derin analize (Aşama 2) geçer."""
        category, confidence = self._predict_from_name(file_path)

        if confidence >= self.confidence_threshold:
            return category

        return self._predict_from_content(file_path)

    def _predict_from_name(self, file_path: str) -> Tuple[str, float]:
        """[Aşama 1] FeatureExtractor ile dosya adını temizler ve modele sorar."""
        if self.name_model is None:
            return ("Bilinmeyen", 0.0)

        filename = Path(file_path).name
        # 1. Özellik Çıkarımı: Örn: "fatura_2026.pdf" -> "fatura 2026 pdf"
        clean_text = FeatureExtractor.extract_from_name(filename)

        # 2. Model Tahmini (scikit-learn text pipeline'ları liste bekler)
        prediction = self.name_model.predict([clean_text])[0]

        # 3. Emin Olma Oranı (En yüksek olasılık değeri)
        probabilities = self.name_model.predict_proba([clean_text])[0]
        confidence = max(probabilities)

        return (prediction, float(confidence))

    def _predict_from_content(self, file_path: str) -> str:
        """[Aşama 2] Dosyanın içeriğini okur ve derin analiz modeline sorar."""
        if self.content_model is None:
            return "Bilinmeyen"

        path_obj = Path(file_path)
        extracted_text = ""

        suffix = path_obj.suffix.lower()

        # 1. Uzantıya göre METİN çıkarmayı dene
        if suffix == ".pdf":
            extracted_text = FeatureExtractor.extract_from_pdf(file_path)
        elif suffix in [".docx", ".doc"]:
            extracted_text = FeatureExtractor.extract_from_docx(file_path)
        elif suffix == ".pptx":
            extracted_text = FeatureExtractor.extract_from_pptx(file_path)
        elif suffix in [".png", ".jpg", ".jpeg"]:
            extracted_text = FeatureExtractor.extract_from_image(file_path)

        # 2. Eğer çıkarılan metin BOŞSA (veya çok kısaysa) yedek mantığı çalıştır
        if not extracted_text.strip() or len(extracted_text.strip()) < 5:
            # Sadece resim formatları için yüz taraması yap
            if suffix in [".png", ".jpg", ".jpeg"]:
                if FeatureExtractor.has_face(file_path):
                    return "Kisisel_Medya"
                else:
                    return "Diger/Resimler"

            # Resim dışındaki okunamayan (veya metinsiz) dosyalar
            return "Bilinmeyen"

        # 3. Metin başarıyla bulunduysa, eğitimli modelimize (Beyin) sor
        prediction = self.content_model.predict([extracted_text])[0]
        return prediction
