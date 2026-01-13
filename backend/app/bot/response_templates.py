"""
Sistema de Templates de Respuestas - MODULAR Y CONFIGURABLE
Permite variaciones, CTAs, social proof y urgencia
"""
import random
from typing import Dict, List


class ResponseTemplates:
    """Sistema de templates de respuestas configurables"""
    
    # CALL TO ACTIONS (CTAs) - Editables
    CTAS_VENTAS = [
        "¿Te gustaría que te reserve el plan de {duration}?",
        "¿Prefieres empezar con {option1} o aprovechar el descuento de {option2}?",
        "¿Listo para unirte al club? 🚀",
        "¿Quieres que te envíe el link de pago?",
        "¿Te animas a probar el club este mes?"
    ]
    
    CTAS_DISEÑO = [
        "¿Qué tipo de contenido quieres crear?",
        "¿Te gustaría ver ejemplos de lo que puedes hacer con estas IAs?",
        "¿Necesitas ayuda para elegir la mejor IA para tu proyecto?"
    ]
    
    CTAS_SOPORTE = [
        "¿Esto resuelve tu duda?",
        "¿Necesitas que te ayude con algo más?",
        "¿Todo claro? Aquí estoy si necesitas más ayuda 🤖"
    ]
    
    # SOCIAL PROOF - Editable
    SOCIAL_PROOF = [
        "Más de 500 miembros ya disfrutan del MEGAPACK 🚀",
        "Únete a nuestra comunidad de creadores y académicos 🎓",
        "Miles de proyectos creados con nuestras IAs ✨",
        "Grupo de referencias: https://chat.whatsapp.com/IumSWrpFzSsCOMdpqIdwoi"
    ]
    
    # URGENCIA - Editable
    URGENCIA = [
        "⏰ Promoción válida hasta fin de mes",
        "🔥 Últimos días de la promoción especial",
        "⚡ Aprovecha el precio de lanzamiento",
        "💎 Precio especial por tiempo limitado"
    ]
    
    # VARIACIONES DE SALUDOS - Editables
    SALUDOS_INICIALES = [
        "¡Hola! Soy Tío IA 🤖",
        "¡Hey! Aquí Tío IA, bienvenido al club 🚀",
        "¡Saludos! Soy Tío IA, tu guía en el club de IAs 💬",
        "¡Qué tal! Tío IA por aquí 👋"
    ]
    
    # VARIACIONES DE RESPUESTAS A PRECIOS - Editables
    INTRO_PRECIOS = [
        "¡Claro! Te detallo nuestros planes para el MEGAPACK:",
        "¡Perfecto! Déjame mostrarte los precios del MEGAPACK:",
        "¡Excelente pregunta! Estos son nuestros planes:",
        "¡Por supuesto! Mira nuestras opciones:"
    ]
    
    # PRECIOS FORMATEADOS - Editable centralmente
    PRECIOS_MEGAPACK = """
**PLANES MEGAPACK** 💰

1. **1 mes**: 💰 **30 soles**
2. **2 meses**: 💰 **50 soles** (ahorro vs mensual)
3. **3 meses**: 💰 **70 soles** ⭐ (mejor precio)

**INCLUYE**:
✅ 40+ IAs premium
✅ ChatGPT Plus, Claude, Sora 2, Veo 3.1, Midjourney
✅ Cuentas personales, uso ilimitado
✅ 3 combos completos de IAs
✅ 3 regalos extras
"""
    
    PRECIOS_VIP = """
**PLANES VIP** 💎

💎 **VIP** (40 soles/mes):
- Todo el MEGAPACK incluido
- IAs más sofisticadas
- Cursos especiales
- Networking exclusivo
- Migración disponible pagando diferencia
"""
    
    @classmethod
    def get_random_saludo(cls) -> str:
        """Obtiene un saludo aleatorio"""
        return random.choice(cls.SALUDOS_INICIALES)
    
    @classmethod
    def get_random_intro_precios(cls) -> str:
        """Obtiene una introducción aleatoria para precios"""
        return random.choice(cls.INTRO_PRECIOS)
    
    @classmethod
    def get_random_cta(cls, tipo: str = "ventas") -> str:
        """Obtiene un CTA aleatorio según el tipo"""
        if tipo == "ventas":
            return random.choice(cls.CTAS_VENTAS)
        elif tipo == "diseño":
            return random.choice(cls.CTAS_DISEÑO)
        elif tipo == "soporte":
            return random.choice(cls.CTAS_SOPORTE)
        return random.choice(cls.CTAS_VENTAS)
    
    @classmethod
    def get_random_social_proof(cls) -> str:
        """Obtiene prueba social aleatoria"""
        return random.choice(cls.SOCIAL_PROOF)
    
    @classmethod
    def get_urgencia(cls) -> str:
        """Obtiene mensaje de urgencia aleatorio"""
        return random.choice(cls.URGENCIA)
    
    @classmethod
    def build_precio_response(cls, include_urgencia: bool = True) -> str:
        """Construye respuesta completa de precios con variaciones"""
        response_parts = [
            cls.get_random_intro_precios(),
            "",
            cls.PRECIOS_MEGAPACK,
        ]
        
        if include_urgencia:
            response_parts.append(cls.get_urgencia())
            response_parts.append("")
        
        response_parts.append(cls.get_random_social_proof())
        response_parts.append("")
        response_parts.append(cls.get_random_cta("ventas").format(
            duration="3 meses",
            option1="1 mes",
            option2="3 meses"
        ))
        
        return "\n".join(response_parts)
    
    @classmethod
    def add_cta_to_response(cls, response: str, tipo: str = "ventas") -> str:
        """Agrega un CTA al final de cualquier respuesta"""
        cta = cls.get_random_cta(tipo)
        return f"{response}\n\n{cta}"
    
    @classmethod
    def add_social_proof_to_response(cls, response: str) -> str:
        """Agrega prueba social a cualquier respuesta"""
        proof = cls.get_random_social_proof()
        return f"{response}\n\n{proof}"


# Exportar para fácil importación
templates = ResponseTemplates()
