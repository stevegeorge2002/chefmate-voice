"""
ChefMate Voice - Translation Service
Real-time kitchen communication across languages
"""

import httpx
import json
from typing import Dict, List

class KitchenTranslator:
    """Multilingual kitchen communication"""
    
    def __init__(self, minimax_key=""):
        self.minimax_key = minimax_key
        
        # Supported languages in kitchen
        self.languages = {
            "en": "English",
            "es": "Spanish",
            "zh": "Mandarin Chinese",
            "fr": "French",
            "it": "Italian",
            "pt": "Portuguese",
            "vi": "Vietnamese",
            "ko": "Korean"
        }
        
        # Kitchen staff language preferences (would come from database)
        self.staff_languages = {
            "chef": "en",
            "sous_chef": "en",
            "line_cook_1": "es",
            "line_cook_2": "es",
            "prep_cook": "zh",
            "dishwasher": "zh",
            "server_1": "en",
            "server_2": "es"
        }
    
    async def translate_command(self, text: str, from_lang: str, to_langs: List[str]) -> Dict:
        """Translate kitchen command to multiple languages"""
        
        if not self.minimax_key:
            # Demo mode - return mock translations
            return self._demo_translate(text, from_lang, to_langs)
        
        # Real MiniMax translation
        translations = {}
        
        for target_lang in to_langs:
            if target_lang == from_lang:
                translations[target_lang] = text
                continue
            
            prompt = f"""Translate this restaurant kitchen command from {self.languages.get(from_lang, from_lang)} to {self.languages.get(target_lang, target_lang)}:

"{text}"

Rules:
1. Preserve kitchen terminology (fire, 86, pickup, etc.)
2. Keep table numbers and dish names clear
3. Maintain urgency and tone
4. Use professional kitchen language

Respond with ONLY the translation, no explanation."""

            try:
                async with httpx.AsyncClient(timeout=15) as client:
                    response = await client.post(
                        "https://api.minimax.chat/v1/text/chatcompletion_v2",
                        headers={
                            "Authorization": f"Bearer {self.minimax_key}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "model": "abab6-chat",
                            "messages": [{"role": "user", "content": prompt}],
                            "temperature": 0.3
                        }
                    )
                    
                    result = response.json()
                    translation = result['choices'][0]['message']['content'].strip()
                    translations[target_lang] = translation
                    
            except Exception as e:
                print(f"Translation error for {target_lang}: {e}")
                translations[target_lang] = text  # Fallback to original
        
        return translations
    
    def _demo_translate(self, text: str, from_lang: str, to_langs: List[str]) -> Dict:
        """Demo translations without API"""
        
        # Common kitchen phrases pre-translated
        demo_translations = {
            "Order fire table 5, two steaks medium-rare": {
                "en": "Order fire table 5, two steaks medium-rare",
                "es": "Orden fuego mesa 5, dos bistecs término medio",
                "zh": "开始烹饪5号桌，两份五分熟牛排",
                "fr": "Commande feu table 5, deux steaks saignants",
                "vi": "Bắt đầu bàn 5, hai miếng bít tết tái"
            },
            "Steak table 5 plated": {
                "en": "Steak table 5 plated",
                "es": "Bistec mesa 5 listo",
                "zh": "5号桌牛排已装盘",
                "fr": "Steak table 5 dressé",
                "vi": "Bít tết bàn 5 đã sẵn sàng"
            },
            "86 salmon": {
                "en": "86 salmon - sold out",
                "es": "86 salmón - agotado",
                "zh": "三文鱼售完",
                "fr": "86 saumon - épuisé",
                "vi": "Hết cá hồi"
            },
            "How long on table 3?": {
                "en": "How long on table 3?",
                "es": "¿Cuánto falta para mesa 3?",
                "zh": "3号桌还要多久？",
                "fr": "Combien de temps pour table 3?",
                "vi": "Còn bao lâu cho bàn 3?"
            }
        }
        
        # Find matching phrase or use original
        translations = demo_translations.get(text, {lang: text for lang in to_langs})
        
        # Return only requested languages
        return {lang: translations.get(lang, text) for lang in to_langs}
    
    async def broadcast_to_kitchen(self, speaker_role: str, message: str) -> Dict:
        """Broadcast message in all kitchen languages"""
        
        speaker_lang = self.staff_languages.get(speaker_role, "en")
        
        # Get all active languages in kitchen
        active_languages = list(set(self.staff_languages.values()))
        
        # Translate to all languages
        translations = await self.translate_command(
            message,
            from_lang=speaker_lang,
            to_langs=active_languages
        )
        
        # Create broadcast message for each role
        broadcasts = {}
        
        for role, pref_lang in self.staff_languages.items():
            broadcasts[role] = {
                "original_speaker": speaker_role,
                "message": translations[pref_lang],
                "language": pref_lang,
                "timestamp": datetime.now().isoformat()
            }
        
        return {
            "speaker": speaker_role,
            "original_message": message,
            "original_language": speaker_lang,
            "translations": translations,
            "broadcasts": broadcasts
        }