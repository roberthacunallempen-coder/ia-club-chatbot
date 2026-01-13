"""
Sistema de Contexto de Cliente - MODULAR Y CONFIGURABLE
Almacena y gestiona el contexto de cada cliente durante la conversación
"""
from typing import Dict, List, Optional
import re
from datetime import datetime


class CustomerContext:
    """Maneja el contexto del cliente durante la conversación"""
    
    def __init__(self):
        self.context = {
            "name": None,
            "interests": [],
            "profile": None,
            "objections_mentioned": [],
            "products_interested": [],
            "budget_mentioned": None,
            "contact_info": {},
            "session_start": datetime.now(),
            "message_count": 0,
            "questions_asked": [],
            "engagement_level": "low"  # low, medium, high
        }
    
    def extract_name(self, message: str):
        """Extrae el nombre del cliente del mensaje"""
        # Patrones comunes: "Soy Juan", "Me llamo María", "Mi nombre es Pedro"
        patterns = [
            r"(?:soy|me llamo|mi nombre es)\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)",
            r"(?:^|\s)([A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)\s+(?:aquí|acá|presente)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                self.context["name"] = match.group(1)
                return match.group(1)
        return None
    
    def extract_contact_info(self, message: str):
        """Extrae información de contacto (email, teléfono)"""
        # Email pattern
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, message)
        if email_match:
            self.context["contact_info"]["email"] = email_match.group(0)
        
        # Phone pattern (Perú: 9 dígitos)
        phone_pattern = r'\b9\d{8}\b'
        phone_match = re.search(phone_pattern, message)
        if phone_match:
            self.context["contact_info"]["phone"] = phone_match.group(0)
    
    def extract_budget(self, message: str):
        """Extrae presupuesto mencionado"""
        # Patrones: "30 soles", "tengo 50", "mi presupuesto es 70"
        patterns = [
            r'(\d+)\s*(?:soles|soles?)',
            r'(?:tengo|presupuesto|dispongo).*?(\d+)',
            r'(?:hasta|máximo).*?(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                self.context["budget_mentioned"] = int(match.group(1))
                return int(match.group(1))
        return None
    
    def add_interest(self, interest: str):
        """Agrega un interés detectado"""
        if interest not in self.context["interests"]:
            self.context["interests"].append(interest)
    
    def add_objection(self, objection_type: str):
        """Registra una objeción mencionada"""
        if objection_type not in self.context["objections_mentioned"]:
            self.context["objections_mentioned"].append(objection_type)
    
    def add_product_interest(self, product: str):
        """Registra interés en un producto específico"""
        if product not in self.context["products_interested"]:
            self.context["products_interested"].append(product)
    
    def add_question(self, question: str):
        """Registra una pregunta hecha"""
        self.context["questions_asked"].append({
            "question": question,
            "timestamp": datetime.now()
        })
    
    def increment_message_count(self):
        """Incrementa contador de mensajes"""
        self.context["message_count"] += 1
        self._update_engagement_level()
    
    def _update_engagement_level(self):
        """Actualiza el nivel de engagement basado en la actividad"""
        count = self.context["message_count"]
        has_objections = len(self.context["objections_mentioned"]) > 0
        has_interests = len(self.context["interests"]) > 0
        
        if count >= 5 and (has_objections or has_interests):
            self.context["engagement_level"] = "high"
        elif count >= 3:
            self.context["engagement_level"] = "medium"
        else:
            self.context["engagement_level"] = "low"
    
    def set_profile(self, profile: str):
        """Establece el perfil del cliente"""
        self.context["profile"] = profile
    
    def get_context(self) -> Dict:
        """Retorna el contexto completo"""
        return self.context
    
    def get_summary(self) -> str:
        """Genera un resumen del contexto para el agente"""
        summary_parts = []
        
        if self.context["name"]:
            summary_parts.append(f"Cliente: {self.context['name']}")
        
        if self.context["profile"]:
            summary_parts.append(f"Perfil: {self.context['profile']}")
        
        if self.context["interests"]:
            summary_parts.append(f"Intereses: {', '.join(self.context['interests'])}")
        
        if self.context["products_interested"]:
            summary_parts.append(f"Productos de interés: {', '.join(self.context['products_interested'])}")
        
        if self.context["budget_mentioned"]:
            summary_parts.append(f"Presupuesto: {self.context['budget_mentioned']} soles")
        
        if self.context["objections_mentioned"]:
            summary_parts.append(f"Objeciones: {', '.join(self.context['objections_mentioned'])}")
        
        summary_parts.append(f"Nivel de engagement: {self.context['engagement_level']}")
        summary_parts.append(f"Mensajes: {self.context['message_count']}")
        
        return " | ".join(summary_parts) if summary_parts else "Nuevo cliente"
    
    def should_push_for_sale(self) -> bool:
        """Determina si debe presionar para cerrar la venta"""
        return (
            self.context["engagement_level"] == "high" or
            self.context["message_count"] >= 5 or
            len(self.context["products_interested"]) > 0
        )
    
    def should_offer_discount(self) -> bool:
        """Determina si debe ofrecer descuento basado en objeciones"""
        return (
            "precio_alto" in self.context["objections_mentioned"] or
            (self.context["budget_mentioned"] and self.context["budget_mentioned"] < 30)
        )
    
    def get_personalized_greeting(self) -> str:
        """Genera saludo personalizado basado en contexto"""
        if self.context["name"]:
            return f"¡Hola de nuevo, {self.context['name']}! 👋"
        return "¡Hola! 👋"
    
    def update_from_message(self, message: str):
        """Actualiza contexto automáticamente desde un mensaje"""
        self.increment_message_count()
        self.extract_name(message)
        self.extract_contact_info(message)
        self.extract_budget(message)
        
        # Detectar intereses
        interests_map = {
            "video": ["video", "sora", "veo", "contenido audiovisual"],
            "diseño": ["diseño", "midjourney", "imagen", "arte"],
            "programación": ["código", "programar", "desarrollo", "copilot"],
            "académico": ["tesis", "investigación", "universidad", "turnitin"],
            "negocio": ["empresa", "negocio", "productividad"]
        }
        
        message_lower = message.lower()
        for interest, keywords in interests_map.items():
            if any(kw in message_lower for kw in keywords):
                self.add_interest(interest)


class ContextManager:
    """Gestor global de contextos de clientes"""
    
    def __init__(self):
        self.contexts = {}  # conversation_id -> CustomerContext
    
    def get_context(self, conversation_id: int) -> CustomerContext:
        """Obtiene o crea contexto para una conversación"""
        if conversation_id not in self.contexts:
            self.contexts[conversation_id] = CustomerContext()
        return self.contexts[conversation_id]
    
    def clear_context(self, conversation_id: int):
        """Limpia el contexto de una conversación"""
        if conversation_id in self.contexts:
            del self.contexts[conversation_id]
    
    def get_all_contexts(self) -> Dict:
        """Retorna todos los contextos activos"""
        return self.contexts


# Instancia global
context_manager = ContextManager()
