import json
import os
from playwright.sync_api import sync_playwright
from processor import ProfileProcessor
from analytics import AnalyticsEngine
from ai_engine import AIEngine

def run_scraper(target_user, mode):
    processor = ProfileProcessor(target_user)
    
    with sync_playwright() as p:
        # headless=False para ver el proceso, cámbialo a True para producción
        browser = p.chromium.launch(headless=False)
        
        try:
            context = browser.new_context(storage_state="session.json")
        except Exception:
            print("❌ Error: session.json no encontrado o inválido.")
            browser.close()
            return

        page = context.new_page()

        def handle_response(response):
            url = response.url
            try:
                # Captura de datos de perfil y posts
                if "graphql" in url:
                    data = response.json()
                    processor.process_identity(data)
                    processor.process_feed_posts(data)
                    if "xdt_api__v1__clips__user__connection_v2" in url:
                        processor.process_reels_connection(data)
                
                # Captura de comentarios (Clave para Modo 2)
                elif "comments/" in url:
                    processor.process_comments(response.json())
                
                # Captura de info detallada (Likes/Plays de Reels)
                elif "/info/" in url:
                    processor.process_reel_info(response.json())
            except: 
                pass

        page.on("response", handle_response)
        
        print(f"🌐 Navegando al perfil de @{target_user}...")
        page.goto(f"https://www.instagram.com/{target_user}/")
        page.wait_for_timeout(4000)

        if mode == "1":
            print("📊 Modo 1: Ejecutando Deep Analytics (Posts vs Reels)...")
            # Scroll para capturar posts del feed
            for _ in range(5):
                if len(processor.posts) >= 10: break
                page.mouse.wheel(0, 1500)
                page.wait_for_timeout(2000)
            
            # Navegación a pestaña Reels para métricas de video
            page.goto(f"https://www.instagram.com/{target_user}/reels/")
            page.wait_for_timeout(3000)
            reel_links = page.locator("a[href*='/reel/']").all()
            for i in range(min(10, len(reel_links))):
                reel_links[i].click(force=True)
                page.wait_for_timeout(2500)
                page.keyboard.press("Escape")
                page.wait_for_timeout(800)

        else:
            print("🔍 Modo 2: Ejecutando Auditoría de Comunidad (IA)...")
            # Selector más robusto para los cuadros de la cuadrícula
            post_links = page.locator("a[href*='/p/'], a[href*='/reel/']").all()
            
            # Limitamos a 12 para la auditoría
            for i in range(min(12, len(post_links))):
                print(f"   💬 Abriendo publicación {i+1}/12 para extraer comentarios...")
                try:
                    post_links[i].click(force=True)
                    page.wait_for_timeout(3500) # Tiempo suficiente para que el JSON de comments cargue
                    page.keyboard.press("Escape")
                    page.wait_for_timeout(1000)
                except:
                    print(f"   ⚠️ No se pudo abrir la publicación {i+1}")

        # Empaquetado de resultados
        resultado = {
            "perfil": processor.profile_info,
            "posts": processor.posts,
            "reels": processor.reels,
            "comunidad_audit": processor.all_comments if mode == "2" else []
        }

        # Procesamiento con IA (Groq)
        ai_analysis = None
        if mode == "2" and processor.all_comments:
            print("\n🤖 Procesando comentarios con Llama 3.3 (Groq)...")
            try:
                ai = AIEngine()
                ai_analysis = ai.analyze_comments(processor.all_comments)
                resultado["ai_insight"] = ai_analysis
            except Exception as e:
                print(f"❌ Error al conectar con Groq: {e}")

        # Guardado en archivo local
        filename = f"data_{target_user}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(resultado, f, indent=4, ensure_ascii=False)
        print(f"✅ Datos guardados en {filename}")

        browser.close()
        
        # --- SECCIÓN DE REPORTES ---
        if mode == "1":
            # Reporte estándar de Analytics
            engine = AnalyticsEngine(resultado)
            engine.generate_report()
        else:
            # Reporte específico de Auditoría para el Modo 2
            print(f"\n📝 AUDITORÍA DE COMUNIDAD: @{processor.profile_info.get('username', target_user)}")
            print("-" * 50)
            print(f"👥 Seguidores: {processor.profile_info.get('followers', 0):,}")
            print(f"📑 Publicaciones analizadas: {len(processor.posts)}")
            print(f"💬 Total comentarios extraídos: {len(processor.all_comments)}")
            
            if ai_analysis:
                print(f"\n🧠 INSIGHTS DE INTELIGENCIA ARTIFICIAL:")
                print(f"   ● Sentimiento General: {ai_analysis.get('sentiment', 'N/A')}")
                print(f"   ● Temas Principales: {', '.join(ai_analysis.get('top_topics', []))}")
                print(f"   ● Vibe de la Comunidad: {ai_analysis.get('community_vibe', 'N/A')}")
                
                print("\n📌 MUESTRA DE COMENTARIOS:")
                for c in processor.all_comments[:5]:
                    is_ver = " [Verified] " if c.get('verified') else ""
                    print(f"   ➤ @{c['user']}{is_ver}: {c['text'][:80]}...")
            print("-" * 50)

if __name__ == "__main__":
    print("\n" + "="*30)
    print("🚀 IGMetricScraper v2.0")
    print("="*30)
    
    raw_user = input("Introduce el @usuario: ").strip()
    # Limpieza del arroba por si acaso
    target = raw_user[1:] if raw_user.startswith("@") else raw_user
    
    print("\nMODOS DISPONIBLES:")
    print("1. Deep Analytics (Comparativa Posts vs Reels)")
    print("2. Community Audit (Análisis de Sentimiento con IA)")
    
    opcion = input("\nSelecciona modo (1 o 2): ").strip()
    
    if opcion in ["1", "2"]:
        run_scraper(target, opcion)
    else:
        print("❌ Opción no válida. Saliendo...")