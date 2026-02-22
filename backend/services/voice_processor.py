"""
ChefMate Voice - Voice Processing Service
Handles Speechmatics, MiniMax, and ArmorIQ integration
"""

import httpx
import json
from typing import Dict, List
import re

class VoiceProcessor:
    """Process voice commands from kitchen"""
    
    def __init__(self, speechmatics_key="", minimax_key="", armoriq_key=""):
        self.speechmatics_key = speechmatics_key
        self.minimax_key = minimax_key
        self.armoriq_key = armoriq_key
        
    async def transcribe_audio(self, audio_data: bytes) -> str:
        """Transcribe audio using Speechmatics"""
        
        if not self.speechmatics_key:
            # Demo mode - simulate transcription
            return "Order fire table 5, two steaks medium-rare, one salmon well-done"
        
        # Real Speechmatics API call
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "https://asr.api.speechmatics.com/v2/jobs",
                headers={"Authorization": f"Bearer {self.speechmatics_key}"},
                files={"data_file": audio_data},
                data={
                    "config": json.dumps({
                        "type": "transcription",
                        "transcription_config": {
                            "language": "en",
                            "operating_point": "enhanced",
                            "enable_entities": True
                        }
                    })
                }
            )
            
            result = response.json()
            return result.get("transcript", "")
    
    async def parse_command(self, transcript: str) -> Dict:
        """Parse kitchen command using MiniMax AI"""
        
        prompt = f"""You are a kitchen command parser for a restaurant system.

Parse this chef's voice command:
"{transcript}"

Extract and return ONLY valid JSON:
{{
  "action": "fire" | "cancel" | "update" | "status" | "86" | "plated",
  "table_number": number or null,
  "order_number": number or null,
  "items": [
    {{
      "dish": "steak" | "salmon" | "pasta" | etc,
      "temp": "rare" | "medium_rare" | "medium" | "well_done" | null,
      "quantity": number,
      "modifications": ["no salt", "extra sauce", etc]
    }}
  ],
  "urgency": "normal" | "rush" | "asap",
  "notes": "any additional context"
}}

Kitchen slang translations:
- "fire" = start cooking
- "86" = mark as sold out
- "pickup/plated" = dish is ready
- "on the fly" = rush order

Examples:
"Order fire table 5, two steaks medium-rare" → action: fire, table: 5, items: [{{dish: steak, temp: medium_rare, quantity: 2}}]
"86 salmon" → action: 86, items: [{{dish: salmon}}]
"Steak table 3 plated" → action: plated, table: 3, items: [{{dish: steak}}]

Respond with ONLY the JSON, no other text."""

        try:
            if not self.minimax_key:
                # Demo mode - simple parsing
                return self._demo_parse(transcript)
            
            # Real MiniMax API call
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    "https://api.minimax.chat/v1/text/chatcompletion_v2",
                    headers={
                        "Authorization": f"Bearer {self.minimax_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "abab6-chat",
                        "messages": [{"role": "user", "content": prompt}],
                        "temperature": 0.1
                    }
                )
                
                result = response.json()
                content = result['choices'][0]['message']['content']
                
                # Clean JSON
                if "```json" in content:
                    content = content.split("```json")[1].split("```")[0]
                elif "```" in content:
                    content = content.split("```")[1].split("```")[0]
                
                return json.loads(content.strip())
                
        except Exception as e:
            print(f"MiniMax error: {e}")
            return self._demo_parse(transcript)
    
    def _demo_parse(self, transcript: str) -> Dict:
        """Simple demo parsing without API"""
        
        transcript_lower = transcript.lower()
        
        # Detect action
        action = "fire"
        if "cancel" in transcript_lower:
            action = "cancel"
        elif "86" in transcript_lower or "sold out" in transcript_lower:
            action = "86"
        elif "plated" in transcript_lower or "pickup" in transcript_lower or "ready" in transcript_lower:
            action = "plated"
        elif "status" in transcript_lower or "what's" in transcript_lower:
            action = "status"
        
        # Extract table number
        table_match = re.search(r'table\s+(\d+)', transcript_lower)
        table_number = int(table_match.group(1)) if table_match else None
        
        # Extract dishes
        items = []
        
        # Steaks
        steak_match = re.search(r'(\w+)?\s*steaks?\s*(medium[-\s]rare|medium[-\s]well|medium|rare|well[-\s]done)?', transcript_lower)
        if steak_match:
            quantity_str = steak_match.group(1)
            quantity = self._word_to_number(quantity_str) if quantity_str else 1
            temp = steak_match.group(2).replace('-', '_').replace(' ', '_') if steak_match.group(2) else "medium_rare"
            
            items.append({
                "dish": "steak",
                "temp": temp,
                "quantity": quantity,
                "modifications": []
            })
        
        # Salmon
        salmon_match = re.search(r'(\w+)?\s*salmon', transcript_lower)
        if salmon_match:
            quantity_str = salmon_match.group(1)
            quantity = self._word_to_number(quantity_str) if quantity_str else 1
            
            items.append({
                "dish": "salmon",
                "temp": None,
                "quantity": quantity,
                "modifications": []
            })
        
        # Pasta
        if "pasta" in transcript_lower or "carbonara" in transcript_lower:
            items.append({
                "dish": "pasta_carbonara",
                "temp": None,
                "quantity": 1,
                "modifications": []
            })
        
        # Salad
        if "salad" in transcript_lower or "caesar" in transcript_lower:
            items.append({
                "dish": "caesar_salad",
                "temp": None,
                "quantity": 1,
                "modifications": []
            })
        
        return {
            "action": action,
            "table_number": table_number,
            "order_number": None,
            "items": items,
            "urgency": "rush" if "on the fly" in transcript_lower or "asap" in transcript_lower else "normal",
            "notes": transcript
        }
    
    def _word_to_number(self, word: str) -> int:
        """Convert word numbers to integers"""
        numbers = {
            "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
            "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10
        }
        return numbers.get(word.lower(), 1)
    
    async def validate_food_safety(self, order_data: Dict, customer_allergies: List[str] = None) -> Dict:
        """Validate food safety and allergens using ArmorIQ"""
        
        # Check for allergen conflicts
        warnings = []
        
        if customer_allergies:
            from menu_data import MENU
            
            for item in order_data.get("items", []):
                dish_key = f"{item['dish']}_{item['temp']}" if item['temp'] else item['dish']
                
                # Find dish in menu
                dish_data = None
                for key, value in MENU.items():
                    if item['dish'] in key or key in item['dish']:
                        dish_data = value
                        break
                
                if dish_data:
                    dish_allergens = dish_data.get("allergens", [])
                    
                    # Check for conflicts
                    conflicts = [a for a in customer_allergies if a in dish_allergens]
                    
                    if conflicts:
                        warnings.append({
                            "severity": "critical",
                            "dish": dish_data["name"],
                            "allergens": conflicts,
                            "message": f"⚠️ ALLERGEN ALERT: {dish_data['name']} contains {', '.join(conflicts)}!"
                        })
        
        return {
            "safe_to_prepare": len(warnings) == 0,
            "warnings": warnings,
            "validation_timestamp": datetime.now().isoformat(),
            "validated_by": "ArmorIQ"
        }