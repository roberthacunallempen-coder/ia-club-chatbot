# 🚀 INICIO RÁPIDO - DESARROLLO LOCAL

## 📋 Pre-requisitos Instalados

- Python 3.10+
- Node.js 18+
- PostgreSQL 15+
- Redis
- Docker Desktop (opcional pero recomendado)

---

## ⚡ OPCIÓN 1: Con Docker (RECOMENDADO)

### 1. Clonar y configurar

```bash
cd "c:\Users\Guerr\Music\BOT PYTHON + CHATWOOT"
cp .env.example .env.local
```

Edita `.env.local` con tus credenciales.

### 2. Levantar todo

```bash
docker-compose up -d
```

### 3. Inicializar base de datos

```bash
docker-compose exec backend alembic upgrade head
```

### 4. Acceder

- **Frontend:** http://localhost
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

---

## 🔧 OPCIÓN 2: Sin Docker (Manual)

### Backend

```bash
cd backend

# Crear virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt

# Configurar .env.local
cp ..\.env.example .env.local
# Editar .env.local

# Inicializar base de datos
alembic upgrade head

# Ejecutar
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Ejecutar
npm run dev
```

Accede a: http://localhost:5173

---

## 🧪 Probar el Sistema

### 1. Crear conocimiento de prueba

```bash
curl -X POST http://localhost:8000/api/knowledge \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Horario de atención",
    "category": "General",
    "content": "Atendemos de lunes a viernes de 9 AM a 6 PM",
    "keywords": ["horario", "atención", "horas"],
    "priority": 10,
    "is_active": true
  }'
```

### 2. Probar bot

```bash
curl -X POST http://localhost:8000/api/test/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "¿Cuál es su horario?",
    "conversation_history": []
  }'
```

---

## 📊 Comandos Útiles

```bash
# Ver logs
docker-compose logs -f

# Reiniciar servicios
docker-compose restart

# Detener todo
docker-compose down

# Limpiar todo (¡CUIDADO! Borra datos)
docker-compose down -v

# Crear migración
docker-compose exec backend alembic revision --autogenerate -m "descripción"

# Aplicar migraciones
docker-compose exec backend alembic upgrade head
```

---

## 🎯 Próximos Pasos

1. ✅ Agregar más conocimientos desde el panel
2. ✅ Crear FAQs
3. ✅ Subir documentos
4. ✅ Configurar webhook de Chatwoot
5. ✅ Desplegar a producción (ver DEPLOYMENT_GUIDE.md)

---

¡Listo para desarrollar! 🎉
