========================================
🚀 GUÍA COMPLETA: DESPLEGAR CON SSH + GIT
========================================

## 📋 INFORMACIÓN DE TU PROYECTO

**Servidor:** 31.97.91.222
**Repositorio:** roberthacunallempen-coder/ia-club-chatbot
**Tecnología:** Python (FastAPI) + React (Vite)


## 🔐 PASO 1: PREPARAR GIT LOCALMENTE

### 1.1 Verificar estado de Git
```powershell
git status
```

### 1.2 Si NO tienes Git iniciado:
```powershell
git init
git add .
git commit -m "Initial commit: IA Club Chatbot"
```

### 1.3 Conectar con GitHub
```powershell
git remote add origin https://github.com/roberthacunallempen-coder/ia-club-chatbot.git
git branch -M main
git push -u origin main
```


## 🔌 PASO 2: CONECTAR VS CODE AL VPS

### 2.1 Instalar extensión
1. Ctrl + Shift + X
2. Buscar: **Remote - SSH**
3. Instalar (de Microsoft)

### 2.2 Conectar al servidor
1. **Ctrl + Shift + P**
2. Escribir: `Remote-SSH: Connect to Host`
3. Escribir: `root@31.97.91.222`
4. Enter contraseña cuando la pida
5. Esperar conexión (esquina inferior izquierda debe decir: SSH: 31.97.91.222)


## 📂 PASO 3: UBICAR PROYECTOS DE EASYPANEL

### 3.1 Abrir terminal en VS Code (conectado al VPS)
**Ctrl + Ñ** o **Ctrl + `**

### 3.2 Buscar proyectos de EasyPanel
```bash
# Listar proyectos
ls -la /var/lib/easypanel/

# Buscar tu proyecto específico
find /var/lib/easypanel -name "*ia-club*" -type d
```

**Ruta típica:**
```
/var/lib/easypanel/projects/ia-club-chatbot/
```


## 🛠️ PASO 4: CONFIGURAR GIT EN EL VPS

### 4.1 Instalar Git (si no está)
```bash
apt update
apt install -y git
```

### 4.2 Configurar Git
```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"
```

### 4.3 Configurar acceso a GitHub
```bash
# Opción 1: HTTPS (más fácil)
git config --global credential.helper store

# Opción 2: SSH (más seguro)
ssh-keygen -t ed25519 -C "tu@email.com"
cat ~/.ssh/id_ed25519.pub
# Copiar la clave y añadirla en GitHub → Settings → SSH Keys
```


## 🚀 PASO 5: CLONAR PROYECTO EN EL VPS

### 5.1 Navegar a la carpeta de EasyPanel
```bash
cd /var/lib/easypanel/projects/ia-club-chatbot/
```

### 5.2 Clonar tu repositorio
```bash
# Si usas HTTPS
git clone https://github.com/roberthacunallempen-coder/ia-club-chatbot.git code

# Si usas SSH
git clone git@github.com:roberthacunallempen-coder/ia-club-chatbot.git code
```

### 5.3 Verificar
```bash
cd code
ls -la
```


## ✏️ PASO 6: EDITAR CÓDIGO EN VIVO

### 6.1 Abrir carpeta en VS Code
**File → Open Folder**
```
/var/lib/easypanel/projects/ia-club-chatbot/code
```

### 6.2 Editar archivos
- Edita cualquier archivo
- Guarda con **Ctrl + S**
- Los cambios se reflejan automáticamente

### 6.3 Si no se reflejan los cambios:
```bash
# Ver servicios corriendo
docker ps

# Reiniciar backend
docker restart backend

# Reiniciar frontend
docker restart frontend
```


## 🔄 PASO 7: FLUJO DE TRABAJO CONTINUO

### Trabajar desde tu PC local:
```powershell
# 1. Hacer cambios locales
# 2. Commit
git add .
git commit -m "Descripción del cambio"

# 3. Push a GitHub
git push origin main
```

### Actualizar en el servidor:
```bash
# Conectado al VPS por SSH
cd /var/lib/easypanel/projects/ia-club-chatbot/code

# Pull cambios
git pull origin main

# Reiniciar servicios
docker restart backend frontend
```


## 🎯 PASO 8: CONFIGURAR VARIABLES DE ENTORNO

### 8.1 En EasyPanel (Método recomendado)
1. Ir a: http://31.97.91.222:3000/
2. Seleccionar proyecto: **ia-club-chatbot**
3. Click en servicio: **backend**
4. Pestaña: **Environment**
5. Editar variables según necesites

### 8.2 Directamente en el VPS (Alternativa)
```bash
cd /var/lib/easypanel/projects/ia-club-chatbot/code

# Crear .env
nano .env

# Pegar configuración (ver EASYPANEL_CONFIG.txt)
```


## 🔍 PASO 9: MONITOREAR Y DEBUGGEAR

### Ver logs en vivo:
```bash
# Backend
docker logs -f backend

# Frontend
docker logs -f frontend

# PostgreSQL
docker logs -f postgres

# Redis
docker logs -f redis
```

### Entrar a un contenedor:
```bash
# Backend
docker exec -it backend bash

# Ver archivos
ls -la

# Ver procesos
ps aux
```


## 📊 PASO 10: VERIFICAR FUNCIONAMIENTO

### 10.1 Endpoints a probar:
```bash
# Health check backend
curl http://localhost:8000/health

# Docs API
curl http://localhost:8000/docs
```

### 10.2 Desde navegador:
- **Frontend:** http://31.97.91.222:PUERTO_FRONTEND
- **Backend API:** http://31.97.91.222:PUERTO_BACKEND/docs


## ⚡ COMANDOS RÁPIDOS ÚTILES

```bash
# Ver todos los contenedores
docker ps -a

# Ver uso de recursos
docker stats

# Reiniciar todo el proyecto
cd /var/lib/easypanel/projects/ia-club-chatbot/code
docker-compose restart

# Ver logs de todos los servicios
docker-compose logs -f

# Rebuild después de cambios importantes
docker-compose up -d --build
```


## 🚨 SOLUCIÓN DE PROBLEMAS COMUNES

### Problema: No puedo conectar por SSH
```bash
# En tu PC local
ssh -v root@31.97.91.222
# Ver detalles del error
```

### Problema: Git pide contraseña cada vez
```bash
# En el VPS
git config --global credential.helper store
git pull  # Ingresar credenciales una vez
```

### Problema: Cambios no se reflejan
```bash
# Limpiar caché de Docker
docker system prune -a
docker-compose up -d --build
```

### Problema: Puerto ocupado
```bash
# Ver qué usa el puerto
netstat -tulpn | grep :8000

# Matar proceso
kill -9 PID
```


## 🎓 MEJORES PRÁCTICAS

### ✅ HACER:
- ✅ Trabajar en una rama de desarrollo: `git checkout -b develop`
- ✅ Hacer commits frecuentes y descriptivos
- ✅ Probar cambios localmente antes de push
- ✅ Revisar logs después de cada deploy
- ✅ Hacer backups de la base de datos

### ❌ NO HACER:
- ❌ Editar directamente en producción sin Git
- ❌ Hacer `git push --force` en main
- ❌ Borrar contenedores sin backup
- ❌ Exponer credenciales en el código
- ❌ Trabajar como root (crear usuario dev)


## 🔐 CREAR USUARIO NO-ROOT (RECOMENDADO)

```bash
# Crear usuario dev
adduser dev

# Dar permisos de Docker
usermod -aG docker dev

# Dar permisos de sudo
usermod -aG sudo dev

# Cambiar a usuario dev
su - dev

# Ahora trabajar como dev en vez de root
```


## 📝 ESTRUCTURA FINAL EN EL VPS

```
/var/lib/easypanel/projects/ia-club-chatbot/
├── code/                    ← TU CÓDIGO (EDITABLE)
│   ├── backend/
│   ├── frontend/
│   ├── docker-compose.yml
│   └── .git/               ← CONTROL DE VERSIONES
├── volumes/                 ← DATOS PERSISTENTES
│   ├── postgres/
│   └── redis/
└── .env                     ← VARIABLES DE ENTORNO
```


## 🎯 PRÓXIMOS PASOS

1. ✅ Conectar VS Code al VPS
2. ✅ Clonar tu repositorio
3. ✅ Configurar variables de entorno
4. ✅ Verificar que todo funcione
5. ✅ Hacer tu primer cambio y push
6. ✅ Configurar Chatwoot


========================================
¿NECESITAS AYUDA?
Guárdame los logs o pantallazos de errores
========================================
