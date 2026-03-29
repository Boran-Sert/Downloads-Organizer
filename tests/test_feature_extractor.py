import pytest
from unittest.mock import MagicMock
from smartosorganizer.ml.feature_extractor import FeatureExtractor


@pytest.fixture
def extractor():
    """Her test için temix extractor sağlar"""
    return FeatureExtractor


def test_extractor_from_name(extractor):
    """
    Dosya adından ve uzantısından anlamsız karakterlerin (alt çizgi vb.)
    temizlenip düzgün bir metin çıkarıldığını test eder.
    """
    file_name = "2026_Yillik_Finans_Raporu_v2.pdf"
    features = extractor.extract_from_name(file_name)

    assert "2026_Yillik_Finans_Raporu_v2.pdf" in features
    assert "pdf" in features


def test_extract_from_pdf(extractor, mocker):
    """
    PDF içeriğinin PyMuPDF (fitz) kütüphanesi kullanılarak
    doğru okunduğunu test eder.
    """

    mock_fitz = mocker.patch("smartosorganizer.ml.feature_extractor.fitz.open")
    mock_page = MagicMock()
    mock_page.get_text.return_value = "Mock PDF"

    mock_doc = MagicMock()
    mock_doc.__iter__.return_value = [mock_page]
    mock_fitz.return_value.__enter__.return_value = mock_doc

    text = extractor.extract_from_pdf("fake/path/test.pdf")
    assert "Mock PDF" in text
    mock_fitz.assert_called_once_with("fake/path/test.pdf")


def test_extract_from_docx(extractor, mocker):
    """
    DOCX içeriğinin python-docx kütüphanesi kullanılarak
    doğru okunduğunu test eder.
    """
    # Gerçek docx kütüphanesini mock'luyoruz
    mock_document_class = mocker.patch("smartosorganizer.ml.feature_extractor.Document")

    # Sahte paragraflar oluştur
    mock_doc_instance = MagicMock()
    mock_para1 = MagicMock()
    mock_para1.text = "İlk paragraf."
    mock_para2 = MagicMock()
    mock_para2.text = "İkinci paragraf."

    mock_doc_instance.paragraphs = [mock_para1, mock_para2]
    mock_document_class.return_value = mock_doc_instance

    text = extractor.extract_from_docx("fake/path/test.docx")

    assert "İlk paragraf." in text
    assert "İkinci paragraf." in text
    mock_document_class.assert_called_once_with("fake/path/test.docx")
