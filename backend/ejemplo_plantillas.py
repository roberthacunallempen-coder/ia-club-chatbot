"""
Script de ejemplo para crear y usar plantillas de mensajes predeterminadas
Este script muestra cómo crear plantillas y enviarlas programáticamente
"""

import asyncio
import httpx
import json

# Configuración
API_URL = "http://localhost:8000"
CONVERSATION_ID = 12345  # Cambia esto por un ID real de Chatwoot

async def main():
    print("🚀 Ejemplo de uso del Sistema de Plantillas de Mensajes\n")
    
    async with httpx.AsyncClient() as client:
        
        # ==========================================
        # 1. CREAR PLANTILLA DE BIENVENIDA
        # ==========================================
        print("📝 1. Creando plantilla de bienvenida...")
        
        plantilla_bienvenida = {
            "name": "Bienvenida_Demo",
            "description": "Secuencia de bienvenida para demostración",
            "category": "bienvenida",
            "trigger_keywords": ["hola", "buenos días", "hola!", "hey"],
            "is_active": True,
            "messages": [
                {
                    "order": 0,
                    "type": "text",
                    "content": "¡Hola {customer_name}! 👋 Bienvenido a IA Club.",
                    "delay_seconds": 0
                },
                {
                    "order": 1,
                    "type": "text",
                    "content": "Soy Tío IA, tu asistente virtual especializado en Inteligencia Artificial.",
                    "delay_seconds": 2
                },
                {
                    "order": 2,
                    "type": "text",
                    "content": "¿En qué puedo ayudarte hoy? Puedo informarte sobre:\n\n✅ Cursos de IA\n✅ Comunidad\n✅ Recursos exclusivos\n✅ Precios y planes",
                    "delay_seconds": 3
                }
            ]
        }
        
        response = await client.post(
            f"{API_URL}/templates/",
            json=plantilla_bienvenida
        )
        
        if response.status_code == 201:
            template_id_1 = response.json()["id"]
            print(f"✅ Plantilla creada con ID: {template_id_1}\n")
        else:
            print(f"❌ Error: {response.text}\n")
        
        # ==========================================
        # 2. CREAR PLANTILLA DE INFORMACIÓN DE CURSOS
        # ==========================================
        print("📝 2. Creando plantilla de información de cursos...")
        
        plantilla_cursos = {
            "name": "Info_Cursos_Demo",
            "description": "Información detallada sobre cursos",
            "category": "productos",
            "trigger_keywords": ["cursos", "curso", "formación", "estudiar"],
            "is_active": True,
            "messages": [
                {
                    "order": 0,
                    "type": "text",
                    "content": "📚 Te cuento sobre nuestros cursos de IA:",
                    "delay_seconds": 0
                },
                {
                    "order": 1,
                    "type": "text",
                    "content": "🎯 **Curso de IA para Principiantes**\n- Duración: 8 semanas\n- Nivel: Básico\n- Precio: $199\n\n🚀 **Curso de IA Avanzada**\n- Duración: 12 semanas\n- Nivel: Avanzado\n- Precio: $399",
                    "delay_seconds": 2
                },
                {
                    "order": 2,
                    "type": "text",
                    "content": "💡 Todos los cursos incluyen:\n✅ Acceso de por vida\n✅ Comunidad privada\n✅ Certificado\n✅ Soporte personalizado",
                    "delay_seconds": 3
                },
                {
                    "order": 3,
                    "type": "text",
                    "content": "¿Te interesa algún curso en particular? 🤔",
                    "delay_seconds": 2
                }
            ]
        }
        
        response = await client.post(
            f"{API_URL}/templates/",
            json=plantilla_cursos
        )
        
        if response.status_code == 201:
            template_id_2 = response.json()["id"]
            print(f"✅ Plantilla creada con ID: {template_id_2}\n")
        else:
            print(f"❌ Error: {response.text}\n")
        
        # ==========================================
        # 3. CREAR PLANTILLA DE PRECIOS
        # ==========================================
        print("📝 3. Creando plantilla de precios...")
        
        plantilla_precios = {
            "name": "Info_Precios_Demo",
            "description": "Información sobre precios y planes",
            "category": "ventas",
            "trigger_keywords": ["precio", "precios", "costo", "cuanto cuesta", "cuánto cuesta"],
            "is_active": True,
            "messages": [
                {
                    "order": 0,
                    "type": "text",
                    "content": "💰 Estos son nuestros planes:",
                    "delay_seconds": 0
                },
                {
                    "order": 1,
                    "type": "text",
                    "content": "📦 **Plan Básico - $49/mes**\n- Acceso a cursos básicos\n- Comunidad\n- Recursos básicos\n\n🎁 **Plan Pro - $99/mes**\n- Todos los cursos\n- Comunidad VIP\n- Recursos exclusivos\n- Soporte prioritario\n\n🏆 **Plan Premium - $199/mes**\n- Todo incluido\n- Mentorías 1-1\n- Proyectos personalizados\n- Certificaciones",
                    "delay_seconds": 2
                },
                {
                    "order": 2,
                    "type": "text",
                    "content": "🎉 **OFERTA ESPECIAL**: 20% de descuento en tu primer mes usando el código: DEMO20",
                    "delay_seconds": 3
                },
                {
                    "order": 3,
                    "type": "text",
                    "content": "¿Qué plan te interesa más? Puedo darte más detalles 😊",
                    "delay_seconds": 2
                }
            ]
        }
        
        response = await client.post(
            f"{API_URL}/templates/",
            json=plantilla_precios
        )
        
        if response.status_code == 201:
            template_id_3 = response.json()["id"]
            print(f"✅ Plantilla creada con ID: {template_id_3}\n")
        else:
            print(f"❌ Error: {response.text}\n")
        
        # ==========================================
        # 4. LISTAR TODAS LAS PLANTILLAS
        # ==========================================
        print("📋 4. Listando todas las plantillas activas...")
        
        response = await client.get(f"{API_URL}/templates?is_active=true")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Total de plantillas activas: {data['total']}")
            for template in data['templates']:
                print(f"   - {template['name']} ({len(template['messages'])} mensajes)")
            print()
        
        # ==========================================
        # 5. ENVIAR UNA PLANTILLA MANUALMENTE
        # ==========================================
        print("📤 5. Enviando plantilla de bienvenida a conversación...")
        
        # IMPORTANTE: Necesitas un conversation_id válido de Chatwoot
        # Si no tienes uno, comenta esta sección
        
        """
        send_request = {
            "template_id": template_id_1,
            "conversation_id": CONVERSATION_ID,
            "variables": {
                "customer_name": "Juan"
            }
        }
        
        response = await client.post(
            f"{API_URL}/templates/send",
            json=send_request
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Plantilla enviada: {result['messages_sent']} mensajes")
            print(f"   Conversación: {result['conversation_id']}")
        else:
            print(f"❌ Error al enviar: {response.text}")
        """
        
        print("⚠️ El envío manual está comentado (necesitas un conversation_id válido)")
        print()
        
        # ==========================================
        # 6. LISTAR CATEGORÍAS
        # ==========================================
        print("🏷️ 6. Listando categorías de plantillas...")
        
        response = await client.get(f"{API_URL}/templates/categories/list")
        if response.status_code == 200:
            categories = response.json()
            print(f"✅ Categorías encontradas: {', '.join(categories)}\n")
        
        # ==========================================
        # 7. OBTENER PLANTILLA POR ID
        # ==========================================
        print(f"🔍 7. Obteniendo detalles de la plantilla de bienvenida...")
        
        response = await client.get(f"{API_URL}/templates/{template_id_1}")
        if response.status_code == 200:
            template = response.json()
            print(f"✅ Plantilla: {template['name']}")
            print(f"   Descripción: {template['description']}")
            print(f"   Mensajes: {len(template['messages'])}")
            print(f"   Palabras clave: {', '.join(template['trigger_keywords'])}")
            print()
        
        # ==========================================
        # 8. ACTUALIZAR PLANTILLA
        # ==========================================
        print("✏️ 8. Actualizando plantilla (desactivándola)...")
        
        update_data = {
            "is_active": False
        }
        
        response = await client.put(
            f"{API_URL}/templates/{template_id_1}",
            json=update_data
        )
        
        if response.status_code == 200:
            print(f"✅ Plantilla actualizada\n")
        
        # ==========================================
        # RESUMEN
        # ==========================================
        print("\n" + "="*60)
        print("✅ DEMOSTRACIÓN COMPLETADA")
        print("="*60)
        print("\n📝 Se crearon 3 plantillas de ejemplo:")
        print("   1. Bienvenida_Demo (bienvenida)")
        print("   2. Info_Cursos_Demo (productos)")
        print("   3. Info_Precios_Demo (ventas)")
        print("\n💡 Ahora puedes:")
        print("   - Ver las plantillas en: http://localhost:5173/templates")
        print("   - Enviarlas manualmente desde la API")
        print("   - Dejar que el bot las active automáticamente por keywords")
        print("\n🔑 Palabras clave configuradas:")
        print("   - 'hola' → Bienvenida_Demo")
        print("   - 'cursos' → Info_Cursos_Demo")
        print("   - 'precio' → Info_Precios_Demo")
        print("\n🧪 Prueba escribiendo estas palabras en el chat!")
        print("="*60 + "\n")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🤖 SISTEMA DE PLANTILLAS DE MENSAJES - EJEMPLO")
    print("="*60 + "\n")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️ Operación cancelada por el usuario")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
