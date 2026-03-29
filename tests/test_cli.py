from typer.testing import CliRunner

from smartosorganizer.cli import app

runner = CliRunner()


def test_cli_star_command(mocker):
    """
    'start' komutunun doğru mesajı verip, arka plan hizmetini tetiklediğini test eder.
    """

    mock_start = mocker.patch("smartosorganizer.cli.start_daemon")
    result = runner.invoke(app, ["start"])

    assert result.exit_code == 0
    assert "SmartOSOrganizer başlatılıyor..." in result.stdout
    mock_start.assert_called_once()


def test_cli_stop_command(mocker):
    """
    'stop' komutunun hizmeti durdurma fonksiyonunu tetiklediğini test eder.
    """
    mock_stop = mocker.patch("smartosorganizer.cli.stop_daemon")

    result = runner.invoke(app, ["stop"])

    assert result.exit_code == 0
    assert "SmartOSOrganizer durduruluyor" in result.stdout
    mock_stop.assert_called_once()


def test_cli_status_command(mocker):
    """
    'status' komutunun arka plan hizmetinin durumunu doğru gösterdiğini test eder.
    """
    mock_status = mocker.patch(
        "smartosorganizer.cli.get_daemon_status", return_value="Çalışıyor"
    )

    result = runner.invoke(app, ["status"])

    assert result.exit_code == 0
    assert "Durum: Çalışıyor" in result.stdout
    mock_status.assert_called_once()
