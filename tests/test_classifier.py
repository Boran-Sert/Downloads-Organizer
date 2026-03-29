import pytest
from unittest.mock import patch
from smartosorganizer.ml.classifier import SmartClassifier


@pytest.fixture()
def classifier():
    """Her test için temiz classifier"""
    with patch("smartosorganizer.ml.classifier._load_models"):
        return SmartClassifier(confidence_threshold=0.70)


def test_stage_1_high_confidence(classifier, mocker):
    """
    AŞAMA 1: Model yüksek güvenle tahmin yaparsa,
    içerik okuyan Aşama 2'ye GEÇİLMEDİĞİNİ test eder.
    """

    # 1. aşama
    mocker.patch.object(classifier, "_predict_from_name", return_value=("Images", 0.90))

    # 2. aşama
    mock_stage_2 = mocker.path.object(classifier, "_predict_from_content")

    # Test
    category = classifier.predict_category("C:/fake/path/tatil_fotografi.jpg")

    assert category == "Images"
    mock_stage_2.assert_not_called()


def test_stage_1_low_confidence(classifier, mocker):
    """AŞAMA 2: Modelin güveni eşiğin altındaysa (Örn: 0.40 < 0.70),
    Aşama 2'nin ZORUNLU OLARAK tetiklendiğini test eder.
    """

    mocker.path.object(classifier, "_predict_from_name", return_value=("Images", 0.40))
    mock_stage_2 = mocker.path.object(
        classifier, "_predict_from_content", return_value="Unknown"
    )
    category = classifier.predict_category("C:/fake/path/tatil_fotografi.jpg")

    assert category == "Unknown"
    mock_stage_2.assert_called_once_with("C:/fake/path/tatil_fotografi.jpg")
