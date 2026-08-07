from __future__ import annotations

from pathlib import Path
from typing import Iterable

import pandas as pd
import plotly.express as px
import streamlit as st


DEFAULT_DATA_PATH = "base_semanal_unidad_2026.parquet"

INSTITUTIONAL_PALETTE = {
    "green_1": "#006657",
    "green_2": "#1E5B4F",
    "green_3": "#002F2A",
    "wine_1": "#9B2247",
    "wine_2": "#611232",
    "gold_1": "#E6D194",
    "gold_2": "#A57F2C",
    "bg": "#F2F0EC",
    "bg_2": "#E8E5DF",
    "border": "#D4CFC8",
    "ink": "#161A1D",
    "ink_2": "#3D4045",
}

GENERAL_CHART_COLORS = [
    "#006657",
    "#A57F2C",
    "#9B2247",
    "#1E5B4F",
    "#611232",
    "#7C8782",
    "#C8B37D",
    "#4C6F66",
    "#B86B84",
    "#8A8D8F",
]

STAFF_RANKED_COLORS = [
    "#EBF5F3",
    "#F3E9CA",
    "#D4EAE6",
    "#E8E5DF",
    "#C7D8D3",
    "#A57F2C",
    "#7EC8BE",
    "#006657",
    "#9B2247",
    "#611232",
]

AGE_GROUP_COLORS = {
    "Embarazadas": "#D45087",
    "Puérperas": "#F58518",
    "Niñas, niños y adolescentes": "#4C78A8",
    "NNA": "#4C78A8",
    "Adultos": "#54A24B",
    "Adultos mayores": "#B279A2",
}


st.set_page_config(
    page_title="Estrategia de Atención Proactiva, 2026",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)


CSS = """
<style>
:root {
  --ap-green: #006657;
  --ap-green-dark: #002F2A;
  --ap-green-mid: #1E5B4F;
  --ap-wine: #9B2247;
  --ap-wine-dark: #611232;
  --ap-gold: #A57F2C;
  --ap-gold-light: #E6D194;
  --ap-ink: #161A1D;
  --ap-ink-soft: #3D4045;
  --ap-muted: #72706E;
  --ap-bg: #F2F0EC;
  --ap-bg-2: #E8E5DF;
  --ap-card: #FFFFFF;
  --ap-border: #D4CFC8;
  --ap-radius: 6px;
  --ap-shadow: 0 1px 3px rgba(0,0,0,.07), 0 2px 8px rgba(0,0,0,.05);
}
.stApp { background: var(--ap-bg); color: var(--ap-ink); font-family: Arial, Helvetica, sans-serif; }
.block-container { padding-top: 1.1rem; padding-bottom: 3rem; max-width: 1540px; }
h1, h2, h3 { color: var(--ap-green-mid); letter-spacing: 0; font-family: Arial, Helvetica, sans-serif; }
h1 { font-size: 2rem; line-height: 1.1; }
h2, h3 { font-size: 1.15rem; }
.ap-title {
  background: var(--ap-green-dark);
  border-bottom: 3px solid var(--ap-gold);
  border-radius: var(--ap-radius);
  box-shadow: var(--ap-shadow);
  padding: 16px 22px;
  margin-bottom: 16px;
}
.ap-title h1 {
  color: var(--ap-gold-light);
  margin: 0;
}
[data-testid="stSidebar"] {
  background: #FFFFFF;
  border-right: 1px solid var(--ap-border);
}
[data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
  color: var(--ap-green-dark);
}
div[data-testid="stTabs"] button {
  border-radius: var(--ap-radius) var(--ap-radius) 0 0;
  color: var(--ap-muted);
  font-weight: 700;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
  color: var(--ap-green-dark);
  border-bottom-color: var(--ap-gold);
}
div[data-testid="stDataFrame"] {
  border: 1px solid var(--ap-border);
  border-radius: var(--ap-radius);
  box-shadow: var(--ap-shadow);
  overflow: hidden;
}
.stPlotlyChart {
  background: var(--ap-card);
  border: 1px solid var(--ap-border);
  border-radius: var(--ap-radius);
  box-shadow: var(--ap-shadow);
  padding: 10px 10px 4px;
}
.stMarkdown h3, .stMarkdown h2 {
  color: var(--ap-green-mid);
}
.app-footer {
  border-top: 1px solid var(--ap-border);
  color: var(--ap-muted);
  font-size: 13px;
  margin-top: 28px;
  padding-top: 12px;
  text-align: center;
}
.filter-summary {
  background: #FFFFFF;
  border: 1px solid var(--ap-border);
  border-left: 5px solid var(--ap-gold);
  border-radius: var(--ap-radius);
  box-shadow: var(--ap-shadow);
  color: var(--ap-ink-soft);
  font-size: 14px;
  margin: 0 0 14px;
  padding: 10px 13px;
}
</style>
"""


def resolve_data_path(path_text: str) -> str:
    path = Path(path_text)
    if path.exists():
        return str(path)
    if path.suffix == "":
        for suffix in (".parquet", ".csv"):
            data_path = path.with_suffix(suffix)
            if data_path.exists():
                return str(data_path)
    return path_text


def load_data(source: str) -> pd.DataFrame:
    data_path = resolve_data_path(source)
    if str(data_path).lower().endswith(".parquet"):
        df = pd.read_parquet(data_path)
    else:
        df = pd.read_csv(data_path, encoding="utf-8-sig")
    df.columns = [str(c).strip() for c in df.columns]
    for col in df.columns:
        if col not in {"Estado", "CLUES FINAL"}:
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)

    if "anio_epidemiologico" in df.columns:
        df = df[df["anio_epidemiologico"] == 2026].copy()

    return df


def existing_columns(df: pd.DataFrame, columns: Iterable[str]) -> list[str]:
    return [col for col in columns if col in df.columns]


def sum_columns(df: pd.DataFrame, columns: Iterable[str]) -> float:
    cols = existing_columns(df, columns)
    if not cols:
        return 0.0
    return float(df[cols].apply(pd.to_numeric, errors="coerce").fillna(0).to_numpy().sum())


def filter_label(value: object) -> str:
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


def checkbox_filter(label: str, options: list, key: str) -> list:
    with st.sidebar.expander(label, expanded=False):
        select_all = st.checkbox("Todas", value=True, key=f"{key}_all")
        if select_all:
            st.caption(f"{len(options):,} opciones seleccionadas")
            return options

        selected = []
        for option in options:
            if st.checkbox(filter_label(option), value=False, key=f"{key}_{filter_label(option)}"):
                selected.append(option)
        return selected


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filtros")
    filtered = df.copy()

    if "anio_epidemiologico" in filtered.columns:
        years = sorted(filtered["anio_epidemiologico"].dropna().unique())
        selected_years = checkbox_filter("Año epidemiológico", years, "anio_epidemiologico")
        filtered = filtered[filtered["anio_epidemiologico"].isin(selected_years)]

    if "Estado" in filtered.columns:
        states = sorted(filtered["Estado"].dropna().astype(str).unique())
        selected_states = checkbox_filter("Estado", states, "estado")
        filtered = filtered[filtered["Estado"].astype(str).isin(selected_states)]

    if "CLUES FINAL" in filtered.columns:
        clues = sorted(filtered["CLUES FINAL"].dropna().astype(str).unique())
        selected_clues = checkbox_filter("CLUES", clues, "clues")
        filtered = filtered[filtered["CLUES FINAL"].astype(str).isin(selected_clues)]

    return filtered


def month_column(df: pd.DataFrame) -> str | None:
    for column in ("Mes", "mes", "MES", "Month", "month", "mes_nombre", "nombre_mes"):
        if column in df.columns:
            return column
    return None


def apply_filters_with_summary(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, tuple[list, list]]]:
    st.sidebar.header("Filtros")
    filtered = df.copy()
    selections = {}

    if "anio_epidemiologico" in filtered.columns:
        years = sorted(filtered["anio_epidemiologico"].dropna().unique())
        selected_years = checkbox_filter("Año epidemiológico", years, "anio_epidemiologico")
        filtered = filtered[filtered["anio_epidemiologico"].isin(selected_years)]
        selections["Año"] = (selected_years, years)

    mes_col = month_column(filtered)
    if mes_col:
        months = sorted(filtered[mes_col].dropna().unique(), key=filter_label)
        selected_months = checkbox_filter("Mes", months, "mes")
        filtered = filtered[filtered[mes_col].isin(selected_months)]
        selections["Mes"] = (selected_months, months)

    if "Estado" in filtered.columns:
        states = sorted(filtered["Estado"].dropna().astype(str).unique())
        selected_states = checkbox_filter("Estado", states, "estado")
        filtered = filtered[filtered["Estado"].astype(str).isin(selected_states)]
        selections["Estado"] = (selected_states, states)

    if "CLUES FINAL" in filtered.columns:
        clues = sorted(filtered["CLUES FINAL"].dropna().astype(str).unique())
        selected_clues = checkbox_filter("CLUES", clues, "clues")
        filtered = filtered[filtered["CLUES FINAL"].astype(str).isin(selected_clues)]
        selections["CLUES"] = (selected_clues, clues)

    return filtered, selections


def selection_text(selected: list, options: list) -> str:
    if len(selected) == len(options):
        return "Todas"
    if not selected:
        return "Ninguna"
    labels = [filter_label(value) for value in selected]
    if len(labels) <= 5:
        return ", ".join(labels)
    return f'{", ".join(labels[:5])} y {len(labels) - 5} más'


def filter_summary_text(selections: dict[str, tuple[list, list]]) -> str:
    parts = []
    for label, (selected, options) in selections.items():
        parts.append(f"{label}: {selection_text(selected, options)}")
    return "Filtros seleccionados - " + " | ".join(parts)


def show_filter_summary(selections: dict[str, tuple[list, list]]) -> None:
    st.markdown(f'<div class="filter-summary">{filter_summary_text(selections)}</div>', unsafe_allow_html=True)


INDICATOR_DENOMINATOR_COLUMNS = [
    "Mujer__fila_399",
    "Hombre__fila_400",
    "Total embarazadas__fila_12",
    "Puerperias__fila_115",
    "Discapacidad__fila_17",
    "Discapacidad__fila_120",
    "Discapacidad__fila_223",
    "Discapacidad__fila_320",
    "Discapacidad__fila_408",
    "Ausentismo__fila_207",
    "Ausentismo__fila_308",
    "Ausentismo__fila_396",
]


def indicator_summary(df: pd.DataFrame) -> pd.DataFrame:
    base_denominator = sum_columns(df, INDICATOR_DENOMINATOR_COLUMNS)
    family_action_columns = [
        "Detección de adicciones",
        "Cuestionario factores de riesgo",
        "Cuestionario de cáncer de próstata",
        "Detecciones de salud mental",
        "Detección a cáncer de menores de 18 años",
        "Test sobre la carga de la persona cuidadora (Zarit y Zarit)",
        "PFAM Orientación en salud bucal, visual y auditiva",
        "PFAM Salud mental y adicciones",
        "PFAM Salud sexual y reproductiva",
        "PFAM Prevención de enfermedades",
        "PFAM Nutrición y actividad física",
        "PFAM Saneamiento básico",
        "PFAM Prevención de la violencia",
        "PFAM Autoexploración para prevención del cáncer de mama",
        "PFAM Entrega de ácido fólico y vitaminas",
        "PFAM Entrega de vida suero oral",
        "PFAM Entrega de material",
    ]
    zarit_positive_columns = [
        "Positivo Test sobre la carga del cuidador (Zarit y Zarit)__fila_73",
        "Positivo Test sobre la carga del cuidador (Zarit y Zarit)__fila_173",
        "Positivo Test sobre la carga del cuidador (Zarit y Zarit)__fila_274",
        "Positivo Test sobre la carga del cuidador (Zarit y Zarit)__fila_362",
        "Positivo Test sobre la carga del cuidador (Zarit y Zarit)__fila_466",
    ]
    zarit_detection_columns = [
        "Detección Test sobre la carga del cuidador (Zarit y Zarit)__fila_72",
        "Detección Test sobre la carga del cuidador (Zarit y Zarit)__fila_172",
        "Detección Test sobre la carga del cuidador (Zarit y Zarit)__fila_273",
        "Detección Test sobre la carga del cuidador (Zarit y Zarit)__fila_361",
        "Detección Test sobre la carga del cuidador (Zarit y Zarit)__fila_465",
    ]

    rows = [
        {
            "Indicador": "USPN que implementan la Estrategia de AP",
            "Tipo": "Porcentaje",
            "Numerador": df["CLUES FINAL"].nunique() if "CLUES FINAL" in df.columns else 0,
            "Denominador": 8273,
        },
        {
            "Indicador": "Atenciones a personas mayores otorgadas mediante AP",
            "Tipo": "Porcentaje",
            "Numerador": sum_columns(df, ["Mujer__fila_399", "Hombre__fila_400"]),
            "Denominador": base_denominator,
        },
        {
            "Indicador": "Atenciones a personas con discapacidad física o psicosocial mediante AP",
            "Tipo": "Porcentaje",
            "Numerador": sum_columns(
                df,
                [
                    "Discapacidad__fila_17",
                    "Discapacidad__fila_120",
                    "Discapacidad__fila_223",
                    "Discapacidad__fila_320",
                    "Discapacidad__fila_408",
                ],
            ),
            "Denominador": base_denominator,
        },
        {
            "Indicador": "Atenciones a personas embarazadas o en puerperio mediante AP",
            "Tipo": "Porcentaje",
            "Numerador": sum_columns(df, ["Total embarazadas__fila_12", "Puerperias__fila_115"]),
            "Denominador": base_denominator,
        },
        {
            "Indicador": "Razón de acciones de promoción y prevención a familiares por personas que reciben AP",
            "Tipo": "Razón",
            "Numerador": sum_columns(df, family_action_columns),
            "Denominador": base_denominator,
        },
        {
            "Indicador": "Positividad del test Zarit-Zarit a cuidadores de quienes reciben AP",
            "Tipo": "Porcentaje",
            "Numerador": sum_columns(df, zarit_positive_columns),
            "Denominador": sum_columns(df, zarit_detection_columns),
        },
        {
            "Indicador": "Atenciones otorgadas a población migrante mediante AP",
            "Tipo": "Porcentaje",
            "Numerador": sum_columns(
                df,
                [
                    "Migrante__fila_8",
                    "Migrante__fila_111",
                    "Migrante__fila_217",
                    "Migrante__fila_314",
                    "Migrante__fila_402",
                ],
            ),
            "Denominador": 783403,
        },
        {
            "Indicador": "Cédulas de Microdiagnóstico Familiar aplicadas en viviendas con intervenciones de AP",
            "Tipo": "Porcentaje",
            "Numerador": sum_columns(df, ["Se aplicó cédula microdx SI"]),
            "Denominador": sum_columns(df, ["Intervenciones en la vivienda SI", "Intervenciones en la vivienda NO"]),
        },
    ]

    indicators = pd.DataFrame(rows)
    indicators["Meta"] = [0.33, 0.366, 0.102, 0.025, 4.0, 0.123, 0.01, 0.35]
    indicators["Meta texto"] = ["33.0%", "36.6%", "10.2%", "2.5%", "4:1", "12.3%", "1.0%", "35.0%"]
    indicators["Valor"] = indicators.apply(
        lambda row: row["Numerador"] / row["Denominador"] if row["Denominador"] else 0,
        axis=1,
    )
    indicators["Restante"] = indicators.apply(
        lambda row: max(0, 1 - row["Valor"]) if row["Tipo"] == "Porcentaje" else max(0, 1 - min(row["Valor"], 1)),
        axis=1,
    )
    indicators["Resultado"] = indicators.apply(
        lambda row: f'{row["Valor"]:.2f}:1' if row["Tipo"] == "Razón" else f'{row["Valor"]:.1%}',
        axis=1,
    )
    indicators["Numerador"] = indicators["Numerador"].round(0).astype(int)
    indicators["Denominador"] = indicators["Denominador"].round(0).astype(int)
    return indicators


def people_by_age_group(df: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("Embarazadas", ("Total embarazadas__fila_12",)),
        ("Puérperas", ("Puerperias__fila_115",)),
        ("Niñas, niños y adolescentes", ("Mujer__fila_210", "Hombre__fila_211")),
        ("Adultos", ("Mujer__fila_311", "Hombre__fila_312")),
        ("Adultos mayores", ("Mujer__fila_399", "Hombre__fila_400")),
    ]
    return pd.DataFrame(
        [{"Grupo de edad": label, "Total": sum_columns(df, columns)} for label, columns in rows]
    )


def people_by_sex(df: pd.DataFrame) -> pd.DataFrame:
    rows = [
        (
            "Mujeres",
            (
                "Total embarazadas__fila_12",
                "Puerperias__fila_115",
                "Mujer__fila_210",
                "Mujer__fila_311",
                "Mujer__fila_399",
            ),
        ),
        (
            "Hombres",
            (
                "Hombre__fila_211",
                "Hombre__fila_312",
                "Hombre__fila_321",
                "Hombre__fila_400",
            ),
        ),
    ]
    return pd.DataFrame([{"Sexo": label, "Total": sum_columns(df, columns)} for label, columns in rows])


def pregnancy_puerperium(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "Concepto": "Total",
                "Embarazadas": sum_columns(df, ["Total embarazadas__fila_12"]),
                "Puérperas": sum_columns(df, ["Puerperias__fila_115"]),
            },
            {
                "Concepto": "Adolescentes",
                "Embarazadas": sum_columns(df, ["Edad 10-19__fila_10"]),
                "Puérperas": sum_columns(df, ["Edad 10-19__fila_113"]),
            },
            {
                "Concepto": "Alto riesgo",
                "Embarazadas": sum_columns(df, ["Embarazo de alto riesgo__fila_28"]),
                "Puérperas": "N/A",
            },
        ]
    )


def disability_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("NNA", "Tipo discapacidad__fila_224", "Tipo discapacidad__fila_225"),
        ("Adultos", "Tipo discapacidad__fila_321", "Tipo discapacidad__fila_322"),
        ("Adultos mayores", "Tipo discapacidad__fila_409", "Tipo discapacidad__fila_410"),
        ("Embarazadas", "Tipo discapacidad__fila_18", "Tipo discapacidad__fila_19"),
        ("Puérperas", "Tipo discapacidad__fila_121", "Tipo discapacidad__fila_122"),
    ]
    return pd.DataFrame(
        [
            {
                "Grupo de edad": label,
                "Discapacidad temporal": sum_columns(df, [temporary]),
                "Discapacidad permanente": sum_columns(df, [permanent]),
            }
            for label, temporary, permanent in rows
        ]
    )


def absenteeism_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("NNA", "Ausentismo__fila_207"),
        ("Adultos", "Ausentismo__fila_308"),
        ("Adultos mayores", "Ausentismo__fila_396"),
        ("Embarazadas", "Ausentismo__fila_4"),
        ("Puérperas", "Ausentismo__fila_107"),
    ]
    return pd.DataFrame(
        [{"Grupo de edad": label, "Ausentismo": sum_columns(df, [column])} for label, column in rows]
    )


def detections_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = [
        {
            "Detección": "Ansiedad y Depresión",
            "NNA": sum_columns(df, ["Positivo Depresión__fila_241", "Positivo Ansiedad__fila_251"]),
            "Adultos": sum_columns(df, ["Positivo Depresión__fila_329", "Positivo Ansiedad__fila_339"]),
            "Adultos mayores": sum_columns(df, ["Positivo Depresión__fila_437", "Positivo Ansiedad__fila_447"]),
            "Embarazadas": sum_columns(df, ["Positivo Depresión__fila_40", "Positivo Ansiedad__fila_50"]),
            "Puérperas": sum_columns(df, ["Positivo Depresión__fila_140", "Positivo Ansiedad__fila_150"]),
        },
        {
            "Detección": "Riesgo de suicidio",
            "NNA": sum_columns(df, ["Positivo Riesgo de suicidio__fila_243"]),
            "Adultos": sum_columns(df, ["Positivo Riesgo de suicidio__fila_331"]),
            "Adultos mayores": sum_columns(df, ["Positivo Riesgo de suicidio__fila_439"]),
            "Embarazadas": sum_columns(df, ["Positivo Riesgo de suicidio__fila_42"]),
            "Puérperas": sum_columns(df, ["Positivo Riesgo de suicidio__fila_142"]),
        },
        {
            "Detección": "Obesidad",
            "NNA": sum_columns(df, ["Positivo Detección de riesgo de obesidad__fila_262"]),
            "Adultos": sum_columns(df, ["Positivo Detección de riesgo de obesidad__fila_350"]),
            "Adultos mayores": sum_columns(df, ["Positivo Detección de riesgo de obesidad__fila_458"]),
            "Embarazadas": sum_columns(df, ["Positivo Detección de riesgo de obesidad__fila_61"]),
            "Puérperas": sum_columns(df, ["Positivo Detección de riesgo de obesidad__fila_161"]),
        },
        {
            "Detección": "DM",
            "NNA": sum_columns(df, ["Positivo Detección riesgo de Diabetes Mellitus__fila_266"]),
            "Adultos": sum_columns(df, ["Positivo Detección riesgo de Diabetes Mellitus__fila_354"]),
            "Adultos mayores": sum_columns(df, ["Positivo Detección riesgo de Diabetes Mellitus__fila_461"]),
            "Embarazadas": sum_columns(df, ["Positivo Detección riesgo de Diabetes Mellitus__fila_65"]),
            "Puérperas": sum_columns(df, ["Positivo Detección riesgo de Diabetes Mellitus__fila_165"]),
        },
        {
            "Detección": "HAS",
            "NNA": sum_columns(df, ["Positivo Detección de riesgo de hipertensión arterial sistémica__fila_264"]),
            "Adultos": sum_columns(df, ["Positivo Detección de riesgo de hipertensión arterial sistémica__fila_352"]),
            "Adultos mayores": sum_columns(df, ["Positivo Detección de riesgo de hipertensión arterial sistémica__fila_460"]),
            "Embarazadas": sum_columns(df, ["Positivo Detección de riesgo de hipertensión arterial sistémica__fila_63"]),
            "Puérperas": sum_columns(df, ["Positivo Detección de riesgo de hipertensión arterial sistémica__fila_163"]),
        },
        {
            "Detección": "Dislipidemias",
            "NNA": sum_columns(df, ["Positivo Detección de riesgo de dislipidemias__fila_268"]),
            "Adultos": sum_columns(df, ["Positivo Detección de riesgo de dislipidemias__fila_356"]),
            "Adultos mayores": sum_columns(df, ["Positivo Detección de riesgo de dislipidemias__fila_464"]),
            "Embarazadas": sum_columns(df, ["Positivo Detección de riesgo de dislipidemias__fila_67"]),
            "Puérperas": sum_columns(df, ["Positivo Detección de riesgo de dislipidemias__fila_167"]),
        },
        {
            "Detección": "Alcohol, Tabaco y Otras sustancias",
            "NNA": sum_columns(df, ["Positivo Consumo de alcohol__fila_245", "Positivo Consumo de tabaco__fila_247", "Positivo Consumo de otras sustancias__fila_249"]),
            "Adultos": sum_columns(df, ["Positivo Consumo de alcohol__fila_333", "Positivo Consumo de tabaco__fila_335", "Positivo Consumo de otras sustancias__fila_337"]),
            "Adultos mayores": sum_columns(df, ["Positivo Consumo de alcohol__fila_441", "Positivo Consumo de tabaco__fila_443", "Positivo Consumo de otras sustancias__fila_445"]),
            "Embarazadas": sum_columns(df, ["Positivo Consumo de alcohol__fila_44", "Positivo Consumo de tabaco__fila_46", "Positivo Consumo de otras sustancias__fila_48"]),
            "Puérperas": sum_columns(df, ["Positivo Consumo de alcohol__fila_144", "Positivo Consumo de tabaco__fila_146", "Positivo Consumo de otras sustancias__fila_148"]),
        },
        {
            "Detección": "Violencia Psicológica",
            "NNA": sum_columns(df, ["Psicológica__fila_255"]),
            "Adultos": sum_columns(df, ["Psicológica__fila_342"]),
            "Adultos mayores": sum_columns(df, ["Psicológica__fila_450"]),
            "Embarazadas": sum_columns(df, ["Psicológica__fila_54"]),
            "Puérperas": sum_columns(df, ["Psicológica__fila_154"]),
        },
        {
            "Detección": "Violencia Física",
            "NNA": sum_columns(df, ["Física__fila_254"]),
            "Adultos": sum_columns(df, ["Física__fila_342"]),
            "Adultos mayores": sum_columns(df, ["Física__fila_450"]),
            "Embarazadas": sum_columns(df, ["Física__fila_53"]),
            "Puérperas": sum_columns(df, ["Física__fila_153"]),
        },
        {
            "Detección": "Bullying",
            "NNA": sum_columns(df, ["Bullying__fila_259"]),
            "Adultos": sum_columns(df, ["Bullying__fila_347"]),
            "Adultos mayores": sum_columns(df, ["Bullying__fila_455"]),
            "Embarazadas": sum_columns(df, ["Bullying__fila_58"]),
            "Puérperas": sum_columns(df, ["Bullying__fila_158"]),
        },
        {
            "Detección": "Violencia Sexual",
            "NNA": sum_columns(df, ["Sexual__fila_256"]),
            "Adultos": sum_columns(df, ["Sexual__fila_344"]),
            "Adultos mayores": sum_columns(df, ["Sexual__fila_452"]),
            "Embarazadas": sum_columns(df, ["Sexual__fila_55"]),
            "Puérperas": sum_columns(df, ["Sexual__fila_155"]),
        },
        {
            "Detección": "Violencia Económica",
            "NNA": sum_columns(df, ["Económica__fila_258"]),
            "Adultos": sum_columns(df, ["Económica__fila_346"]),
            "Adultos mayores": sum_columns(df, ["Económica__fila_454"]),
            "Embarazadas": sum_columns(df, ["Económica__fila_57"]),
            "Puérperas": sum_columns(df, ["Económica__fila_157"]),
        },
        {
            "Detección": "Abandono",
            "NNA": sum_columns(df, ["Abandono__fila_257"]),
            "Adultos": sum_columns(df, ["Abandono__fila_345"]),
            "Adultos mayores": sum_columns(df, ["Abandono__fila_453"]),
            "Embarazadas": sum_columns(df, ["Abandono__fila_56"]),
            "Puérperas": sum_columns(df, ["Abandono__fila_156"]),
        },
        {
            "Detección": "Referencias",
            "NNA": sum_columns(df, ["Referidos a 1er nivel por violencia__fila_260"]),
            "Adultos": sum_columns(df, ["Referidos a 1er nivel por violencia__fila_348"]),
            "Adultos mayores": sum_columns(df, ["Referidos a 1er nivel por violencia__fila_456"]),
            "Embarazadas": sum_columns(df, ["Referidos a 1er nivel por violencia__fila_59"]),
            "Puérperas": sum_columns(df, ["Referidos a 1er nivel por violencia__fila_159"]),
        },
    ]
    return pd.DataFrame(rows)


def visit_conclusion_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = [
        (
            "Cita en USPN",
            (
                "Desenlace se asignó fecha proxima visita uspn__fila_92",
                "Desenlace se asignó fecha proxima visita uspn__fila_192",
                "Desenlace se asignó fecha proxima visita uspn__fila_293",
                "Desenlace se asignó fecha proxima visita uspn__fila_381",
                "Desenlace se asignó fecha proxima visita uspn__fila_485",
            ),
        ),
        (
            "Referencia a 2ndo nivel",
            (
                "Referencia 2ndo nivel__fila_91",
                "Referencia 2ndo nivel__fila_191",
                "Referencia 2ndo nivel__fila_292",
                "Referencia 2ndo nivel__fila_380",
                "Referencia 2ndo nivel__fila_484",
            ),
        ),
        (
            "Referencia a USPN",
            (
                "Referencia 1er nivel__fila_90",
                "Referencia 1er nivel__fila_190",
                "Referencia 1er nivel__fila_291",
                "Referencia 1er nivel__fila_379",
                "Referencia 1er nivel__fila_483",
            ),
        ),
        (
            "Próxima visita en domicilio",
            (
                "Desenlace se asignó fecha proxima visita domicilio__fila_93",
                "Desenlace se asignó fecha proxima visita domicilio__fila_193",
                "Desenlace se asignó fecha proxima visita domicilio__fila_294",
                "Desenlace se asignó fecha proxima visita domicilio__fila_382",
                "Desenlace se asignó fecha proxima visita domicilio__fila_486",
            ),
        ),
        (
            "Expidió nueva receta",
            (
                "Desenlace Expidió nueva receta__fila_94",
                "Desenlace Expidió nueva receta__fila_194",
                "Desenlace Expidió nueva receta__fila_295",
                "Desenlace Expidió nueva receta__fila_383",
                "Desenlace Expidió nueva receta__fila_487",
            ),
        ),
        (
            "Surtió nueva receta",
            (
                "Desenlace surtió nueva receta__fila_95",
                "Desenlace surtió nueva receta__fila_195",
                "Desenlace surtió nueva receta__fila_296",
                "Desenlace surtió nueva receta__fila_384",
                "Desenlace surtió nueva receta__fila_488",
            ),
        ),
    ]
    return pd.DataFrame(
        [{"Conclusión de la visita": label, "Total": sum_columns(df, columns)} for label, columns in rows]
    )


def proactive_staff_summary(df: pd.DataFrame) -> pd.DataFrame:
    columns = [
        "Médica(o) general",
        "Enfermera(o)",
        "Promotor(a) de salud",
        "Nutriólogo(a)",
        "Psicólogo(a)",
        "Fisioterapeuta",
        "Odontólogo(a)",
        "Trabajador(a) social",
        "Administrativo(a)",
        "Otro personal",
    ]
    return pd.DataFrame([{"Perfil": column, "Total": sum_columns(df, [column])} for column in columns])


def patient_interventions_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("Cambio de sonda", ("Cambio de sonda__fila_76", "Cambio de sonda__fila_176", "Cambio de sonda__fila_277", "Cambio de sonda__fila_365", "Cambio de sonda__fila_469")),
        ("Curaciones", ("Curaciones__fila_77", "Curaciones__fila_177", "Curaciones__fila_278", "Curaciones__fila_366", "Curaciones__fila_470")),
        ("Aplicación de vendajes", ("Aplicación de vendajes__fila_78", "Aplicación de vendajes__fila_178", "Aplicación de vendajes__fila_279", "Aplicación de vendajes__fila_367", "Aplicación de vendajes__fila_471")),
        ("Valoración por úlceras por presión", ("Valoración por úlceras por presión__fila_79", "Valoración por úlceras por presión__fila_179", "Valoración por úlceras por presión__fila_280", "Valoración por úlceras por presión__fila_368", "Valoración por úlceras por presión__fila_472")),
        ("Colocación de venoclisis", ("Colocación de venoclisis__fila_80", "Colocación de venoclisis__fila_180", "Colocación de venoclisis__fila_281", "Colocación de venoclisis__fila_369", "Colocación de venoclisis__fila_473")),
        ("Entrega de métodos anticonceptivos", ("Entrega de métodos anticonceptivos__fila_81", "Entrega de métodos anticonceptivos__fila_181", "Entrega de métodos anticonceptivos__fila_282", "Entrega de métodos anticonceptivos__fila_370", "Entrega de métodos anticonceptivos__fila_474")),
        ("Expedición de certificado de discapacidad", ("Expedición de certificado de discapacidad__fila_82", "Expedición de certificado de discapacidad__fila_182", "Expedición de certificado de discapacidad__fila_283", "Expedición de certificado de discapacidad__fila_371", "Expedición de certificado de discapacidad__fila_475")),
        ("Certificado de defunción", ("Certificado de defunción__fila_83", "Certificado de defunción__fila_183", "Certificado de defunción__fila_284", "Certificado de defunción__fila_372", "Certificado de defunción__fila_476")),
        ("Formato de voluntad anticipada paciente adulto", ("Formato de voluntad anticipada paciente adulto__fila_84", "Formato de voluntad anticipada paciente adulto__fila_184", "Formato de voluntad anticipada paciente adulto__fila_285", "Formato de voluntad anticipada paciente adulto__fila_373", "Formato de voluntad anticipada paciente adulto__fila_477")),
        ("Otras intervenciones", ("Otras intervenciones__fila_85", "Otras intervenciones__fila_185", "Otras intervenciones__fila_286", "Otras intervenciones__fila_374", "Otras intervenciones__fila_478")),
    ]
    return pd.DataFrame([{"Intervención": label, "Total": sum_columns(df, columns)} for label, columns in rows])


def ethnicity_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("Embarazadas", ("Etnicidad__fila_7",)),
        ("Puérperas", ("Etnicidad__fila_110",)),
        ("Niñas, niños y adolescentes", ("Etnicidad__fila_216",)),
        ("Adultos", ("Etnicidad__fila_313",)),
        ("Adultos mayores", ("Etnicidad__fila_401",)),
    ]
    return pd.DataFrame([{"Grupo": label, "Total": sum_columns(df, columns)} for label, columns in rows])


def migrant_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("Embarazadas", ("Migrante__fila_8",)),
        ("Puérperas", ("Migrante__fila_111",)),
        ("Niñas, niños y adolescentes", ("Migrante__fila_217",)),
        ("Adultos", ("Migrante__fila_314",)),
        ("Adultos mayores", ("Migrante__fila_402",)),
    ]
    return pd.DataFrame([{"Grupo": label, "Total": sum_columns(df, columns)} for label, columns in rows])


def format_integer(value: float) -> str:
    return f"{value:,.0f}"


def format_percent(value: float) -> str:
    return f"{value:.0%}"


def prevention_promotion_summary(df: pd.DataFrame) -> dict:
    detection_columns = [
        "Detección de adicciones",
        "Cuestionario factores de riesgo",
        "Cuestionario de cáncer de próstata",
        "Detecciones de salud mental",
        "Detección a cáncer de menores de 18 años",
        "Test sobre la carga de la persona cuidadora (Zarit y Zarit)",
    ]
    positive_columns = [
        "Detección de adicciones positivas",
        "Cuestionario factores de riesgo positivos",
        "Cuestionario de cáncer de próstata positivos",
        "Detecciones de salud mental positivos",
        "Detección a cáncer de menores de 18 años positivas",
        "Test sobre la carga de la persona cuidadora (Zarit y Zarit) positivos",
    ]
    caregiver_columns = [
        "Persona Cuidadora__fila_9",
        "Persona Cuidadora__fila_112",
        "Persona Cuidadora__fila_218",
        "Persona Cuidadora__fila_315",
        "Persona Cuidadora__fila_403",
    ]
    family_delivery_columns = [
        "PFAM Entrega de ácido fólico y vitaminas",
        "PFAM Entrega de vida suero oral",
        "PFAM Entrega de material",
    ]

    detections = sum_columns(df, detection_columns)
    positives = sum_columns(df, positive_columns)
    zarit = sum_columns(df, ["Test sobre la carga de la persona cuidadora (Zarit y Zarit)"])
    zarit_positive = sum_columns(df, ["Test sobre la carga de la persona cuidadora (Zarit y Zarit) positivos"])

    return {
        "houses": sum_columns(df, ["Intervenciones en la vivienda SI", "Intervenciones en la vivienda NO"]),
        "family_members": sum_columns(df, ["Núm. integrantes que recibieron acciones preventivas"]),
        "detections": detections,
        "detection_positivity": positives / detections if detections else 0,
        "caregivers": sum_columns(df, caregiver_columns),
        "zarit": zarit,
        "zarit_positivity": zarit_positive / zarit if zarit else 0,
        "family_deliveries": sum_columns(df, family_delivery_columns),
    }


def health_talks_summary(df: pd.DataFrame) -> pd.DataFrame:
    rows = [
        ("Nutrición y actividad física", ("PFAM Nutrición y actividad física",)),
        ("Prevención de enfermedades", ("PFAM Prevención de enfermedades",)),
        ("Saneamiento básico", ("PFAM Saneamiento básico",)),
        ("Orientación salud bucal, visual y auditiva", ("PFAM Orientación en salud bucal, visual y auditiva",)),
        ("Salud mental y adicciones", ("PFAM Salud mental y adicciones",)),
        ("Salud sexual y reproductiva", ("PFAM Salud sexual y reproductiva",)),
        ("Prevención de la violencia", ("PFAM Prevención de la violencia",)),
        ("Prevención de cáncer de mama", ("PFAM Autoexploración para prevención del cáncer de mama",)),
    ]
    df_talks = pd.DataFrame([{"Plática": label, "Total": sum_columns(df, columns)} for label, columns in rows])
    total = df_talks["Total"].sum()
    df_talks["Porcentaje"] = df_talks["Total"] / total if total else 0
    return df_talks


def _legacy_render_prevention_promotion(summary: dict, talks: pd.DataFrame) -> None:
    talks_total = float(talks["Total"].sum())
    environment_actions = talks_total + summary["detections"]

    st.markdown('<div class="prevention-wrap">', unsafe_allow_html=True)
    st.markdown(
        '<div class="prevention-title">ACCIONES DE PREVENCIÓN Y PROMOCIÓN DE LA SALUD</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([1, 1.18])
    with left:
        st.markdown(
            f'<div class="metric-card">{format_integer(summary["houses"])} viviendas con<br>intervenciones</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="metric-card">{format_integer(summary["family_members"])} familiares que<br>'
            "recibieron acciones de<br>prevención y promoción de<br>la salud</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="metric-card">{format_integer(summary["detections"])} detecciones a<br>familiares</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="metric-card small">{format_percent(summary["detection_positivity"])} positividad</div>',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f'<div class="metric-card small">{format_integer(summary["caregivers"])} Cuidadores</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="metric-card small">{format_integer(summary["zarit"])} con Zarit y Zarit</div>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="metric-card small">{format_percent(summary["zarit_positivity"])} positividad</div>',
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            f'<div class="metric-card">{format_integer(talks_total)} pláticas de promoción a<br>'
            "la salud impartidas a familiares</div>",
            unsafe_allow_html=True,
        )
        st.markdown('<div class="talk-panel">', unsafe_allow_html=True)
        for _, row in talks.iterrows():
            st.markdown(
                f'<div class="talk-row"><div class="talk-label">{row["Plática"]}</div>'
                f'<div class="talk-pct">{format_percent(row["Porcentaje"])}</div></div>',
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)
        st.markdown(
            f'<div class="bottom-total">{format_integer(environment_actions)} acciones realizadas<br>'
            "en el entorno familiar</div>",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)


def show_table(title: str, df: pd.DataFrame) -> None:
    st.subheader(title)
    st.dataframe(df, hide_index=True, use_container_width=True)


def value_color_map(df: pd.DataFrame, names: str, values: str, colors: list[str]) -> dict[str, str]:
    ranked = df.sort_values(values, ascending=False)[names].tolist()
    return {name: colors[index % len(colors)] for index, name in enumerate(ranked)}


def show_pie_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    title: str,
    color_map: dict[str, str] | None = None,
    color_sequence: list[str] | None = None,
    hover_percent_only: bool = False,
) -> None:
    color_arg = names if color_map else None
    fig = px.pie(
        df,
        names=names,
        values=values,
        title=title,
        hole=0.35,
        color=color_arg,
        color_discrete_map=color_map,
        color_discrete_sequence=color_sequence or GENERAL_CHART_COLORS,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    if hover_percent_only:
        fig.update_traces(hovertemplate="%{percent:.1%}<extra></extra>")
    fig.update_layout(
        title_font_color=INSTITUTIONAL_PALETTE["green_2"],
        title_font_size=18,
        margin=dict(t=50, b=20, l=20, r=20),
        legend_title_text="",
        font=dict(family="Arial, sans-serif", size=14, color=INSTITUTIONAL_PALETTE["ink"]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)


def show_bar_chart(df: pd.DataFrame, x: str, y: str, title: str, horizontal: bool = False) -> None:
    chart_df = df.sort_values(y, ascending=True if horizontal else False)
    fig = px.bar(
        chart_df,
        x=y if horizontal else x,
        y=x if horizontal else y,
        title=title,
        text=y,
        color=x if not horizontal else None,
        orientation="h" if horizontal else "v",
        color_discrete_sequence=GENERAL_CHART_COLORS,
    )
    if horizontal:
        marker_color = [
            AGE_GROUP_COLORS.get(label, INSTITUTIONAL_PALETTE["green_1"])
            for label in chart_df[x].tolist()
        ]
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside", marker_color=marker_color)
    else:
        fig.update_traces(texttemplate="%{text:,.0f}", textposition="outside")
    fig.update_layout(
        title_font_color=INSTITUTIONAL_PALETTE["green_2"],
        title_font_size=18,
        xaxis_title="Total" if horizontal else "",
        yaxis_title="" if horizontal else "Total",
        showlegend=False,
        margin=dict(t=60, b=90 if not horizontal else 20, l=40 if not horizontal else 190, r=50),
        font=dict(family="Arial, sans-serif", size=14, color=INSTITUTIONAL_PALETTE["ink"]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)


def show_stacked_indicator_chart(indicators: pd.DataFrame) -> None:
    chart_df = indicators.copy()
    chart_df["Avance"] = chart_df.apply(
        lambda row: min(row["Valor"] / row["Meta"], 1) if row["Tipo"].startswith("Raz") and row["Meta"] else min(row["Valor"], 1),
        axis=1,
    )
    chart_df["Meta grafica"] = chart_df.apply(
        lambda row: 1 if row["Tipo"].startswith("Raz") else row["Meta"],
        axis=1,
    )
    chart_df["Restante"] = (1 - chart_df["Avance"]).clip(lower=0)
    chart_df["Comparacion"] = chart_df.apply(
        lambda row: "Supera o cumple meta" if row["Valor"] >= row["Meta"] else "Por debajo de meta",
        axis=1,
    )
    long_df = chart_df.melt(
        id_vars=["Indicador", "Resultado", "Meta texto", "Comparacion"],
        value_vars=["Avance", "Restante"],
        var_name="Componente",
        value_name="Proporción",
    )

    fig = px.bar(
        long_df,
        x="Proporción",
        y="Indicador",
        color="Componente",
        orientation="h",
        title="Indicadores de avance, a nivel nacional",
        category_orders={"Indicador": chart_df["Indicador"].tolist()[::-1]},
        color_discrete_map={"Avance": INSTITUTIONAL_PALETTE["green_1"], "Restante": INSTITUTIONAL_PALETTE["border"]},
        custom_data=["Resultado", "Meta texto", "Comparacion"],
    )
    fig.update_traces(
        hovertemplate="<b>%{y}</b><br>Resultado: %{customdata[0]}<br>Meta: %{customdata[1]}<br>%{customdata[2]}<extra></extra>",
    )
    fig.add_scatter(
        x=chart_df["Meta grafica"],
        y=chart_df["Indicador"],
        mode="markers+text",
        marker=dict(symbol="line-ns-open", size=18, color=INSTITUTIONAL_PALETTE["wine_1"], line=dict(width=3)),
        text=chart_df["Meta texto"],
        textposition="middle right",
        name="Meta",
        hovertemplate="<b>%{y}</b><br>Meta: %{text}<extra></extra>",
    )
    fig.update_layout(
        barmode="stack",
        title_font_color=INSTITUTIONAL_PALETTE["green_2"],
        title_font_size=18,
        xaxis_title="Avance",
        yaxis_title="",
        xaxis=dict(tickformat=".0%", range=[0, 1]),
        legend_title_text="",
        margin=dict(t=60, b=40, l=260, r=40),
        font=dict(family="Arial, sans-serif", size=14, color=INSTITUTIONAL_PALETTE["ink"]),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
    )
    st.plotly_chart(fig, use_container_width=True)


def prevention_summary_table(summary: dict, talks: pd.DataFrame) -> pd.DataFrame:
    talks_total = float(talks["Total"].sum())
    environment_actions = talks_total + summary["detections"] + summary["family_deliveries"]
    rows = [
        ("Viviendas con intervenciones", format_integer(summary["houses"])),
        ("Familiares que recibieron acciones de prevención y promoción de la salud", format_integer(summary["family_members"])),
        ("Detecciones a familiares", format_integer(summary["detections"])),
        ("Positividad en detecciones a familiares", format_percent(summary["detection_positivity"])),
        ("Cuidadores", format_integer(summary["caregivers"])),
        ("Con Zarit y Zarit", format_integer(summary["zarit"])),
        ("Positividad Zarit y Zarit", format_percent(summary["zarit_positivity"])),
        ("Pláticas de promoción a la salud impartidas a familiares", format_integer(talks_total)),
        ("Acciones realizadas en el entorno familiar", format_integer(environment_actions)),
    ]
    return pd.DataFrame(rows, columns=["Indicador", "Valor"])


def health_talks_display_table(talks: pd.DataFrame) -> pd.DataFrame:
    table = talks.copy()
    table["Porcentaje"] = table["Porcentaje"].map(format_percent)
    table["Total"] = table["Total"].map(format_integer)
    return table


def render_prevention_promotion(summary: dict, talks: pd.DataFrame) -> None:
    st.subheader("Acciones de prevención y promoción de la salud")
    talk_label_column = talks.columns[0]
    left, right = st.columns([1, 1])
    with left:
        show_table("Resumen de acciones en el entorno familiar", prevention_summary_table(summary, talks))
    with right:
        show_bar_chart(
            talks,
            talk_label_column,
            "Total",
            "Pláticas de promoción a la salud impartidas a familiares",
        )
    show_table("Distribución de pláticas de promoción a la salud", health_talks_display_table(talks))


def main() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown(
        '<div class="ap-title"><h1>Estrategia de Atención Proactiva, 2026</h1></div>',
        unsafe_allow_html=True,
    )

    try:
        df = load_data(DEFAULT_DATA_PATH)
    except Exception as exc:
        st.error(f"No pude leer el archivo institucional: {exc}")
        st.stop()

    filtered, filter_selections = apply_filters_with_summary(df)

    tab1, tab2, tab3, tab4 = st.tabs(
        [
            "Indicadores de avance",
            "Datos relevantes",
            "Intervenciones a los pacientes",
            "Acciones de prevención y promoción a la salud",
        ]
    )

    with tab1:
        indicators = indicator_summary(df)
        show_stacked_indicator_chart(indicators)
        indicator_table = indicators[["Indicador", "Tipo", "Numerador", "Denominador", "Meta texto", "Resultado"]]
        st.subheader("Indicadores de avance, a nivel nacional")
        st.dataframe(indicator_table, hide_index=True, use_container_width=True)

    with tab2:
        show_filter_summary(filter_selections)
        if filtered.empty:
            st.warning("No hay registros con los filtros seleccionados.")
        people = people_by_age_group(filtered)
        sex = people_by_sex(filtered)
        pregnancy = pregnancy_puerperium(filtered)
        disability = disability_summary(filtered)
        absenteeism = absenteeism_summary(filtered)
        detections = detections_summary(filtered)

        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            show_pie_chart(
                people,
                "Grupo de edad",
                "Total",
                "Personas atendidas por grupo de edad",
                color_map=AGE_GROUP_COLORS,
            )
            st.dataframe(people, hide_index=True, use_container_width=True)
        with chart_col2:
            show_pie_chart(sex, "Sexo", "Total", "Personas atendidas por sexo")
            st.dataframe(sex, hide_index=True, use_container_width=True)

        col1, col2 = st.columns(2)
        with col1:
            pregnancy_total = pregnancy[pregnancy["Concepto"] == "Total"].melt(
                id_vars="Concepto",
                var_name="Grupo de edad",
                value_name="Total",
            )
            show_pie_chart(
                pregnancy_total,
                "Grupo de edad",
                "Total",
                "Embarazadas y puerperio",
                color_map=AGE_GROUP_COLORS,
            )
        with col2:
            show_pie_chart(
                absenteeism,
                "Grupo de edad",
                "Ausentismo",
                "Ausentismo",
                color_map=AGE_GROUP_COLORS,
            )

        dis_col1, dis_col2 = st.columns(2)
        with dis_col1:
            show_pie_chart(
                disability,
                "Grupo de edad",
                "Discapacidad temporal",
                "Personas con discapacidad temporal",
                color_map=AGE_GROUP_COLORS,
            )
        with dis_col2:
            show_pie_chart(
                disability,
                "Grupo de edad",
                "Discapacidad permanente",
                "Personas con discapacidad permanente",
                color_map=AGE_GROUP_COLORS,
            )
        show_table("Detecciones", detections)

    with tab3:
        show_filter_summary(filter_selections)
        if filtered.empty:
            st.warning("No hay registros con los filtros seleccionados.")
        proactive_staff = proactive_staff_summary(filtered)
        patient_interventions = patient_interventions_summary(filtered)
        ethnicity = ethnicity_summary(filtered)
        migrant = migrant_summary(filtered)

        show_pie_chart(
            proactive_staff,
            "Perfil",
            "Total",
            "Perfiles del personal de Atención Proactiva",
            color_map=value_color_map(proactive_staff, "Perfil", "Total", STAFF_RANKED_COLORS),
            hover_percent_only=True,
        )
        show_bar_chart(
            patient_interventions,
            "Intervención",
            "Total",
            "Intervenciones a pacientes con Atención Proactiva",
            horizontal=True,
        )
        chart_col1, chart_col2 = st.columns(2)
        with chart_col1:
            show_bar_chart(
                ethnicity,
                "Grupo",
                "Total",
                "Población indígena/afromexicana atendida, por grupo",
                horizontal=True,
            )
        with chart_col2:
            show_bar_chart(
                migrant,
                "Grupo",
                "Total",
                "Población Migrante atendida",
                horizontal=True,
            )
        visit_conclusion = visit_conclusion_summary(filtered)
        show_bar_chart(
            visit_conclusion,
            "Conclusión de la visita",
            "Total",
            "Conclusión de la visita",
        )
    with tab4:
        show_filter_summary(filter_selections)
        if filtered.empty:
            st.warning("No hay registros con los filtros seleccionados.")
        prevention_summary = prevention_promotion_summary(filtered)
        health_talks = health_talks_summary(filtered)
        render_prevention_promotion(prevention_summary, health_talks)

    st.markdown(
        '<div class="app-footer">Estrategia de Atención Proactiva. IMSS-Bienestar - '
        'Coordinación de Unidades de Primer Nivel. 29 de julio de 2026</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
