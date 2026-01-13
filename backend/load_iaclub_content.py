"""
Script para cargar contenido de IA Club
"""
import sys
sys.path.append('C:/Users/Guerr/Music/BOT PYTHON + CHATWOOT/backend')

from app.utils.database import SessionLocal
from app.models.knowledge import Knowledge
from app.models.faq import FAQ

db = SessionLocal()

# Limpiar datos existentes
print("Limpiando datos anteriores...")
db.query(Knowledge).delete()
db.query(FAQ).delete()
db.commit()

# KNOWLEDGE BASE
knowledge_items = [
    {
        "title": "Información General IA Club",
        "category": "empresa",
        "content": """IA Club es un club de inteligencias artificiales que vende paquetes de IA. 
        
Público objetivo:
- Académicos e investigadores
- Profesionales audiovisuales y creadores de contenido  
- Programadores y desarrolladores

Producto estrella: MEGAPACK - Más de 40 IAs en un solo paquete.

Propuesta de valor: Precios accesibles y sentido de pertenencia a un club exclusivo."""
    },
    {
        "title": "MEGAPACK - Producto Principal",
        "category": "productos",
        "content": """El MEGAPACK incluye 3 combos completos:

1ER COMBO - IAs DE ASISTENCIA INTELIGENTE/DESARROLLO/PROGRAMACIÓN
- ChatGPT Plus
- Claude
- Otras IAs de desarrollo

2DO COMBO - IAs DE CREACIÓN DE CONTENIDO/AUDIOVISUALES  
- Sora 2 (generación de video con sonido)
- Veo 3.1 Ultra (generación de video premium)
- Midjourney
- Runway
- Editores de video y audio
- Generadores de imágenes

3ER COMBO - IAs DE EDUCACIÓN E INVESTIGACIÓN/ACADÉMICOS
- Turnitin (detector de IA y plagio)
- Humanizadores (WriteHuman, Humbot, JustDone)
- Perplexity, Consensus, Scribd
- IAs para referencias bibliográficas

VENTAJAS:
✅ Más de 40 IAs incluidas
✅ Licencias oficiales premium
✅ Planes ilimitados sin restricciones
✅ 3 regalos extras incluidos"""
    },
    {
        "title": "Precios MEGAPACK",
        "category": "precios",
        "content": """PRECIOS PROMOCIONALES MEGAPACK:

📅 1 MES: 30 soles
📅 2 MESES: 50 soles  
📅 3 MESES: 70 soles

RENOVACIÓN: Se mantienen los mismos precios promocionales para clientes que renuevan a tiempo.

IMPORTANTE: La promoción caduca a fin de mes. ¡Precio único y accesible!"""
    },
    {
        "title": "Servicios VIP (VIP 1, VIP 2, VIP 3)",
        "category": "productos",
        "content": """SERVICIOS VIP - PRECIO: 40 SOLES/MES

Todos los VIP incluyen:
✅ MEGAPACK completo (40+ IAs)
✅ Google Ultra Veo3 Ilimitado
✅ Cursos premium: TikTok, Facebook, Instagram Ads, Chatbot, Capcut, Canva
✅ Cursos Virales valorados en 500$
✅ Hailuo Max, Runway Unlimited, Fish Audio Pro
✅ Dreamface, Heygen, Higgsfield
✅ Eleven Labs Ilimitado
✅ Networking con comunidad de emprendedores

DIFERENCIAS:

🎨 VIP 1 (INVESTIGACIÓN Y CREATIVO)
- ChatGPT PRO + Sora PRO 2

💻 VIP 2 (INVESTIGACIÓN Y PROGRAMACIÓN)  
- Claude PRO MAX 20

🚀 VIP 3 (INVESTIGACIÓN Y CREACIÓN DE CONTENIDO)
- Super Grok Heavy"""
    },
    {
        "title": "Regalos Extras del MEGAPACK",
        "category": "promociones",
        "content": """Al contratar el MEGAPACK recibes 3 REGALOS:

🎁 REGALO 1: Acceso a streaming (Disney+, Crunchyroll, IPTV)
🎁 REGALO 2: IA para apuestas deportivas
🎁 REGALO 3: Cursos de Marketing Digital y Monetización con IA

PLUS: Cursos Virales 1000$ GRATIS por promoción
- Desarrollo personal / Finanzas
- Dropshipping / Ecommerce  
- Marketing Digital
- Automatización y Monetización Redes
- Edición de videos
- Cripto/Trading/Apuestas"""
    },
    {
        "title": "IAs Destacadas - Generación de Video",
        "category": "productos",
        "content": """🎥 GENERADORES DE VIDEO TOP:

SORA 2: Lo más sofisticado en generación de videos con sonido. Admite imágenes para dar vida.

VEO 3.1 ULTRA: Junto a Sora 2, lo mejor en generación de video. Admite imágenes para animación.

KLING AI: Plan ilimitado para generación de videos sin restricciones.

RUNWAY: Versión Unlimited incluida en VIP.

HIGGSFIELD: Nueva incorporación VIP. La más potente para efectos cinematográficos."""
    },
    {
        "title": "IAs Destacadas - Académicos",
        "category": "productos",
        "content": """📚 COMBO ACADÉMICO (Ideal para tesis y maestrías):

TURNITIN: Detecta IA y plagio. Sin repositorio (no se guarda en la nube). *Temporalmente en mantenimiento

HUMANIZADORES (Plan Ilimitado):
- WriteHuman
- Humbot  
- JustDone
Verificables con Turnitin para asegurar efectividad.

IAs DE INVESTIGACIÓN:
- Perplexity
- Consensus
- Scribd
Para referencias bibliográficas profesionales."""
    },
    {
        "title": "Productos Individuales Disponibles",
        "category": "productos",
        "content": """IAs INDIVIDUALES (Promoción 20 soles c/u):

• Sora 2
• Turboscribe
• Envato
• Gamma (normalmente 20 soles)
• Turnitin (agotado)
• Veo 3.1
• ChatGPT
• Midjourney

NOTA: Precio normal 25 soles. En promoción 20 soles.

OTROS INDIVIDUALES:

📹 CapCut PRO: 10 soles (privado para app y escritorio)

💬 ChatGPT Plus Personal: 35 soles (con garantía, apto celular y PC)

🎬 Gemini Veo3 Ultra Flow: 40 soles (45,000 créditos, generación ilimitada HD, cuenta personal con garantía)

🎵 Suno (IA música): Incluida GRATIS al unirse al club"""
    },
    {
        "title": "Proceso de Compra y Entrega",
        "category": "proceso",
        "content": """PROCESO DE COMPRA:

1️⃣ Cliente elige plan (MEGAPACK o VIP)
2️⃣ Realiza el pago
3️⃣ IA Club entrega login de acceso (usuario y contraseña)
4️⃣ Cliente accede al ecosistema de 40+ IAs

CARACTERÍSTICAS DEL SERVICIO:
✅ Cuentas personales, libres e ilimitadas
✅ Válidas para celular Y laptop
✅ Licencias oficiales premium
✅ Sin restricciones de uso
✅ Instalación a través de DiCloak
✅ Activación manual por asesores

IMPORTANTE: No es producto físico, no hay entrega a domicilio. Es acceso digital."""
    },
    {
        "title": "Migración de Planes",
        "category": "proceso",
        "content": """MIGRACIÓN DE MEGAPACK A VIP:

Los clientes pueden migrar pagando la diferencia:

Si pagó 30 soles/mes (MEGAPACK):
➡️ Agregar 10 soles = 40 soles/mes (VIP)

Si pagó 50 soles/2 meses:
➡️ Agregar 15 soles por mes = 40 soles/mes cada mes

Si pagó 70 soles/3 meses:  
➡️ Agregar 17 soles por mes = 40 soles/mes cada mes

El plan VIP incluye IAs más sofisticadas + cursos + networking."""
    },
    {
        "title": "Políticas y Garantías",
        "category": "empresa",
        "content": """POLÍTICA DE CALIDAD:

🔄 Reinversión constante: Múltiples membresías de cada IA para evitar saturación y lentitud.

📊 Evidencias: Grupo de WhatsApp con referencias reales de clientes, ventas y renovaciones diarias.

💯 Garantía de precio: Renovaciones mantienen precio promocional.

🔒 Seguridad: Cuentas personales con garantía de funcionamiento.

⚡ Soporte técnico: Disponible para resolver cualquier dificultad con el servicio.

CONTACTO SOPORTE: +51 993 689 365
(Solo para clientes con dificultades técnicas o entregas pendientes)"""
    },
    {
        "title": "Grupo de Referencias WhatsApp",
        "category": "ventas",
        "content": """GRUPO DE REFERENCIAS OFICIAL:
https://chat.whatsapp.com/IumSWrpFzSsCOMdpqIdwoi

PROPÓSITO:
✅ Generar confianza con evidencias reales
✅ Ver renovaciones diarias de clientes satisfechos
✅ Comprobar calidad del servicio
✅ Testimonios reales de usuarios
✅ Aumentar convencimiento de compra

CUÁNDO ENVIARLO:
- Cuando pidan evidencias o pruebas
- Al consultar precios
- Cuando expresen dudas sobre saturación/calidad
- Al despedirse para que lo piensen
- Para tomar decisión con más confianza"""
    }
]

# FAQs
faqs = [
    {
        "question": "¿Qué es IA Club y qué venden?",
        "answer": "IA Club es un club de inteligencias artificiales que vende paquetes de IA. Nuestro producto estrella es el MEGAPACK que incluye más de 40 IAs premium en 3 combos: Asistencia Inteligente, Creación de Contenido, y Educación/Investigación. Precios desde 30 soles/mes. 🚀",
        "category": "general"
    },
    {
        "question": "¿Cuánto cuesta el MEGAPACK?",
        "answer": """PRECIOS PROMOCIONALES MEGAPACK:
• 1 mes: 30 soles
• 2 meses: 50 soles  
• 3 meses: 70 soles

Incluye 40+ IAs premium + 3 regalos extras. Promoción válida hasta fin de mes. ¡Únete al club ahora! 💰""",
        "category": "precios"
    },
    {
        "question": "¿Qué incluye el MEGAPACK?",
        "answer": """El MEGAPACK incluye 3 combos completos:

1️⃣ IAs de Asistencia (ChatGPT, Claude, desarrollo)
2️⃣ IAs Creativas (Sora 2, Veo 3.1, Midjourney, editores)  
3️⃣ IAs Académicas (Turnitin, humanizadores, investigación)

PLUS: 3 regalos (streaming, IA apuestas, cursos). Más de 40 IAs en total.""",
        "category": "productos"
    },
    {
        "question": "¿Cuál es la diferencia entre MEGAPACK y VIP?",
        "answer": """MEGAPACK (30 soles): 40+ IAs en 3 combos + regalos

VIP (40 soles): TODO lo del MEGAPACK + IAs sofisticadas (ChatGPT PRO/Claude MAX 20/Grok Heavy) + cursos premium + networking + herramientas exclusivas como Veo3 Ultra, Runway Unlimited, Heygen, etc.

El VIP es ideal si necesitas lo más avanzado.""",
        "category": "productos"
    },
    {
        "question": "¿Las cuentas son compartidas o personales?",
        "answer": "Todas nuestras cuentas son PERSONALES, libres e ilimitadas para tu uso exclusivo. Válidas para celular Y laptop. Son licencias oficiales premium sin restricciones. 🔐",
        "category": "tecnico"
    },
    {
        "question": "¿Cómo recibo el servicio después de pagar?",
        "answer": "Después del pago, IA Club te entrega tu login personal (usuario y contraseña) para acceder al ecosistema de 40+ IAs. Es acceso digital, no producto físico. Activación rápida por nuestros asesores. ✅",
        "category": "proceso"
    },
    {
        "question": "¿El servicio tiene saturación o es lento?",
        "answer": """Tenemos política de REINVERSIÓN. Mantenemos múltiples membresías de cada IA para evitar saturación y garantizar calidad.

Evidencia: Únete a nuestro grupo de referencias y ve cuántos clientes renuevan diario:
https://chat.whatsapp.com/IumSWrpFzSsCOMdpqIdwoi 📊""",
        "category": "calidad"
    },
    {
        "question": "¿Tienen Sora 2 y Veo 3.1?",
        "answer": "¡Sí! Ambas son nuestras estrellas en generación de video con sonido. Veo 3.1 Ultra y Sora 2 están incluidos en el MEGAPACK. Son las IAs más sofisticadas para crear videos desde texto o dar vida a imágenes. 🎬",
        "category": "productos"
    },
    {
        "question": "¿Tienen Turnitin para detectar IA?",
        "answer": "Sí, Turnitin está incluido en el combo académico. Detecta IA y plagio, sin repositorio (no se guarda en nube). Da opción de descargar reporte completo para subsanar. ⚠️ Temporalmente en mantenimiento. 📚",
        "category": "productos"
    },
    {
        "question": "¿Puedo comprar solo ChatGPT?",
        "answer": """Tienes 2 opciones:

OPCIÓN 1: ChatGPT Plus incluido en MEGAPACK a 30 soles (+ 40 IAs más)
OPCIÓN 2: ChatGPT Plus PERSONAL a 35 soles (solo esa IA, con garantía)

Recomendamos el MEGAPACK por el valor agregado. 💡""",
        "category": "productos"
    },
    {
        "question": "¿Tienen Claude?",
        "answer": """Sí, tenemos Claude en 2 opciones:

OPCIÓN 1: Claude en MEGAPACK (combo 1) a 30 soles
OPCIÓN 2: Claude MAX 20 solo con combo 1 a 30 soles
OPCIÓN 3: Claude PRO MAX 20 en VIP 2 a 40 soles (+ todo el VIP)

Claude es excelente para programación. 💻""",
        "category": "productos"
    },
    {
        "question": "¿Cuándo caduca la promoción?",
        "answer": "La promoción caduca a FIN DE MES. Estos precios especiales no durarán para siempre. ¡Únete al club ahora y asegura tu precio! ⏰⚡",
        "category": "promociones"
    },
    {
        "question": "¿Puedo ver referencias de clientes?",
        "answer": """¡Claro! Únete a nuestro grupo de WhatsApp con referencias REALES:
https://chat.whatsapp.com/IumSWrpFzSsCOMdpqIdwoi

Ahí verás renovaciones diarias, testimonios y evidencias de clientes satisfechos. 🌟""",
        "category": "ventas"
    },
    {
        "question": "¿Tienen página web o redes sociales?",
        "answer": """Síguenos en Facebook para ver reseñas de clientes:
https://www.facebook.com/profile.php?id=61576360997029

También tenemos grupo de WhatsApp con referencias:
https://chat.whatsapp.com/IumSWrpFzSsCOMdpqIdwoi 📱""",
        "category": "general"
    },
    {
        "question": "¿Qué hago si tengo problemas técnicos?",
        "answer": """Para soporte técnico o dificultades con el servicio, contacta directamente:

📞 SOPORTE: +51 993 689 365

Este número se encarga de entregas y resolver cualquier inconveniente técnico. Solo para clientes con dificultades.""",
        "category": "soporte"
    }
]

print(f"Insertando {len(knowledge_items)} items de conocimiento...")
for item in knowledge_items:
    knowledge = Knowledge(**item)
    db.add(knowledge)

print(f"Insertando {len(faqs)} FAQs...")
for item in faqs:
    faq = FAQ(**item)
    db.add(faq)

db.commit()
print("✅ Contenido de IA Club cargado exitosamente!")
print(f"📚 {len(knowledge_items)} items de conocimiento")
print(f"❓ {len(faqs)} FAQs")
print("\nAhora configura los agentes desde el panel admin.")

db.close()
