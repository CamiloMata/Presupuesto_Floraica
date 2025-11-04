📊 Dashboard de Presupuesto 2026 - FLORAICA

📝 Descripción
Este proyecto es un dashboard interactivo creado con Streamlit para visualizar y analizar el Presupuesto 2026 de FLORAICA.

La aplicación carga datos desde un archivo CSV, presenta los indicadores clave (KPIs) de ingresos, egresos y resultado neto, y permite un análisis detallado mediante gráficos dinámicos. Los usuarios pueden ver la vista "General" o filtrar por un "Área" específica para profundizar en los datos.

🚀 Características Principales
KPIs Generales: Muestra los totales de Ingresos, Egresos y Resultado Neto (en millones).

Filtro por Área: Un menú desplegable en la barra lateral permite seleccionar una vista "General" o filtrar por cualquier área de la compañía.

Gráficos Interactivos (Plotly):

Ingresos: Gráficos de pastel (por Rubro) y de barras (por Área).

Egresos: Gráficos de pastel (por Rubro) y de barras (por Área).

Análisis de Pareto: Cuando se selecciona un área, se activa una pestaña con un análisis 80/20, mostrando los CECOs que representan el 80% del gasto (excluyendo nómina).

Diseño Personalizado:

Incluye un fondo de pantalla (flowers.png) y el logo de FLORAICA (logo_floraica.png).

El texto es blanco para asegurar la legibilidad sobre el fondo.

Diseño Responsivo (Mobile-Friendly): El dashboard se adapta automáticamente a pantallas pequeñas (móviles y tablets), apilando las columnas verticalmente para una mejor visualización.

Lógica de Negocio (Ceniflores): Los KPIs generales excluyen los ingresos provenientes del área "Investigación y Desarrollo Floral" (Ceniflores) para mostrar un resultado neto operativo más preciso. Sin embargo, al filtrar por esa área, sí se pueden ver sus ingresos y egresos completos.

📂 Archivos Requeridos
Para que el dashboard funcione correctamente, asegúrate de que los siguientes archivos estén en la misma carpeta que el script dashboard.py:

dashboard.py: (Este script).

presupuesto2025.csv: El archivo principal con los datos del presupuesto.

logo_floraica.png: El logo de la empresa.

flowers.png: La imagen de fondo.

(Nota: El script también intenta cargar expo.csv y salarios.csv, pero estas líneas están actualmente comentadas en el código. Si se descomentan, esos archivos también serían necesarios).

🛠️ Instalación
Abre una terminal o línea de comandos.

Navega al directorio donde guardaste los archivos del proyecto:

Bash

cd ruta/a/tu/proyecto
(Recomendado) Crea un entorno virtual para aislar las dependencias:

Bash

python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
Instala las librerías necesarias:

Bash

pip install streamlit pandas plotly-express
▶️ Ejecución
Asegúrate de estar en la terminal, dentro de la carpeta del proyecto y con tu entorno virtual activado.

Ejecuta el siguiente comando:

Bash

streamlit run dashboard.py

Otro camino para ejecutar es: python -m streamlit run dashboard.py

Streamlit abrirá automáticamente el dashboard en tu navegador web.
