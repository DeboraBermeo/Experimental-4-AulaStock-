# AulaStock — Flujo CI/CD para Django

Sistema académico de inventario: crear, consultar, editar y eliminar equipos, con código único, categoría y cantidad positiva. Versión 1.1.0. Los registros de `seed_demo` son datos de ejemplo.

## Requisitos
VS Code, Git y Docker Desktop funcionando en modo contenedores Linux, Docker Compose v2 con soporte para `--wait`, cuenta de GitHub. Docker instala Python 3.10 y PostgreSQL 16 dentro de contenedores; no necesitas instalar PostgreSQL en Windows. La interfaz se limita a localhost, es una práctica académica sin autenticación, no debe exponerse públicamente.

## 0. Línea de productos: variantes A y B
AulaStock se entrega como una línea de productos con una sola base de código y dos variantes, elegidas con `PRODUCT_VARIANT` en `.env`:

| Característica | Variante A (básico) | Variante B (completo) |
|---|---|---|
| Inventario CRUD (núcleo, app `app`) | Sí | Sí |
| Reportes y exportación CSV (app `reportes`) | No | Sí |
| Alertas de stock bajo (app `notificaciones`) | No | Sí |

Las variantes se definen en `project/config_product.py`. `settings.py` carga las apps opcionales y `project/urls.py` incluye sus rutas solo si la variante las activa. Para cambiar de variante edita `PRODUCT_VARIANT` en `.env` y ejecuta `docker compose up -d --build --wait`.

Sin Docker: `$env:PRODUCT_VARIANT="A"; python manage.py runserver --settings=project.settings_local` (usa `"B"` para el completo).

Para ver las dos variantes a la vez (dos proyectos de Compose, puertos distintos):
```powershell
$env:PRODUCT_VARIANT="A"; $env:APP_PORT="8001"; docker compose -p aulastock_a up -d --build --wait
$env:PRODUCT_VARIANT="B"; $env:APP_PORT="8002"; docker compose -p aulastock_b up -d --build --wait
```
Variante A en http://localhost:8001 y variante B en http://localhost:8002.

## 1. Abrir y ejecutar en PowerShell
Extrae el ZIP, abre la carpeta AulaStock en VS Code y selecciona Terminal > Nueva terminal. Todos los comandos parten de esa carpeta, donde está manage.py.

```powershell
docker --version
docker compose version
docker info
Copy-Item .env.example .env
code .env
```
En `.env`, cambia DJANGO_SECRET_KEY y POSTGRES_PASSWORD por valores propios, sin espacios; guarda el archivo. `.env` no se sube a GitHub.

```powershell
docker compose config --quiet
docker compose up -d --build --wait --wait-timeout 180
docker compose exec web python manage.py seed_demo
docker compose exec web python manage.py check
docker compose exec web python manage.py test --verbosity 2
docker compose ps
Invoke-RestMethod http://localhost:8000/health/
```
Abre http://localhost:8000 y prueba registrar, editar y eliminar un equipo. Los ejemplos iniciales suman 3 tipos y 17 unidades en una base vacía. Usa EQ-004 para registrar otro equipo, no repitas EQ-001. Para revisar un error: `docker compose logs web` y `docker compose logs db`.

## 2. Subir a GitHub desde VS Code
Crea en GitHub un repositorio vacío llamado `aulastock-cicd`, sin README, licencia ni gitignore. Sustituye TU_USUARIO por tu cuenta real.

```powershell
git init -b main
git config user.name "Tu nombre"
git config user.email "Tu correo de GitHub"
git add .
git commit -m "feat: crear inventario AulaStock y flujo CI CD"
git remote add origin https://github.com/TU_USUARIO/aulastock-cicd.git
git push -u origin main
git switch -c ci-setup
git commit --allow-empty -m "ci: verificar pipeline desde ci-setup"
git push -u origin ci-setup
```
Los comandos de identidad afectan solo a este repositorio. En GitHub abre **Actions > AulaStock CI CD** y espera los tres trabajos `test`, `build` y `deploy`. Si Actions está deshabilitado, habilítalo en el repositorio. No declares una ejecución exitosa si aparece roja: abre el paso fallido y corrige su mensaje. Crea un Pull Request de ci-setup hacia main, revisa los checks y fusiona si corresponde.

La URL para el informe será `https://github.com/TU_USUARIO/aulastock-cicd`, una vez creado. No hay un repositorio remoto creado por este paquete.

## 3. Qué hace el pipeline
- `test`: Python 3.10, instalación de requirements.txt, PostgreSQL de servicio, check, revisión de migraciones y las pruebas (28) en las variantes A y B mediante una matriz. `pipefail` conserva un fallo aunque la salida se copie con tee.
- `build`: depende de test, construye la imagen identificada por el SHA del commit y exporta un TAR y su SHA-256, conserva el artefacto 7 días.
- `deploy`: descarga exactamente ese TAR, verifica su integridad, carga la imagen, copia Compose a una carpeta externa del runner y levanta el sistema sin reconstruir. Comprueba /health/ y /, conserva evidencias y detiene los contenedores al finalizar. Es un entorno temporal de validación, no una web alojada permanentemente.

Ver `deploy-notes.md` para reproducir el despliegue en otra carpeta de Windows y conservarlo abierto para las capturas.

## 4. Estructura
- `manage.py`, `project/`: configuración, rutas y WSGI.
- `app/`: núcleo. Modelo Equipo, formularios, vistas, migración y pruebas.
- `reportes/`: app opcional (variante B). Resumen por categoría y exportación CSV.
- `notificaciones/`: app opcional (variante B). Alertas de stock bajo.
- `project/config_product.py`: definición de las variantes A y B.
- `app/templates/app/`: interfaz HTML sin dependencias externas.
- `Dockerfile`, `entrypoint.sh`: imagen Python 3.10, migraciones al inicio, Gunicorn.
- `docker-compose.yml`: web, PostgreSQL, volumen y healthchecks.
- `.github/workflows/ci.yml`: pruebas, construcción, artefactos y despliegue.
- `evidence/`: registros y capturas locales disponibles, con su alcance.
- `CAPTURAS.md`: instrucciones precisas para evidencias de VS Code, Docker y Actions.

## 5. Validación auxiliar sin Docker
Solo para revisar la interfaz cuando Docker no esté disponible, no sustituye PostgreSQL ni la validación del pipeline.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate --settings=project.settings_local
python manage.py seed_demo --settings=project.settings_local
python manage.py test --settings=project.settings_local --verbosity 2
python manage.py runserver --settings=project.settings_local
```
Si PowerShell bloquea la activación, ejecuta directamente `.\.venv\Scripts\python.exe` en lugar de `python`. Ejecuta los tests desde la carpeta del proyecto, no desde su carpeta padre.

## 6. Versiones y mantenimiento
`VERSION` inicia en 1.0.0, la imagen de CI se etiqueta con el SHA, que identifica exactamente el código construido. Para una entrega revisada, actualiza VERSION y la versión de /health/, registra los cambios y crea `git tag v1.0.0`, luego `git push origin v1.0.0`. El tag debe corresponder al contenido revisado. No subas claves, entornos virtuales, archivos SQLite ni imágenes TAR al repositorio.

## 7. Detener y conservar datos
`docker compose down` detiene el sistema y conserva el volumen. `docker compose up -d --wait` lo inicia otra vez. Evita `down -v` si necesitas conservar el inventario, porque elimina el volumen PostgreSQL.

## Estado de esta entrega
Se ejecutaron 28 pruebas por variante (A: 21 ejecutadas y 7 omitidas por no aplicar; B: 28) con Python 3.12 y SQLite auxiliar, todas satisfactorias, además de check y revisión de migraciones. Docker, PostgreSQL y GitHub Actions deben ejecutarse en el entorno del estudiante; no se incluyen logs inventados de esos servicios. Las imágenes de la interfaz son vistas renderizadas del HTML real devuelto por Django mediante el cliente de pruebas, no son capturas de un navegador ni de VS Code, y no acreditan Docker.
