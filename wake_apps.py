"""
Despierta apps de Streamlit Cloud que se hayan dormido por inactividad.
Visita cada URL con un navegador real (Playwright), y si encuentra
el botón "Yes, get this app back up!", lo toca.
"""
import sys
from playwright.sync_api import sync_playwright

# Agregá acá las URLs de tus apps de Streamlit
APP_URLS = [
    "https://rkuahz8wvydknjkyfdcxsy.streamlit.app/",
    "https://fermvhdmvspkxuvm3mroqi.streamlit.app/",
]

WAKE_BUTTON_TEXT = "Yes, get this app back up!"


def wake_app(page, url: str) -> str:
    print(f"\n--- Visitando: {url} ---")
    try:
        page.goto(url, timeout=60000, wait_until="domcontentloaded")
    except Exception as e:
        return f"ERROR al cargar la pagina: {e}"

    page.wait_for_timeout(5000)

    try:
        boton = page.get_by_text(WAKE_BUTTON_TEXT, exact=False)
        if boton.count() > 0:
            print("App dormida detectada. Tocando el boton de reactivar...")
            boton.first.click()
            page.wait_for_timeout(30000)
            return "OK - app estaba dormida, se toco el boton para despertarla."
        else:
            return "OK - app ya estaba despierta (no aparecio boton de reactivar)."
    except Exception as e:
        return f"ERROR buscando/tocando el boton: {e}"


def main():
    resultados = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        for url in APP_URLS:
            resultado = wake_app(page, url)
            print(resultado)
            resultados.append((url, resultado))
        browser.close()

    print("\n=== RESUMEN ===")
    hubo_error = False
    for url, resultado in resultados:
        print(f"{url} -> {resultado}")
        if resultado.startswith("ERROR"):
            hubo_error = True

    if hubo_error:
        sys.exit(1)


if __name__ == "__main__":
    main()
   
