import os
from playwright.sync_api import sync_playwright

class SessionManager:
    def __init__(self, session_file="session.json"):
        self.session_file = session_file

    def save_session(self, context):
        context.storage_state(path=self.session_file)
        print(f"✅ Sesión guardada exitosamente en {self.session_file}")

    def load_session(self, browser):
        if os.path.exists(self.session_file):
            return browser.new_context(storage_state=self.session_file)
        return browser.new_context()

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        page.goto("https://www.instagram.com/")
        
        print("\n--- PASOS ---")
        print("1. Introduce tus credenciales en la ventana del navegador.")
        print("2. Si tienes 2FA (código al cel), introdúcelo.")
        print("3. Una vez veas tu muro (feed), el script detectará la sesión y se cerrará.\n")

        try:
            page.wait_for_selector("svg[aria-label='Inicio']", timeout=120000)
            page.wait_for_timeout(2000)
            
            manager = SessionManager()
            manager.save_session(context)
            
        except Exception as e:
            print(f"❌ Error o tiempo de espera agotado: {e}")
        
        finally:
            browser.close()