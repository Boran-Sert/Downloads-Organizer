import typer

from smartosorganizer.daemon import start_daemon, stop_daemon, get_daemon_status

# Typer uygulamasını başlat
app = typer.Typer(
    help="SmartOSOrganizer - Akıllı İşletim Sistemi Sınıflandırıcısı Komut Satırı Arayüzü",
    add_completion=False,  # Terminal otomatik tamamlama kurulumunu şimdilik kapalı tutuyoruz
)


@app.command
def start():
    """Arka plan sınıflandırma hizmetini (daemon) başlatır."""
    typer.echo("SmartOSOrganizer başlatılıyor...")
    start_daemon()


@app.command
def stop():
    """Arka plan sınıflandırma hizmetini (daemon) durdurur."""
    typer.echo("SmartOSOrganizer durduruluyor...")
    stop_daemon()


@app.command
def get_status():
    """Arka plan sınıflandırma hizmetini (daemon) durumunu gösterir."""
    cur_status = get_daemon_status
    typer.echo(f"Durum: {cur_status}")


if __name__ == "__main__":
    app()
