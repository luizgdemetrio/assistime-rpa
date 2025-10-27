# src/app.py
import os
from dotenv import load_dotenv, find_dotenv
import typer

# IMPORTS DO PROJETO
from src.browser import get_playwright_context
from src.flows.login_flow import do_login

# dentro do login_cmd (logo no início):
env_path = find_dotenv(filename=".env", usecwd=True)
# opcional de debug: print qual .env foi usado
print(f"Usando .env: {env_path}")  # pode remover depois

load_dotenv(dotenv_path=env_path, override=True)  # <<< força sobrescrever

app = typer.Typer(help="CLI do Assist Me RPA")  # <<< app COM SUBCOMANDOS

# --- NÃO use @app.callback aqui. NÃO use typer.run(...). --- #


@app.command("login")
def login_cmd(
    headless: bool = typer.Option(False, help="Roda em headless"),
    base_url: str = typer.Option(None, help="URL da tela de login (sobrepõe .env)"),
):
    """
    Realiza o login na plataforma Assist Me.
    """
    load_dotenv(find_dotenv())

    base = base_url or os.getenv("ASSISTME_BASE_URL")
    user = os.getenv("ASSISTME_USER")
    pwd = os.getenv("ASSISTME_PASS")

    missing = [
        k
        for k, v in {
            "ASSISTME_BASE_URL": base,
            "ASSISTME_USER": user,
            "ASSISTME_PASS": pwd,
        }.items()
        if not v
    ]
    if missing:
        typer.secho(
            "Variáveis ausentes: "
            + ", ".join(missing)
            + "\n→ Crie/complete o .env na raiz OU passe --base-url.",
            fg=typer.colors.RED,
        )
        raise typer.Exit(code=2)

    p, browser, context = get_playwright_context(headless=headless)
    try:
        page = context.new_page()
        do_login(page, base_url=base)
        typer.echo("✅ Login concluído.")
    finally:
        context.close()
        browser.close()
        p.stop()


if __name__ == "__main__":
    app()  # <<< importante: NADA de typer.run(...)
