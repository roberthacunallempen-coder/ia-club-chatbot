"""
Sistema de Perfilado de Clientes - MODULAR Y CONFIGURABLE
Detecta el tipo de cliente y personaliza respuestas
"""
from typing import Dict, List, Optional
import re


class CustomerProfiler:
    """Detecta y clasifica el perfil del cliente"""
    
    # PALABRAS CLAVE POR PERFIL - Editables
    KEYWORDS = {
        "academico": [
            "tesis", "investigación", "paper", "artículo", "universidad",
            "estudiante", "profesor", "académico", "turnitin", "plagio",
            "referencias", "bibliografía", "ensayo", "reporte", "estudio"
        ],
        "creativo": [
            "video", "diseño", "contenido", "youtube", "tiktok", "instagram",
            "redes sociales", "marketing", "publicidad", "imagen", "arte",
            "creativo", "edición", "animación", "sora", "veo", "midjourney"
        ],
        "desarrollador": [
            "código", "programar", "desarrollo", "app", "software", "web",
            "api", "backend", "frontend", "debug", "error", "copilot",
            "github", "python", "javascript", "programación"
        ],
        "empresario": [
            "negocio", "empresa", "ventas", "cliente", "equipo", "productividad",
            "automatización", "eficiencia", "ahorro", "tiempo", "gestión"
        ]
    }
    
    # IAs RECOMENDADAS POR PERFIL - Editables
    IAS_POR_PERFIL = {
        "academico": {
            "principales": ["ChatGPT Plus", "Claude", "Perplexity", "Consensus"],
            "destacar": "🎓 **Para académicos**: ChatGPT Plus y Claude son perfectos para investigación, redacción de papers y análisis de datos.",
            "beneficios": [
                "Análisis profundo de literatura académica",
                "Redacción y corrección de textos",
                "Generación de referencias bibliográficas",
                "Compatible con herramientas antiplagio"
            ]
        },
        "creativo": {
            "principales": ["Sora 2", "Veo 3.1 Ultra", "Midjourney", "CapCut PRO", "Runway"],
            "destacar": "🎨 **Para creadores**: Sora 2 y Veo 3.1 son las IAs de video más avanzadas del mercado, junto con Midjourney para diseño.",
            "beneficios": [
                "Generación de videos con sonido (Sora 2)",
                "Calidad cinematográfica (Veo 3.1 Ultra)",
                "Diseños profesionales (Midjourney)",
                "Edición avanzada (CapCut PRO)"
            ]
        },
        "desarrollador": {
            "principales": ["ChatGPT Plus", "Claude", "GitHub Copilot", "Cursor AI"],
            "destacar": "💻 **Para developers**: ChatGPT Plus y Claude son ideales para debugging, code review y arquitectura de software.",
            "beneficios": [
                "Generación de código optimizado",
                "Debugging inteligente",
                "Documentación automática",
                "Code reviews y mejores prácticas"
            ]
        },
        "empresario": {
            "principales": ["ChatGPT Plus", "Claude", "Jasper", "Copy.ai"],
            "destacar": "💼 **Para negocios**: Automatiza tareas, mejora productividad y escala tu operación con IA.",
            "beneficios": [
                "Automatización de tareas repetitivas",
                "Análisis de datos y tendencias",
                "Generación de contenido marketing",
                "Atención al cliente 24/7"
            ]
        }
    }
    
    @classmethod
    def detect_profile(cls, message: str, conversation_history: List[Dict] = None) -> Dict:
        """
        Detecta el perfil del cliente basado en el mensaje y contexto
        
        Returns:
            {
                "profile": "academico" | "creativo" | "desarrollador" | "empresario" | "general",
                "confidence": 0.0-1.0,
                "keywords_found": [...],
                "recommended_ias": [...]
            }
        """
        message_lower = message.lower()
        
        # Agregar contexto de historial
        if conversation_history:
            context = " ".join([
                msg.get("content", "").lower() 
                for msg in conversation_history[-5:]
            ])
            message_lower += " " + context
        
        # Contar matches por perfil
        profile_scores = {}
        keywords_by_profile = {}
        
        for profile, keywords in cls.KEYWORDS.items():
            matches = [kw for kw in keywords if kw in message_lower]
            profile_scores[profile] = len(matches)
            keywords_by_profile[profile] = matches
        
        # Determinar perfil con mayor score
        if max(profile_scores.values()) == 0:
            return {
                "profile": "general",
                "confidence": 0.0,
                "keywords_found": [],
                "recommended_ias": []
            }
        
        detected_profile = max(profile_scores, key=profile_scores.get)
        max_score = profile_scores[detected_profile]
        total_keywords = sum(profile_scores.values())
        confidence = max_score / max(total_keywords, 1)
        
        return {
            "profile": detected_profile,
            "confidence": confidence,
            "keywords_found": keywords_by_profile[detected_profile],
            "recommended_ias": cls.IAS_POR_PERFIL[detected_profile]["principales"]
        }
    
    @classmethod
    def get_personalized_pitch(cls, profile: str) -> str:
        """Obtiene el pitch personalizado según el perfil"""
        if profile in cls.IAS_POR_PERFIL:
            data = cls.IAS_POR_PERFIL[profile]
            
            pitch = f"{data['destacar']}\n\n"
            pitch += "**Beneficios principales**:\n"
            for beneficio in data['beneficios']:
                pitch += f"✅ {beneficio}\n"
            
            return pitch
        
        return ""
    
    @classmethod
    def get_recommended_ias(cls, profile: str) -> List[str]:
        """Obtiene las IAs recomendadas para un perfil"""
        if profile in cls.IAS_POR_PERFIL:
            return cls.IAS_POR_PERFIL[profile]["principales"]
        return []
    
    @classmethod
    def add_profile_to_context(cls, context: Dict, message: str, history: List[Dict] = None) -> Dict:
        """Agrega información de perfil al contexto existente"""
        profile_data = cls.detect_profile(message, history)
        context["customer_profile"] = profile_data
        return context


# Exportar para fácil uso
profiler = CustomerProfiler()
