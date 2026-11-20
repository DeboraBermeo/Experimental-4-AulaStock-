# Despliegue local de AulaStock

## Opción A — Construcción desde otra carpeta
Abre PowerShell fuera del proyecto, sustituye TU_USUARIO por la cuenta donde publicaste el repositorio. Detén antes el proyecto original con `docker compose down` para liberar el puerto 8000.

```powershell
New-Item -ItemType Directory -Force C:\despliegues | Out-Null
Set-Location C:\despliegues
git clone https://github.com/TU_USUARIO/aulastock-cicd.git aulastock
Set-Location aulastock
Copy-Item .env.example .env
code .env
```
Configura claves propias y ejecuta:

```powershell
docker compose up -d --build --wait --wait-timeout 180
docker compose exec web python manage.py seed_demo
docker compose exec web python manage.py test --verbosity 2
docker compose ps
Invoke-RestMethod http://localhost:8000/health/
Start-Process http://localhost:8000
```
Captura la ruta externa, ambos servicios saludables, la respuesta HTTP y la página con registros. Registra el commit con `git rev-parse HEAD`.

## Opción B — Desplegar exactamente la imagen del pipeline
En Actions, abre una ejecución aprobada, descarga `image-<SHA>` y extrae su contenido en la carpeta externa del proyecto. Deben existir `artifacts/aulastock-image.tar` y `artifacts/aulastock-image.tar.sha256`. Desde la raíz:

```powershell
$expectedHash = ((Get-Content artifacts/aulastock-image.tar.sha256) -split ' ')[0]
$actualHash = (Get-FileHash artifacts/aulastock-image.tar -Algorithm SHA256).Hash.ToLower()
if ($actualHash -ne $expectedHash) { throw 'El hash de la imagen no coincide' }
docker load -i artifacts/aulastock-image.tar
$env:APP_IMAGE = 'aulastock:PEGAR_SHA_COMPLETO_DE_LA_EJECUCION'
docker compose up -d --no-build --wait --wait-timeout 180
docker compose exec web python manage.py seed_demo
Invoke-RestMethod http://localhost:8000/health/
```
Sustituye PEGAR_SHA_COMPLETO_DE_LA_EJECUCION por el SHA que se muestra en Actions, no uses el texto literal. Si el ZIP no conserva la carpeta artifacts, créala y mueve los dos archivos allí. Esta opción utiliza la misma imagen construida en CI, la opción A reconstruye desde el código.

## Criterios de aceptación
Ambos servicios están healthy, /health/ devuelve status ok, la página carga, se registra un equipo, sobrevive a `docker compose restart web`, los 15 tests pasan usando PostgreSQL y Actions muestra test, build y deploy aprobados. Adjunta evidencia real de cada criterio antes de afirmar que se verificó.

## Recuperación
Revisar `docker compose logs web` y `docker compose logs db`. Para volver a una versión anterior, descargar su artefacto, verificar el hash, cargarlo y configurar APP_IMAGE con su SHA. Revisar compatibilidad de migraciones y respaldar PostgreSQL antes de cambiar versiones, cambiar la imagen no revierte automáticamente la base.
