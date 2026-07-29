# Visualizador Streamlit - Estrategia de Atención Proactiva, 2026

Este proyecto convierte la maqueta del tablero semanal en una aplicación interactiva de Streamlit.

## Estado actual

La estructura general ya está creada y las cuatro pestañas principales ya tienen una primera versión de contenido.

## Qué incluye esta versión

- Título fijo: `Estrategia de Atención Proactiva, 2026`.
- La base de datos se carga siempre desde una ruta fija dentro de `app.py`.
- No se muestra opción para cargar CSV ni para modificar la ruta del archivo.
- Barra lateral con filtros de casillas:
  - Año epidemiológico.
  - Estado.
  - CLUES.
- Cada filtro incluye la opción `Todas`.
- Sin filtro de semana epidemiológica.
- Sin tarjetas superiores de resumen.
- Sin botones manuales de descarga CSV debajo de las tablas.
- Cuatro pestañas:
  - `Indicadores de avance`.
  - `Datos relevantes`.
  - `Intervenciones a los pacientes`.
  - `Acciones de prevención y promoción a la salud`.
- Pestaña `Indicadores de avance` con:
  - Gráfica horizontal apilada de 8 indicadores con marcador de meta.
  - Tabla de numerador, denominador, meta y resultado.
- Pestaña `Datos relevantes` con:
  - Gráfica de pastel y tabla de personas atendidas por grupo de edad.
  - Gráfica de pastel y tabla de personas atendidas por sexo.
  - Tabla de mujeres y puerperio.
  - Tabla de ausentismo.
  - Tabla de personas con discapacidad.
  - Tabla de detecciones.
- Pestaña `Intervenciones a los pacientes` con:
  - Gráfica de barras `Perfiles del personal de Atención Proactiva`.
  - Gráfica de barras `Intervenciones a pacientes con Atención Proactiva`.
  - Gráfica de barras `Población indígena/afromexicana atendida, por grupo`.
  - Gráfica de barras `Población Migrante atendida`.
  - Gráfica de barras `Conclusión de la visita`.
- Pestaña `Acciones de prevención y promoción a la salud` con:
  - Tabla resumen de viviendas, familiares, detecciones, positividad, cuidadores, Zarit-Zarit, pláticas y acciones familiares.
  - Gráfica de barras de pláticas de promoción a la salud.
  - Tabla de distribución porcentual de pláticas de promoción a la salud.

## Ruta de datos

La ruta precargada en `app.py` es:

```text
C:\Users\diego.velazquez.OPDIB\OneDrive - IMSS-BIENESTAR\Documentos\IMSS-B\23 Atención PROACTIVA\Python\base_semanal_unidad_2026.csv
```

Si el archivo se actualiza constantemente con el mismo nombre y ruta, no necesitas tocar el código. La app lee directamente el CSV cada vez que Streamlit ejecuta el script, sin caché en la carga de datos.

Además, el visualizador conserva automáticamente solo registros con `anio_epidemiologico == 2026`.

## Instalación local

Abre PowerShell en esta carpeta:

```powershell
cd C:\Users\diego.velazquez.OPDIB\Documents\Codex\2026-07-20\ten\outputs\visualizador_ap_streamlit
```

Crea y activa un ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instala dependencias:

```powershell
pip install -r requirements.txt
```

Ejecuta el visualizador:

```powershell
streamlit run app.py
```

La URL local usual será:

```text
http://localhost:8501
```

## Publicación en WordPress institucional

Streamlit debe correr como aplicación web independiente. WordPress puede enlazarla o mostrarla mediante un iframe.

Ruta recomendada:

1. Solicitar a infraestructura un subdominio o ruta, por ejemplo:

```text
https://tusitio.gob.mx/ap/
```

2. Instalar Python en el servidor o usar contenedor Docker.
3. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

4. Ejecutar Streamlit como servicio interno:

```powershell
streamlit run app.py --server.port 8501 --server.address 127.0.0.1
```

5. Configurar Apache o Nginx como proxy reverso hacia `127.0.0.1:8501`.
6. En WordPress, agregar:

```html
<iframe src="https://tusitio.gob.mx/ap/" width="100%" height="900" style="border:0;"></iframe>
```
