# 🧹 Mantenimiento VACUUM Paralelo para PostgreSQL

Este proyecto ejecuta comandos `VACUUM` de manera paralela en una base de datos PostgreSQL, permitiendo mantenimiento eficiente y concurrente a través de múltiples conexiones.

---

## ⚙️ Requisitos

- Python 3.8 o superior
- PostgreSQL en ejecución
- pip
- virtualenv (recomendado)

---

## 🔧 Instalación y Ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu_usuario/mtto.git
cd mtto
```

### 2. Crear el entorno virtual (git y virtualenv) 

```bash
python -m virtualenv ven_mtto
```

### 3. Activar el entorno virtual(En Git Bash o PowerShell)
```bash
source ven_mtto/Scripts/activate
```

### 4. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 5. Crear y configurar el archivo .env

Debes crear un archivo .env en la raíz del proyecto con las siguientes variables:

```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=db_name
DB_USER=user
DB_PASSWORD=ABC123
SQL_FILE=D:/mymtto/query_mtto.sql
LOG_FILE=D:/mymtto/query_mtto.log
MAX_CONNECTIONS=15
```

## 6. Ejecutar el script principal

```bash
python run.py
```