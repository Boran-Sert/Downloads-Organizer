import csv
import joblib
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from smartosorganizer.ml.feature_extractor import FeatureExtractor

# Proje kök dizinini mutlak yol olarak belirle (models/ klasörünün bir üstü)
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"


def train_name_classifier():
    """Aşama 1: Dosya isimlerinden kategori tahmin eden modeli eğitir."""
    print("Aşama 1: İsim Sınıflandırıcı eğitiliyor...")

    texts = []
    labels = []

    # Gerçek veri setimizi okuyoruz
    with open(DATA_DIR / "my_name_dataset.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # İsimleri temizleyerek (alt çizgi vb. silerek) listeye ekliyoruz
            clean_text = FeatureExtractor.extract_from_name(row["file_name"])
            texts.append(clean_text)
            labels.append(row["category"])

    # TF-IDF (Metinleri vektöre çevirir) ve LinearSVC (Hızlı ve güçlü sınıflandırıcı)
    # ngram_range=(1, 2) kelime öbeklerini de (örn: "finans raporu") yakalamayı sağlar.
    model = make_pipeline(
        TfidfVectorizer(ngram_range=(1, 2)), LogisticRegression(max_iter=1000)
    )
    model.fit(texts, labels)

    # Eğitilen modeli kaydet
    MODELS_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODELS_DIR / "name_classifier.pkl")
    print(
        "İsim Sınıflandırıcı başarıyla 'models/name_classifier.pkl' olarak kaydedildi!"
    )


def train_content_classifier():
    """Aşama 2: Dosya içeriklerinden (PDF/Word metni) kategori tahmin eden modeli eğitir."""
    print("Aşama 2: İçerik Sınıflandırıcı eğitiliyor...")

    texts = []
    labels = []

    with open(DATA_DIR / "my_content_dataset.csv", "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            texts.append(row["content"])
            labels.append(row["category"])

    model = make_pipeline(
        TfidfVectorizer(ngram_range=(1, 2)), LogisticRegression(max_iter=1000)
    )
    model.fit(texts, labels)

    joblib.dump(model, MODELS_DIR / "content_classifier.pkl")
    print(
        "İçerik Sınıflandırıcı başarıyla 'models/content_classifier.pkl' olarak kaydedildi!\n"
    )


if __name__ == "__main__":
    print("SmartOSOrganizer Makine Öğrenimi Eğitim Süreci Başlıyor...\n")

    # Önce veri setinin var olduğundan emin olalım
    if not (DATA_DIR / "my_name_dataset.csv").exists():
        print(f"HATA: '{DATA_DIR / 'my_name_dataset.csv'}' dosyası bulunamadı!")
        exit(1)

    train_name_classifier()
    train_content_classifier()
    print("Tüm modeller başarıyla eğitildi ve sisteme entegre edilmeye hazır!")
