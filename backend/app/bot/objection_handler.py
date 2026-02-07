"""
Sistema de Manejo de Objeciones - MODULAR Y CONFIGURABLE
Detecta y responde objeciones de ventas de forma profesional
"""
from typing import Dict, List, Optional
import re


class ObjectionHandler:
    """Maneja objeciones comunes de clientes"""
    
    # OBJECIONES Y RESPUESTAS - Editables y expandibles
    OBJECTIONS = {
        "precio_alto": {
            "keywords": [
                "caro", "costoso", "mucho dinero", "muy caro", "precio alto",
                "no tengo", "no puedo pagar", "es mucho"
            ],
            "respuestas": [
                """Entiendo tu preocupación por el precio. Déjame mostrarte por qué vale la pena:

**Si compraras las IAs individualmente**:
💰 ChatGPT Plus: $20/mes = ~75 soles
💰 Midjourney: $30/mes = ~110 soles
💰 Claude Pro: $20/mes = ~75 soles
💰 Sora: No disponible individualmente
**Total**: Más de 260 soles/mes

**Con el MEGAPACK**: Solo 30 soles/mes
✅ Ahorras más del 88%
✅ Obtienes 40+ IAs en lugar de 3
✅ Incluye Sora 2 y Veo 3.1 (no disponibles solos)

¿Tiene más sentido ahora? 🤔""",
                
                """Te entiendo perfectamente. Por eso tenemos el **plan de 1 mes por solo 30 soles** 💰

Es menos que:
- Una cena 🍕
- Una entrada al cine 🎬  
- Un día de delivery 🚚

Y obtienes:
✅ 40+ IAs premium durante 30 días completos
✅ Sin límites de uso
✅ Acceso a Sora 2, ChatGPT Plus, Claude, Midjourney...

Puedes probarlo 1 mes y si no te convence, no renuevas. ¿Qué te parece? 😊"""
            ]
        },
        
        "no_usar_todo": {
            "keywords": [
                "no usaré", "no lo uso", "no necesito", "solo quiero",
                "no uso todo", "demasiadas", "muchas ias"
            ],
            "respuestas": [
                """¡Perfecto! Nadie usa las 40+ IAs todos los días 😄

Lo importante es que **cuando necesites una IA específica, ya la tienes**:

📅 **Hoy**: Necesitas ChatGPT para trabajo
📅 **Mañana**: Quieres crear un video con Sora
📅 **Próxima semana**: Diseñar algo con Midjourney

Por solo 30 soles/mes tienes todo el arsenal disponible 24/7.

**La mayoría de nuestros miembros**:
- Usan 5-7 IAs regularmente
- Descubren nuevas IAs útiles cada semana
- Agradecen tener acceso cuando las necesitan

¿Prefieres tenerlas y no usarlas, o necesitarlas y no tenerlas? 🤔""",
                
                """Entiendo tu punto. Por eso el MEGAPACK es perfecto:

**No vendes IAs sueltas** porque:
1. La mayoría cuesta más de 30 soles cada una
2. Sora 2 y Veo 3.1 NO están disponibles individualmente
3. Terminarías pagando mucho más por menos

**Con el MEGAPACK**:
✅ Pagas el precio de 1 IA y llevas 40+
✅ Descubres IAs que no sabías que necesitabas
✅ Flexibilidad total para cualquier proyecto

Es como Netflix: pagas por la plataforma completa, no por cada película 🎬"""
            ]
        },
        
        "cuentas_compartidas": {
            "keywords": [
                "compartida", "compartido", "varias personas", "saturado",
                "lento", "muchos usuarios", "personal"
            ],
            "respuestas": [
                """¡Excelente pregunta! 👏

**❌ NO son cuentas compartidas**
**✅ SON cuentas 100% PERSONALES**

**¿Qué significa esto?**:
- Tu usuario y contraseña únicos
- Sin saturación ni lentitud
- Uso ilimitado, cuando quieras
- Licencias oficiales premium

**¿Por qué puedo confiar?**:
📱 Únete a nuestro grupo de referencias: https://chat.whatsapp.com/IumSWrpFzSsCOMdpqIdwoi
👥 Más de 500 miembros satisfechos
⭐ Testimonios reales de usuarios activos

¿Quieres hablar con alguien del grupo antes de decidir? 😊"""
            ]
        },
        
        "seguridad_confianza": {
            "keywords": [
                "seguro", "confiable", "estafa", "real", "verdad",
                "funciona", "legítimo", "referencias"
            ],
            "respuestas": [
                """¡Me alegra que preguntes! La confianza es súper importante 🤝

**Pruebas de que somos reales**:

1. **Grupo de Referencias WhatsApp** 📱
   https://chat.whatsapp.com/IumSWrpFzSsCOMdpqIdwoi
   - Habla directamente con miembros activos
   - Ve testimonios y casos reales
   - Pregunta lo que quieras

2. **Más de 500 miembros activos** 👥
   - Uso diario de las IAs
   - Comunidad establecida
   - Soporte constante

3. **Prueba sin riesgo** ✅
   - Empieza con 1 mes (30 soles)
   - Si no funciona, simplemente no renuevas
   - Entrega inmediata después del pago

¿Quieres entrar al grupo para ver por ti mismo? 🚀""",
                
                """Perfecto que seas cauteloso. Te doy 3 formas de verificarnos:

**1. Grupo de WhatsApp (público)** 📱
https://chat.whatsapp.com/IumSWrpFzSsCOMdpqIdwoi
- Entra y pregunta a miembros reales
- Sin compromiso

**2. Redes sociales** 📲
- Instagram: @iaclub
- TikTok: @iaclub
- Contenido y testimonios diarios

**3. Prueba de 1 mes** 💰
- Solo 30 soles
- Bajo riesgo
- Alta recompensa

No te pido que confíes a ciegas. Verifica tú mismo 😊"""
            ]
        },
        
        "pensarlo": {
            "keywords": [
                "pensarlo", "después", "luego", "más tarde",
                "no sé", "dudas", "tiempo"
            ],
            "respuestas": [
                """¡Por supuesto! Tómate tu tiempo 😊

**Mientras lo piensas, recuerda**:
⏰ La promoción de 30 soles termina este mes
💰 El precio regular será de 50 soles/mes
🎁 Los regalos extras son solo en promoción

**Te recomiendo**:
1. Únete al grupo de referencias: https://chat.whatsapp.com/IumSWrpFzSsCOMdpqIdwoi
2. Habla con miembros actuales
3. Ve casos de uso reales
4. Decide con información completa

¿Tienes alguna duda específica que pueda resolver para ayudarte a decidir? 🤔""",
                
                """¡Entiendo perfectamente! Es una decisión importante 👍

**Para ayudarte a decidir**:

✅ **Lo que obtienes**: 40+ IAs premium
💰 **Inversión**: 30 soles (menos que una pizza)
⏰ **Duración**: 30 días completos
🔄 **Compromiso**: Ninguno (cancelas cuando quieras)

**¿Qué te frena?**
- ¿El precio?
- ¿Dudas sobre las cuentas?
- ¿No sabes si lo usarás?

Dime tu preocupación y la resolvemos juntos 😊"""
            ]
        }
    }
    
    @classmethod
    def detect_objection(cls, message: str) -> Optional[Dict]:
        """
        Detecta si el mensaje contiene una objeción
        
        Returns:
            {
                "type": "precio_alto",
                "confidence": 0.85,
                "keywords_found": ["caro", "mucho dinero"],
                "suggested_response": "..."
            }
            o None si no hay objeción
        """
        message_lower = message.lower()
        
        # Buscar matches en todas las objeciones
        matches = []
        
        for objection_type, data in cls.OBJECTIONS.items():
            keywords_found = [kw for kw in data["keywords"] if kw in message_lower]
            if keywords_found:
                matches.append({
                    "type": objection_type,
                    "keywords_found": keywords_found,
                    "score": len(keywords_found)
                })
        
        if not matches:
            return None
        
        # Retornar la objeción con mayor score
        best_match = max(matches, key=lambda x: x["score"])
        
        # Seleccionar una respuesta aleatoria
        import random
        response = random.choice(cls.OBJECTIONS[best_match["type"]]["respuestas"])
        
        return {
            "type": best_match["type"],
            "confidence": min(best_match["score"] / 3, 1.0),  # Normalizar
            "keywords_found": best_match["keywords_found"],
            "suggested_response": response
        }
    
    @classmethod
    def handle_objection(cls, message: str) -> Optional[str]:
        """
        Detecta y retorna la respuesta apropiada para una objeción
        
        Returns:
            Respuesta si hay objeción, None si no hay
        """
        objection = cls.detect_objection(message)
        if objection and objection["confidence"] > 0.3:
            return objection["suggested_response"]
        return None
    
    @classmethod
    def get_objection_types(cls) -> List[str]:
        """Retorna lista de tipos de objeciones configuradas"""
        return list(cls.OBJECTIONS.keys())
    
    @classmethod
    def add_custom_objection(cls, objection_type: str, keywords: List[str], responses: List[str]):
        """Permite agregar objeciones personalizadas en runtime"""
        cls.OBJECTIONS[objection_type] = {
            "keywords": keywords,
            "respuestas": responses
        }


# Exportar para fácil uso
objection_handler = ObjectionHandler()
