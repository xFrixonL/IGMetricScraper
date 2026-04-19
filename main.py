import json
from playwright.sync_api import sync_playwright
from processor import ProfileProcessor
from analytics import AnalyticsEngine

def scrape_profile(target_user):
    processor = ProfileProcessor(target_user)
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        try:
            context = browser.new_context(storage_state="session.json")
        except:
            print("❌ Error: session.json no encontrado.")
            return

        page = context.new_page()

        def handle_response(response):
            url = response.url
            try:
                if "graphql" in url:
                    data = response.json()
                    processor.process_identity(data)
                    processor.process_feed_posts(data)
                    if "xdt_api__v1__clips__user__connection_v2" in url or "clips" in url:
                        processor.process_reels_connection(data)
                
                elif "/info/" in url:
                    processor.process_reel_info(response.json())
            except: pass

        page.on("response", handle_response)

        print(f"🚀 Obteniendo posts de @{target_user}...")
        page.goto(f"https://www.instagram.com/{target_user}/")
        
        for _ in range(5):
            if len(processor.posts) >= 10: break
            page.mouse.wheel(0, 1500)
            page.wait_for_timeout(2000)

        print(f"\n🎬 Entrando a pestaña Reels...")
        page.goto(f"https://www.instagram.com/{target_user}/reels/")
        page.wait_for_timeout(3000)

        reel_elements = page.locator("a[href*='/reel/']").all()
        for i in range(min(10, len(reel_elements))):
            current_reel_code = reel_elements[i].get_attribute("href").split("/")[-2]
            if target_user not in page.url:
                print(f"⚠️ Se desvió la navegación. Volviendo a @{target_user}...")
                page.goto(f"https://www.instagram.com/{target_user}/reels/")
                page.wait_for_timeout(2000)

            print(f"   🖱️ Abriendo modal para reel: {current_reel_code}")
            reel_elements[i].click(force=True)
            page.wait_for_timeout(2500) 
            page.keyboard.press("Escape")
            page.wait_for_timeout(800)

        resultado = {
            "perfil": processor.profile_info,
            "posts": processor.posts[:10],
            "reels": processor.reels[:10]
        }

        filename = f"data_{target_user}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(resultado, f, indent=4, ensure_ascii=False)

        print(f"\n✅ Completado. Datos en {filename}")
        browser.close()

    engine = AnalyticsEngine(resultado)
    engine.generate_report()

if __name__ == "__main__":
    scrape_profile("profile_username")  # Reemplaza con el nombre de usuario objetivo