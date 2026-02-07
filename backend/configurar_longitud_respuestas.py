"""
Script para configurar la longitud de las respuestas del bot
"""
from sqlalchemy.orm import Session
from app.utils.database import SessionLocal
from app.models.settings import Settings


def configurar_longitud():
    """Configura la longitud de las respuestas del bot"""
    db: Session = SessionLocal()
    
    try:
        print("=" * 60)
        print("CONFIGURACIÓN DE LONGITUD DE RESPUESTAS")
        print("=" * 60)
        print()
        
        # Mostrar opciones
        print("Opciones disponibles:")
        print()
        print("1. CONCISA (Recomendado)")
        print("   - Respuestas muy breves (2-3 oraciones)")
        print("   - Máximo ~150 tokens")
        print("   - Ideal para WhatsApp/chat rápido")
        print("   - Ahorra costos de OpenAI")
        print()
        print("2. NORMAL")
        print("   - Respuestas de longitud media")
        print("   - Máximo ~250 tokens")
        print("   - Balance entre detalle y brevedad")
        print()
        print("3. DETALLADA")
        print("   - Respuestas completas y explicativas")
        print("   - Máximo ~400 tokens")
        print("   - Más contexto y explicaciones")
        print()
        
        opcion = input("Selecciona una opción (1, 2 o 3): ").strip()
        
        if opcion == "1":
            estilo = "concisa"
            max_tokens = 150
            print("\n✓ Configurado: Respuestas CONCISAS (2-3 oraciones)")
        elif opcion == "2":
            estilo = "normal"
            max_tokens = 250
            print("\n✓ Configurado: Respuestas NORMALES (longitud media)")
        elif opcion == "3":
            estilo = "detallada"
            max_tokens = 400
            print("\n✓ Configurado: Respuestas DETALLADAS (completas)")
        else:
            print("\n✗ Opción inválida. Usando CONCISA por defecto.")
            estilo = "concisa"
            max_tokens = 150
        
        # Guardar configuración de estilo
        setting_style = db.query(Settings).filter_by(key="response_style").first()
        if not setting_style:
            setting_style = Settings(
                key="response_style",
                value=estilo,
                category="bot_behavior",
                description="Estilo de longitud de respuestas: concisa, normal, detallada"
            )
            db.add(setting_style)
        else:
            setting_style.value = estilo
        
        # Guardar configuración de tokens
        setting_tokens = db.query(Settings).filter_by(key="max_response_tokens").first()
        if not setting_tokens:
            setting_tokens = Settings(
                key="max_response_tokens",
                value=str(max_tokens),
                category="bot_behavior",
                description="Número máximo de tokens por respuesta"
            )
            db.add(setting_tokens)
        else:
            setting_tokens.value = str(max_tokens)
        
        db.commit()
        
        print(f"✓ Max tokens: {max_tokens}")
        print()
        print("=" * 60)
        print("CONFIGURACIÓN GUARDADA EXITOSAMENTE")
        print("=" * 60)
        print()
        print("Los cambios se aplicarán en las próximas respuestas del bot.")
        print("Si el backend está corriendo, los cambios son automáticos.")
        print()
        
        # Mostrar configuración actual
        print("Configuración actual:")
        print(f"  - Estilo: {estilo.upper()}")
        print(f"  - Max tokens: {max_tokens}")
        print()
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    configurar_longitud()
