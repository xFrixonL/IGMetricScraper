import json
import os
import time
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class AIEngine:
    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        self.model = "llama-3.3-70b-versatile"
        
        if not self.api_key:
            raise ValueError("❌ ERROR: GROQ_API_KEY no encontrada en el archivo .env")
            
        self.client = Groq(api_key=self.api_key)

    def analyze_comments(self, comments_list):
        if not comments_list:
            return {"sentiment": "N/A", "top_topics": [], "community_vibe": "Sin comentarios"}

        formatted_comments = "\n".join([f"- {c['text']}" for c in comments_list])
        
        prompt = f"""
        Analiza el sentimiento y los temas de estos comentarios de Instagram.
        
        COMENTARIOS:
        {formatted_comments}
        
        Responde ESTRICTAMENTE en formato JSON con la siguiente estructura:
        {{
            "sentiment": "Positivo/Negativo/Neutral",
            "top_topics": ["tema1", "tema2", "tema3"],
            "community_vibe": "breve descripción de la actitud del público"
        }}
        """

        retries = 3
        while retries > 0:
            try:
                completion = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": "Eres un experto en social media listening y análisis de sentimiento. Solo respondes en JSON."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.2,
                    response_format={"type": "json_object"}
                )
                return json.loads(completion.choices[0].message.content)
            
            except Exception as e:
                if "429" in str(e):
                    print(f"⚠️ Límite de Groq alcanzado. Esperando 20s... (Reintentos: {retries})")
                    time.sleep(20)
                    retries -= 1
                else:
                    print(f"❌ Error inesperado en IA: {e}")
                    return {"sentiment": "Error", "top_topics": [], "community_vibe": str(e)}
        
        return {"sentiment": "Timeout", "top_topics": [], "community_vibe": "No se pudo procesar tras reintentos."}