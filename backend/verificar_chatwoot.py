"""
Script para verificar y configurar la conexión con Chatwoot
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.config import get_settings
import asyncio
import aiohttp

settings = get_settings()

def check_env_variables():
    """Verifica que las variables de entorno estén configuradas"""
    print("\n" + "="*60)
    print("🔍 VERIFICANDO VARIABLES DE ENTORNO")
    print("="*60 + "\n")
    
    checks = {
        "CHATWOOT_API_KEY": settings.chatwoot_api_key,
        "CHATWOOT_BASE_URL": settings.chatwoot_base_url,
        "CHATWOOT_ACCOUNT_ID": settings.chatwoot_account_id,
        "OPENAI_API_KEY": settings.openai_api_key,
    }
    
    all_ok = True
    for key, value in checks.items():
        if not value or (isinstance(value, str) and "your-" in value.lower()):
            print(f"❌ {key}: NO CONFIGURADO")
            all_ok = False
        else:
            # Mostrar solo los primeros caracteres por seguridad
            display_value = str(value)
            if "KEY" in key:
                display_value = display_value[:10] + "..." if len(display_value) > 10 else display_value
            print(f"✅ {key}: {display_value}")
    
    print()
    return all_ok

async def test_chatwoot_connection():
    """Prueba la conexión con Chatwoot API"""
    print("\n" + "="*60)
    print("🔗 PROBANDO CONEXIÓN CON CHATWOOT")
    print("="*60 + "\n")
    
    url = f"{settings.chatwoot_base_url}/api/v1/accounts/{settings.chatwoot_account_id}/conversations"
    headers = {
        "api_access_token": settings.chatwoot_api_key,
        "Content-Type": "application/json"
    }
    
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status == 200:
                    data = await response.json()
                    print(f"✅ CONEXIÓN EXITOSA")
                    print(f"   Status: {response.status}")
                    print(f"   Conversaciones encontradas: {len(data.get('data', {}).get('payload', []))}")
                    return True
                elif response.status == 401:
                    print(f"❌ ERROR DE AUTENTICACIÓN")
                    print(f"   Status: {response.status}")
                    print(f"   Mensaje: API Key inválida o expirada")
                    print(f"\n💡 Solución:")
                    print(f"   1. Ve a Chatwoot → Profile Settings → Access Token")
                    print(f"   2. Copia tu Personal Access Token")
                    print(f"   3. Actualiza CHATWOOT_API_KEY en .env.local")
                    return False
                elif response.status == 404:
                    print(f"❌ ACCOUNT ID INCORRECTO")
                    print(f"   Status: {response.status}")
                    print(f"   Account ID: {settings.chatwoot_account_id}")
                    print(f"\n💡 Solución:")
                    print(f"   1. Mira la URL de Chatwoot: /app/accounts/XXXXX/...")
                    print(f"   2. Actualiza CHATWOOT_ACCOUNT_ID en .env.local")
                    return False
                else:
                    print(f"❌ ERROR DESCONOCIDO")
                    print(f"   Status: {response.status}")
                    text = await response.text()
                    print(f"   Respuesta: {text[:200]}")
                    return False
    except aiohttp.ClientConnectorError:
        print(f"❌ ERROR DE CONEXIÓN")
        print(f"   No se pudo conectar a: {settings.chatwoot_base_url}")
        print(f"\n💡 Solución:")
        print(f"   1. Verifica que CHATWOOT_BASE_URL sea correcto")
        print(f"   2. Verifica tu conexión a internet")
        return False
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        return False

async def test_openai_connection():
    """Prueba la conexión con OpenAI API"""
    print("\n" + "="*60)
    print("🤖 PROBANDO CONEXIÓN CON OPENAI")
    print("="*60 + "\n")
    
    try:
        from app.services.openai_service import openai_service
        
        # Intenta hacer una llamada simple
        response = await openai_service.generate_response(
            system_prompt="Eres un asistente útil",
            user_message="Responde solo con: OK",
            temperature=0.1,
            max_tokens=10
        )
        
        if response and "OK" in response.upper():
            print(f"✅ OPENAI FUNCIONANDO CORRECTAMENTE")
            print(f"   Modelo: {settings.openai_model}")
            print(f"   Respuesta: {response}")
            return True
        else:
            print(f"⚠️ OPENAI RESPONDE PERO CON CONTENIDO INESPERADO")
            print(f"   Respuesta: {response}")
            return True  # Todavía funciona, solo respuesta rara
    except Exception as e:
        print(f"❌ ERROR EN OPENAI")
        print(f"   Error: {str(e)}")
        print(f"\n💡 Solución:")
        print(f"   1. Verifica que OPENAI_API_KEY sea válida")
        print(f"   2. Verifica que tengas créditos en tu cuenta OpenAI")
        print(f"   3. Actualiza OPENAI_API_KEY en .env.local")
        return False

def print_next_steps():
    """Imprime los siguientes pasos"""
    print("\n" + "="*60)
    print("📋 SIGUIENTES PASOS")
    print("="*60 + "\n")
    
    print("1. CONFIGURAR WEBHOOK EN CHATWOOT:")
    print("   • Ve a Settings → Integrations → Webhooks")
    print("   • Add Webhook")
    print("   • URL: https://TU-DOMINIO.COM/webhook/chatwoot")
    print("   • Eventos: message_created ✅")
    print()
    
    print("2. PARA DESARROLLO LOCAL (ngrok):")
    print("   • Descarga ngrok: https://ngrok.com/download")
    print("   • Ejecuta: ngrok http 8000")
    print("   • Usa la URL pública en el webhook de Chatwoot")
    print()
    
    print("3. CREAR INBOX EN CHATWOOT:")
    print("   • Settings → Inboxes → Add Inbox")
    print("   • Tipo: API (o Website)")
    print("   • Nombre: IA Club Bot")
    print()
    
    print("4. PROBAR:")
    print("   • Envía un mensaje en Chatwoot")
    print("   • El bot debería responder automáticamente")
    print()
    
    print("📚 Documentación completa: CONFIGURACION_CHATWOOT.md")
    print()

async def main():
    """Función principal"""
    print("\n" + "="*60)
    print("🚀 CONFIGURACIÓN Y VERIFICACIÓN DE CHATWOOT")
    print("="*60)
    
    # 1. Verificar variables de entorno
    env_ok = check_env_variables()
    
    if not env_ok:
        print("\n⚠️  CONFIGURACIÓN INCOMPLETA")
        print("\n📝 Instrucciones:")
        print("   1. Edita el archivo: backend\\.env.local")
        print("   2. Actualiza las variables marcadas con ❌")
        print("   3. Ejecuta este script de nuevo")
        print()
        return
    
    # 2. Probar conexión con Chatwoot
    chatwoot_ok = await test_chatwoot_connection()
    
    # 3. Probar conexión con OpenAI
    openai_ok = await test_openai_connection()
    
    # 4. Resumen
    print("\n" + "="*60)
    print("📊 RESUMEN")
    print("="*60 + "\n")
    
    if env_ok and chatwoot_ok and openai_ok:
        print("✅ TODO CONFIGURADO CORRECTAMENTE")
        print("\n🎉 ¡Tu bot está listo para conectarse con Chatwoot!")
        print_next_steps()
    elif env_ok and chatwoot_ok and not openai_ok:
        print("⚠️  CHATWOOT OK, pero OpenAI tiene problemas")
        print("\nEl bot puede recibir mensajes pero no podrá generar respuestas.")
        print("Configura OpenAI antes de continuar.")
    elif env_ok and not chatwoot_ok:
        print("⚠️  OPENAI OK, pero Chatwoot no está conectado")
        print("\nRevisa las credenciales de Chatwoot y vuelve a intentar.")
    else:
        print("❌ HAY PROBLEMAS DE CONFIGURACIÓN")
        print("\nRevisa los errores arriba y corrige la configuración.")
    
    print()

if __name__ == "__main__":
    asyncio.run(main())
