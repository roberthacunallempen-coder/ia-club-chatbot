# 📋 COMANDOS PARA EJECUTAR EN EL VPS

## 1. Buscar proyectos de EasyPanel
```bash
ls -la /var/lib/easypanel/
```

## 2. Buscar tu proyecto específico
```bash
find /var/lib/easypanel -name "*ia-club*" -type d 2>/dev/null
```

## 3. Listar todos los proyectos
```bash
ls -la /var/lib/easypanel/projects/
```

## 4. Ver estructura completa
```bash
tree -L 2 /var/lib/easypanel/projects/
```

---
**Copia y pega estos comandos uno por uno en la terminal del VPS**
