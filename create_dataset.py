import csv
from pathlib import Path
from smartosorganizer.ml.feature_extractor import FeatureExtractor


def create_templates():
    user_home = Path.home()
    # Taranacak klasörler: Masaüstü ve İndirilenler
    directories = [user_home / "Desktop", user_home / "Downloads"]

    name_data = []
    content_data = []

    print(
        "Bilgisayarındaki dosyalar taranıyor, bu işlem PDF'lerin boyutuna göre biraz sürebilir..."
    )

    for directory in directories:
        if not directory.exists():
            continue

        for file_path in directory.iterdir():
            if not file_path.is_file():
                continue

            # 1. Aşama Modeli İçin: Tüm dosyaların isimlerini topla
            name_data.append(
                {
                    "file_name": file_path.name,
                    "category": "",  # Burası senin Excel'de dolduracağın yer
                }
            )

            # 2. Aşama Modeli İçin: Sadece PDF ve DOCX dosyalarının içeriklerini oku
            if file_path.suffix.lower() in [".pdf", ".docx", ".doc"]:
                text = ""
                try:
                    if file_path.suffix.lower() == ".pdf":
                        text = FeatureExtractor.extract_from_pdf(str(file_path))
                    else:
                        text = FeatureExtractor.extract_from_docx(str(file_path))
                except Exception:
                    pass  # Okunamayan dosyaları atla

                if text.strip():
                    # Dosyanın tamamı yerine sadece ilk 500 karakterini alıyoruz.
                    # Böylece sen CSV'ye bakıp anında "Ah bu vize notu" veya "Bu şirket faturası" diyebilirsin.
                    snippet = text.strip()[:500].replace("\n", " ")
                    content_data.append(
                        {
                            "file_name": file_path.name,
                            "content": snippet,
                            "category": "",
                        }
                    )

    # Verileri CSV olarak kaydet
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    # İsim Veri Setini Yazdır
    with open(data_dir / "my_name_dataset.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["file_name", "category"])
        writer.writeheader()
        writer.writerows(name_data)

    # İçerik Veri Setini Yazdır
    with open(
        data_dir / "my_content_dataset.csv", "w", newline="", encoding="utf-8"
    ) as f:
        writer = csv.DictWriter(f, fieldnames=["file_name", "content", "category"])
        writer.writeheader()
        writer.writerows(content_data)

    print(
        f"\nHarika! Toplam {len(name_data)} dosya ismi ve {len(content_data)} dosya içeriği çıkarıldı."
    )
    print(
        "Oluşturulan dosyalar: 'data/my_name_dataset.csv' ve 'data/my_content_dataset.csv'"
    )
    print(
        "Şimdi bu CSV dosyalarını Excel ile açıp boş olan 'category' (Okul, Is, Fatura vb.) sütunlarını doldurabilirsin!"
    )


if __name__ == "__main__":
    create_templates()
