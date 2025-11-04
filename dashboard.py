# dashboard.py

import streamlit as st
import pandas as pd
import plotly.express as px
import textwrap
import base64

# --- Page Configuration ---
st.set_page_config(layout="wide")

# --- Function to Inject All Custom CSS ---
def inject_custom_css(image_file):
    """
    Injects CSS to set a background image and ensures all text is white for readability.
    Includes responsive CSS for fonts and layout.
    """
    try:
        with open(image_file, "rb") as f:
            img_bytes = f.read()
        encoded_img = base64.b64encode(img_bytes).decode()
        
        # --- MODIFICACIÓN RESPONSIVA ---
        # Se ha reescrito la etiqueta <style> para incluir 'clamp()' para fuentes
        # y una '@media query' para el apilamiento en móviles.
        st.markdown(
            f"""
            <style>
            /* --- Background Image --- */
            .stApp {{
                background-image: url("data:image/png;base64,{encoded_img}");
                background-size: cover !important;
                background-repeat: no-repeat !important;
                background-attachment: fixed;
            }}

            /* --- General White Text & RESPONSIVE Font Sizes --- */
            .stApp, .stApp h1, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {{
                color: white !important;
            }}
            
            /* Usamos clamp(MIN, PREFERIDO, MAX) para fuentes responsivas */
            h1 {{ font-size: clamp(2.2rem, 5vw, 3rem) !important; }}
            h3 {{ font-size: clamp(1.2rem, 3vw, 1.5rem) !important; }}
            h4 {{ font-size: clamp(1rem, 2.5vw, 1.25rem) !important; }}
            
            /* --- RESPONSIVE KPI Metrics (usando Clases) --- */
            .kpi-label {{
                font-size: clamp(1rem, 2.5vw, 1.5rem) !important;
                color: white !important;
                opacity: 1;
                font-weight: 700;
                margin-bottom: -10px; /* Ajusta el espacio entre etiqueta y valor */
            }}
            .kpi-value {{
                font-size: clamp(1.5rem, 4vw, 2.2rem) !important;
                color: white !important;
                font-weight: 800;
            }}

            /* Estilos de st.metric (por si se usan) */
            div[data-testid="stMetricLabel"] > div {{
                color: white !important;
            }}
            div[data-testid="stMetricValue"] {{
                color: white !important;
            }}

            /* --- Tabs --- */
            button[data-baseweb="tab"] {{
                color: white;
                background-color: transparent !important;
                font-size: clamp(0.9rem, 2vw, 1.1rem); /* Tabs responsivos */
            }}
            button[data-baseweb="tab"][aria-selected="true"] {{
                color: white;
                font-weight: bold;
            }}
            .stTabs [data-baseweb="tab-list"] {{
                border-bottom-color: rgba(255, 255, 255, 0.3) !important;
            }}
            
            /* --- Keep text in info/warning boxes readable --- */
            .st-emotion-cache-1wivapv p, .st-emotion-cache-1e5k5j6 p {{
                color: black !important;
            }}

            /* --- MEDIA QUERY PARA RESPONSIVIDAD MÓVIL ---
            Si el ancho de la pantalla es 768px o menos (móviles/tablets pequeñas)
            */
            @media (max-width: 768px) {{
                
                /* Apila las columnas (st.columns) verticalmente */
                div[data-testid="stHorizontalBlock"] {{
                    flex-direction: column !important;
                    align-items: stretch !important;
                }}
                
                /* Asegura que cada columna apilada ocupe el 100% del ancho */
                div[data-girdle-container] > div[data-testid="stVerticalBlock"] {{
                    width: 100% !important;
                    margin-bottom: 20px; /* Espacio entre bloques apilados */
                }}

                /* Achica el logo en móviles */
                .stImage img {{
                    width: 150px !important;
                }}

                /* Centra el título en móviles */
                h1 {{
                    margin-top: 0px !important;
                    text-align: center !important;
                }}

                /* Apila las columnas anidadas (Gráfico/Tabla) */
                div[data-testid="stHorizontalBlock"] div[data-testid="stHorizontalBlock"] {{
                     flex-direction: column !important;
                }}
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.warning(f"Advertencia: No se encontró la imagen de fondo '{image_file}'.")

# --- Data Loading and Caching ---
@st.cache_data
def load_data(file_path):
    """
    Loads the main budget data from the csv file.
    """
    try:
        # --- MODIFICACIÓN: Usamos el nombre de archivo que subiste 'presupuesto20251.csv' ---
        # Asegúrate de que el delimitador es correcto, tu archivo usa ';'
        df = pd.read_csv(file_path, delimiter=';', engine='python', on_bad_lines='skip')
        df.columns = df.columns.str.strip()
        
        # --- MODIFICACIÓN: Ajuste de columnas requeridas según tu CSV ---
        # Tu CSV tiene 'Area' (con tilde)
        required_cols = ['Tipo', 'Rubro', 'Area', 'Presupuesto 2025', 'Nombre Ceco']
        
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            st.error(f"Error Crítico: Faltan las siguientes columnas requeridas: {', '.join(missing_cols)}")
            st.info(f"Las columnas encontradas son: {', '.join(df.columns)}")
            return pd.DataFrame()

        df_selection = df[required_cols].copy()
        
        # Limpieza de la columna de presupuesto
        df_selection['Presupuesto 2025'] = df_selection['Presupuesto 2025'].astype(str).str.replace('[$.]', '', regex=True).str.replace(',', '.', regex=False)
        df_selection['Presupuesto 2025'] = pd.to_numeric(df_selection['Presupuesto 2025'], errors='coerce').fillna(0)
        
        # Limpieza de columnas de texto
        df_selection['Tipo'] = df_selection['Tipo'].fillna('N/A').str.strip()
        df_selection['Rubro'] = df_selection['Rubro'].fillna('N/A').str.strip()
        df_selection['Area'] = df_selection['Area'].fillna('N/A').str.strip()
        df_selection['Nombre Ceco'] = df_selection['Nombre Ceco'].fillna('N/A').str.strip()
        
        return df_selection
        
    except FileNotFoundError:
        st.error(f"Error: No se encontró el archivo '{file_path}'.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Ocurrió un error inesperado al cargar los datos: {e}")
        return pd.DataFrame()

@st.cache_data
def load_arguments_data(file_path):
    """
    Loads and cleans the arguments data from expo.csv.
    """
    try:
        df_args = pd.read_csv(file_path, delimiter=';', on_bad_lines='warn')
        df_args.columns = df_args.columns.str.strip()
        
        df_args = df_args.rename(columns={"Area": "Area", "Tipo": "Tipo Argumento", "Argumento": "Texto Argumento"})
        
        if 'Area' in df_args.columns:
            df_args['Area'] = df_args['Area'].str.strip()
        if 'Tipo Argumento' in df_args.columns:
            df_args['Tipo Argumento'] = df_args['Tipo Argumento'].str.strip()
            
        return df_args
    except FileNotFoundError:
        st.warning(f"Advertencia: No se encontró el archivo de argumentos '{file_path}'.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error al cargar los datos de argumentos: {e}")
        return pd.DataFrame()

@st.cache_data
def load_salaries_data(file_path):
    """
    Loads, cleans, and prepares the salaries data from salarios.csv.
    """
    try:
        df_sal = pd.read_csv(file_path, delimiter=';')
        df_sal.columns = df_sal.columns.str.strip()
        
        required = ['Nombre', 'Cargo', 'Salario', 'Area']
        if not all(col in df_sal.columns for col in required):
            st.error("El archivo 'salarios.csv' no contiene las columnas requeridas: 'Nombre', 'Cargo', 'Salario', 'Area'.")
            return pd.DataFrame()
            
        df_sal['Salario'] = pd.to_numeric(df_sal['Salario'], errors='coerce').fillna(0)
        df_sal['Area'] = df_sal['Area'].str.strip()
        
        return df_sal
    except FileNotFoundError:
        st.warning(f"Advertencia: No se encontró el archivo de salarios '{file_path}'. La pestaña 'Salarios' no tendrá datos.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Error al cargar los datos de salarios: {e}")
        return pd.DataFrame()

# --- Analysis Function ---
def perform_pareto_analysis(data_df):
    """
    Performs a Pareto (80/20) analysis to find the top items
    that constitute 80% of the total budget.
    """
    analysis_df = data_df[
        (data_df['Rubro'] != 'Personal') &
        (data_df['Tipo'] != 'Ingresos') &
        (data_df['Presupuesto 2025'] > 0)
    ].copy()

    if analysis_df.empty:
        return pd.DataFrame(columns=['Nombre Ceco', 'Presupuesto 2025']) 

    sorted_df = analysis_df.sort_values(by='Presupuesto 2025', ascending=False)

    total_budget = sorted_df['Presupuesto 2025'].sum()
    target_80_percent = total_budget * 0.80

    sorted_df['Cumulative Sum'] = sorted_df['Presupuesto 2025'].cumsum()

    cutoff_index = sorted_df[sorted_df['Cumulative Sum'] >= target_80_percent].index
    
    if len(cutoff_index) > 0:
        pareto_df = sorted_df.loc[:cutoff_index[0]]
    else:
        pareto_df = sorted_df
    
    return pareto_df[['Nombre Ceco', 'Presupuesto 2025']] 

# --- Helper Functions ---
def format_currency_millions(value):
    if not isinstance(value, (int, float)) or value == 0:
        return "$0"
    value_in_millions = round(value / 1_000_000)
    formatted_string = f"${value_in_millions:,.0f}".replace(',', '.')
    return formatted_string

def wrap_labels(label, length=25):
    wrapped_text = textwrap.wrap(label, length, break_long_words=False)
    return '<br>'.join(wrapped_text)

def style_dataframe(df, currency_column=None):
    """
    Applies custom styling to any DataFrame for display in Streamlit.
    """
    # --- MODIFICACIÓN RESPONSIVA ---
    # Usamos clamp() para el tamaño de fuente de la tabla
    font_size_responsive = "clamp(0.8rem, 2vw, 1rem)"
    
    styler = df.style.set_properties(**{
        'background-color': '#b5dbc3', 'color': 'black',
        'font-size': font_size_responsive, # <-- Aplicado aquí
        'text-align': 'left', 'white-space': 'normal'
    }).set_table_styles([
        {'selector': 'th', 'props': [
            ('font-weight', 'bold'), ('text-align', 'center'),
            ('background-color', '#a4c7b1'), ('color', 'black'),
            ('font-size', font_size_responsive) # <-- Y aplicado aquí
        ]},
        {'selector': 'tbody tr:nth-child(even)', 'props': [('background-color', '#cce3d5')]}
    ]).hide(axis="index")
    
    if currency_column and currency_column in df.columns:
        styler = styler.format({currency_column: '${:,.0f}'})
        
    return styler

# --- Main Dashboard ---
# --- MODIFICACIÓN: Apuntamos al archivo CSV que subiste ---
data_file = 'presupuesto2025.csv' 
##arguments_file = 'expo.csv'
logo_file = 'logo_floraica.png'
background_image_file = 'flowers.png'
##salaries_file = 'salarios.csv'

inject_custom_css(background_image_file)
df = load_data(data_file)
##df_arguments = load_arguments_data(arguments_file)
##df_salaries = load_salaries_data(salaries_file)

if not df.empty:
    
    # --- NUEVO: Filtro Avanzado Ceniflores ---
    # 1. Identificar los ingresos de Ceniflores
    mask_ceniflores_ingresos = (df['Area'] == 'Investigación y Desarrollo Floral') & (df['Tipo'] == 'Ingresos')
    
    # 2. Guardar estos ingresos por separado para uso futuro (como "información complementaria")
    df_ceniflores_ingresos = df[mask_ceniflores_ingresos].copy()
    total_ceniflores_ingresos = df_ceniflores_ingresos['Presupuesto 2025'].sum()
    
    # 3. Crear el DataFrame principal del dashboard excluyendo esos ingresos
    # El operador ~ (tilde) invierte la máscara, seleccionando TODO MENOS los ingresos de Ceniflores
    df_main = df[~mask_ceniflores_ingresos].copy()
    
    # NOTA: 'df' se usará para el filtro de sidebar y vistas detalladas.
    # 'df_main' se usará para los KPIs y la vista "General".
    
    # --- Title and Logo Section ---
    col1, col2 = st.columns([1, 4]) # Esta proporción se mantendrá, pero se apilará en móvil
    with col1:
        try:
            st.image(logo_file, width=160)
        except Exception:
            st.warning(f"No se encontró el logo '{logo_file}'.")
    with col2:
        st.markdown("<h1 style='text-align: center; margin-top: -15px;'>PRESUPUESTO 2026</h1>", unsafe_allow_html=True)

    # --- Sidebar and Filters ---
    st.sidebar.header("Filtros")
    
    # --- MODIFICACIÓN: Usamos 'df' (el original) para asegurar que todas las áreas aparezcan en el filtro ---
    all_areas = sorted(df['Area'].unique())
    options_for_select = ["General"] + all_areas

    selected_area = st.sidebar.selectbox(
        "Seleccione un Área para ver el detalle",
        options=options_for_select,
        index=0 
    )

    # --- Calculate Grand Totals ---
    # --- MODIFICACIÓN: Usamos 'df_main' para los cálculos totales ---
    total_ingresos = df_main[df_main['Tipo'] == 'Ingresos']['Presupuesto 2025'].sum()
    total_egresos = df_main[df_main['Tipo'] == 'Egresos']['Presupuesto 2025'].sum()
    resultado_neto = total_ingresos - total_egresos

    # --- Display Grand Totals in KPIs ---
    st.markdown("<h3 style='margin-top: -10px;'>TOTALES GENERALES (en millones de $)</h3>", unsafe_allow_html=True)
    
    kpi1, kpi2, kpi3 = st.columns(3) # Estas columnas se apilarán en móvil
    with kpi1:
        st.markdown(f"<p class='kpi-label'>INGRESOS TOTALES</p>", unsafe_allow_html=True)
        # Este KPI ahora excluye los ingresos de Ceniflores
        st.markdown(f"<p class='kpi-value'>{format_currency_millions(total_ingresos)}</p>", unsafe_allow_html=True)
    with kpi2:
        st.markdown(f"<p class='kpi-label'>EGRESOS TOTALES</p>", unsafe_allow_html=True)
        st.markdown(f"<p class='kpi-value'>{format_currency_millions(total_egresos)}</p>", unsafe_allow_html=True)
    with kpi3:
        st.markdown(f"<p class='kpi-label'>RESULTADO NETO</p>", unsafe_allow_html=True)
        # Este resultado también se ve afectado, ya que 'total_ingresos' cambió
        st.markdown(f"<p class='kpi-value'>{format_currency_millions(resultado_neto)}</p>", unsafe_allow_html=True)

      

    
    st.markdown("---")
    
    # --- Filter data for the visual components ---
    if selected_area == "General":
        # --- MODIFICACIÓN: La vista "General" usa df_main (sin ingresos Ceniflores) ---
        filtered_df = df_main.copy()
        st.subheader("Detalle General (en millones de $)")
    else:
        # --- MODIFICACIÓN: Las vistas detalladas (incl. Ceniflores) usan el 'df' original ---
        # Esto permite que al seleccionar "Ceniflores", se muestren SUS ingresos y egresos.
        filtered_df = df[df['Area'] == selected_area]
        st.subheader(f"Detalle para: {selected_area} (en millones de $)")

    green_color_scale = px.colors.sequential.YlGnBu

    # --- ROW 1: INGRESOS ---
    ing_left, ing_right = st.columns([1.2, 1])
    with ing_left:
        st.markdown("#### Detalle de Ingresos por Rubro")
        df_ingresos = filtered_df[filtered_df['Tipo'] == 'Ingresos']
        ingresos_por_rubro = df_ingresos.groupby('Rubro')['Presupuesto 2025'].sum().nlargest(6).reset_index()
        if not ingresos_por_rubro.empty and ingresos_por_rubro['Presupuesto 2025'].sum() > 0:
            pie_col, table_col = st.columns([3, 1.2]) # Columnas anidadas
            with pie_col:
                ingresos_por_rubro['Rubro_wrapped'] = ingresos_por_rubro['Rubro'].apply(wrap_labels)
                fig_ingresos = px.pie(ingresos_por_rubro, names='Rubro_wrapped', values='Presupuesto 2025', hole=0.5, color_discrete_sequence=green_color_scale)
                
                fig_ingresos.update_traces(textposition='outside', textinfo='percent+label', textfont=dict(color='white'))
                
                fig_ingresos.update_layout(
                    margin=dict(t=80, b=80, l=40, r=40), 
                    showlegend=False, 
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_ingresos, use_container_width=True)
            with table_col:
                st.markdown("<div style='padding-top: 30px;'></div>", unsafe_allow_html=True)
                ingresos_table = ingresos_por_rubro.copy()
                ingresos_table['Monto (M)'] = ingresos_table['Presupuesto 2025'].apply(format_currency_millions)
                ingresos_table.rename(columns={'Rubro': 'Categoría'}, inplace=True)
                styled_ingresos = style_dataframe(ingresos_table[['Categoría', 'Monto (M)']])
                st.markdown(styled_ingresos.to_html(), unsafe_allow_html=True)
        else:
            st.info("No hay datos de ingresos por rubro para mostrar.")

    with ing_right:
        st.markdown("#### Detalle de Ingresos por Área")
        df_ingresos_area = filtered_df[filtered_df['Tipo'] == 'Ingresos']
        
        # --- MODIFICACIÓN: Aseguramos que 'Area' esté presente antes de agrupar ---
        if 'Area' in df_ingresos_area.columns:
            ingresos_por_area = df_ingresos_area[df_ingresos_area['Presupuesto 2025'] > 0].groupby('Area')['Presupuesto 2025'].sum().sort_values(ascending=True).reset_index()
            
            if not ingresos_por_area.empty:
                ingresos_por_area['Ppto_millones'] = ingresos_por_area['Presupuesto 2025'] / 1_000_000
                ingresos_por_area['Ppto_millones_str'] = ingresos_por_area['Presupuesto 2025'].apply(format_currency_millions)
                max_value_ing = ingresos_por_area['Ppto_millones'].max()
                chart_height_ing = len(ingresos_por_area) * 35 + 60
                fig_ingresos_area = px.bar(ingresos_por_area, x='Ppto_millones', y='Area', text='Ppto_millones_str', orientation='h', color_discrete_sequence=green_color_scale)
                
                fig_ingresos_area.update_traces(texttemplate='%{text}', textposition='outside', textfont=dict(color='white'))
                
                fig_ingresos_area.update_layout(
                    xaxis=dict(showticklabels=False, showgrid=False, range=[0, max_value_ing * 1.25]),
                    xaxis_title=None, yaxis_title=None, height=chart_height_ing,
                    margin=dict(t=25, b=0, r=60), 
                    yaxis=dict(tickfont=dict(color='white'), automargin=True),
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                
                st.plotly_chart(fig_ingresos_area, use_container_width=True)
            else:
                st.info("No hay datos de ingresos por área para mostrar.")
        else:
             st.info("No hay datos de ingresos por área para mostrar.")

    st.markdown("---")

    # --- ROW 2: EGRESOS ---
    egr_left, egr_right = st.columns([1.2, 1])
    with egr_left:
        st.markdown("#### Detalle de Egresos por Rubro")
        df_egresos = filtered_df[filtered_df['Tipo'] == 'Egresos']
        egresos_por_rubro = df_egresos.groupby('Rubro')['Presupuesto 2025'].sum().nlargest(5).reset_index()
        if not egresos_por_rubro.empty and egresos_por_rubro['Presupuesto 2025'].sum() > 0:
            pie_col, table_col = st.columns([3, 1.2]) # Columnas anidadas
            with pie_col:
                egresos_por_rubro['Rubro_wrapped'] = egresos_por_rubro['Rubro'].apply(wrap_labels)
                fig_egresos = px.pie(egresos_por_rubro, names='Rubro_wrapped', values='Presupuesto 2025', hole=0.5, color_discrete_sequence=green_color_scale)
                
                fig_egresos.update_traces(textposition='outside', textinfo='percent+label', textfont=dict(color='white'))
                
                fig_egresos.update_layout(
                    margin=dict(t=80, b=80, l=40, r=40), 
                    showlegend=False, 
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_egresos, use_container_width=True)
            with table_col:
                st.markdown("<div style='padding-top: 30px;'></div>", unsafe_allow_html=True)
                egresos_table = egresos_por_rubro.copy()
                egresos_table['Monto (M)'] = egresos_table['Presupuesto 2025'].apply(format_currency_millions)
                egresos_table.rename(columns={'Rubro': 'Categoría'}, inplace=True)
                styled_egresos = style_dataframe(egresos_table[['Categoría', 'Monto (M)']])
                st.markdown(styled_egresos.to_html(), unsafe_allow_html=True)
        else:
            st.info("No hay datos de egresos por rubro para mostrar.")

    with egr_right:
        st.markdown("#### Detalle de Egresos por Área")
        df_egresos_area = filtered_df[filtered_df['Tipo'] == 'Egresos']
        
        # --- MODIFICACIÓN: Aseguramos que 'Area' esté presente antes de agrupar ---
        if 'Area' in df_egresos_area.columns:
            gastos_por_area = df_egresos_area.groupby('Area')['Presupuesto 2025'].sum().sort_values(ascending=True).reset_index()
            gastos_por_area = gastos_por_area[gastos_por_area['Presupuesto 2025'] > 0]
            
            if not gastos_por_area.empty:
                gastos_por_area['Ppto_millones'] = gastos_por_area['Presupuesto 2025'] / 1_000_000
                gastos_por_area['Ppto_millones_str'] = gastos_por_area['Presupuesto 2025'].apply(format_currency_millions)
                max_value_eg = gastos_por_area['Ppto_millones'].max()
                chart_height_eg = len(gastos_por_area) * 35 + 60
                fig_gastos_area = px.bar(gastos_por_area, x='Ppto_millones', y='Area', text='Ppto_millones_str', orientation='h', color_discrete_sequence=green_color_scale)
                
                fig_gastos_area.update_traces(texttemplate='%{text}', textposition='outside', textfont=dict(color='white'))
                
                fig_gastos_area.update_layout(
                    xaxis=dict(showticklabels=False, showgrid=False, range=[0, max_value_eg * 1.25]),
                    xaxis_title=dict(text=None, font=dict(color='white')), 
                    yaxis_title=None, height=chart_height_eg,
                    margin=dict(t=25, b=25, r=60),
                    yaxis=dict(tickfont=dict(color='white'), automargin=True),
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                
                st.plotly_chart(fig_gastos_area, use_container_width=True)
            else:
                st.info("No hay datos de egresos por área para mostrar.")
        else:
            st.info("No hay datos de egresos por área para mostrar.")
            
    # --- CONDITIONAL SECTIONS ---
    if selected_area != "General":
        st.markdown("---")
        st.subheader(f"Análisis de Pareto para: {selected_area}")
        
        tab1 = st.tabs(["Análisis Pareto"])
        # --- Pareto Analysis Section ---
        st.markdown("##### CECO's que Representan el 80% del Presupuesto por área (Egresos, Sin Nómina)")
        pareto_result_df = perform_pareto_analysis(filtered_df)
        if not pareto_result_df.empty:
                pareto_result_df['Presupuesto 2025'] = pareto_result_df['Presupuesto 2025'].apply(format_currency_millions)
                styled_pareto = style_dataframe(pareto_result_df.rename(columns={'Presupuesto 2025': 'Monto (M)'}))
                st.markdown(styled_pareto.to_html(), unsafe_allow_html=True)
        else:
                st.info("No hay suficientes datos de egresos para realizar el análisis de Pareto en esta área.")

else:
    st.error("No se pudieron cargar los datos. Revisa el nombre del archivo 'presupuesto20251.csv' y su contenido.")