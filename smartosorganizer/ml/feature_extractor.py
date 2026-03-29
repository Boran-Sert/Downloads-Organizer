import fitz
from docx import Document


class FeatureExtractor:
    """
    Dosyalardan makine öğrenimi modelleri için anlamlı metin (özellik) çıkaran modül.
    """

    @staticmethod
    def extract_from_name(file_name: str) -> str:
        """
        Dosya adındaki özel karakterleri temizler ve NLP için kelimelere ayırır.
        Örn: '2026_Yillik_Finans-Raporu_v2.pdf' -> '2026 Yillik Finans Raporu v2 pdf'
        """
        clean_name = file_name.replace("_", " ").replace("-", " ").replace(".", " ")
        return " ".join(clean_name.split())

    @staticmethod
    def extract_from_pdf(file_path: str) -> str:
        """
        PyMuPDF kullanarak PDF dosyasının içeriğini okur ve tek bir metin olarak döndürür.
        """
        ex_text = []
        try:
            with fitz.open(file_path) as doc:
                for page in doc:
                    ex_text.append(page.get_text())
        except Exception:
            return ""

        return "".join(ex_text)

    @staticmethod
    def extract_from_docx(file_path: str) -> str:
        """
        python-docx kullanarak Word dosyasının içeriğini okur ve tek bir metin olarak döndürür.
        """
        ex_text = []
        try:
            doc = Document(file_path)
            for para in doc.paragraphs:
                ex_text.append(para.text)
        except Exception:
            return ""

        return "".join(ex_text)
