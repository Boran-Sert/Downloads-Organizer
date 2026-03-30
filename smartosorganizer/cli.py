import typer
from smartosorganizer.daemon import (
    start_daemon,
    stop_daemon,
    get_daemon_status,
    scan_all_directories,
)

# Typer uygulamasını başlat
app = typer.Typer(
    help="SmartOSOrganizer - Akıllı İşletim Sistemi Sınıflandırıcısı Komut Satırı Arayüzü",
    add_completion=False,  # Terminal otomatik tamamlama kurulumunu şimdilik kapalı tutuyoruz
)


@app.command()
def start():
    """Arka plan sınıflandırma hizmetini (daemon) başlatır."""
    typer.echo("SmartOSOrganizer başlatılıyor...")
    start_daemon()


@app.command()
def stop():
    """Arka plan sınıflandırma hizmetini (daemon) durdurur."""
    typer.echo("SmartOSOrganizer durduruluyor...")
    stop_daemon()


@app.command()
def status():
    """Arka plan sınıflandırma hizmetini (daemon) durumunu gösterir."""
    cur_status = get_daemon_status()
    typer.echo(f"Durum: {cur_status}")


@app.command()
def scan():
    """Geçmişte birikmiş tüm dosyaları tek seferde tarar ve düzenler."""
    typer.echo(
        "Geçmiş dosyalar taranıyor ve düzenleniyor. Dosya sayısına göre bu işlem biraz sürebilir..."
    )
    scan_all_directories()
    typer.echo(
        "Tarama ve düzenleme işlemi başarıyla tamamlandı! Masaüstün artık tertemiz."
    )


if __name__ == "__main__":
    app()
