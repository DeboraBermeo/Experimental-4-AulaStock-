# Evidencias para el informe

Las imágenes de la interfaz incluidas son vistas renderizadas del HTML real devuelto por Django con SQLite auxiliar, no son capturas de VS Code ni de un navegador. No son evidencia de Docker ni GitHub. Inserta las siguientes capturas sin recrear sus interfaces:

1. VS Code: Archivo > Abrir carpeta > AulaStock, abre Explorer con manage.py, project, app, requirements.txt y .github/workflows/ci.yml. En terminal ejecuta `git branch --show-current` para mostrar ci-setup. Pie: estructura del proyecto y rama de configuración.
2. CI: abre Actions, ejecución del commit que vas a entregar, trabajo test y paso Pruebas con PostgreSQL. Captura `Ran 15 tests` y `OK`, junto al nombre del trabajo. Pie: pruebas automáticas de inventario con PostgreSQL.
3. VS Code: abre Dockerfile completo y entrypoint.sh en otra pestaña, muestra python:3.10-slim y ENTRYPOINT. Pie: definición del entorno y preparación del arranque.
4. VS Code: abre docker-compose.yml y ejecuta `docker compose ps` en la terminal. Captura web y db con healthy y el puerto 8000. Pie: servicios Django y PostgreSQL en ejecución.
5. Navegador: abre localhost:8000 con Docker activo y captura el inventario, registra EQ-004 y captura el mensaje de confirmación. Pie: consulta y registro desde el contenedor web.
6. Actions: captura test, build y deploy aprobados, el SHA y la sección Artifacts. Pie: dependencia entre validación, construcción y despliegue del mismo commit.
7. Despliegue externo: terminal en C:\despliegues\aulastock, `docker compose ps` y `Invoke-RestMethod http://localhost:8000/health/`. Pie: validación desde una carpeta distinta del proyecto original.
8. GitHub: portada del repositorio, URL visible, README y archivos. Copia la URL al espacio del informe.

No incluyas el contenido de .env ni datos de acceso en las capturas. Los puestos de autor, integrantes, periodo y fecha de entrega deben completarse con los datos del equipo.
