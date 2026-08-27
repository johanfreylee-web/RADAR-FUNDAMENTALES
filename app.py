import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="Radar Value Investing", page_icon="🔍", layout="wide")

st.title("🔍 Radar Value Investing: Escáner de Descuento DCF")
st.caption("Estimación de valor intrínseco por Flujo de Caja Descontado (DCF) y margen de seguridad.")

# ----------------------------
# Parámetros configurables
# ----------------------------
with st.sidebar:
    st.header("⚙️ Parámetros del modelo")
    wacc = st.slider("WACC (tasa de descuento)", 0.05, 0.15, 0.09, 0.005, format="%.3f")
    tasa_perpetua = st.slider("Crecimiento a perpetuidad", 0.01, 0.04, 0.025, 0.005, format="%.3f")
    crecimiento_min = st.slider("Crecimiento mínimo asumido", 0.0, 0.10, 0.05, 0.01, format="%.2f")
    crecimiento_max = st.slider("Crecimiento máximo asumido", 0.05, 0.30, 0.15, 0.01, format="%.2f")
    umbral_oportunidad = st.slider("Umbral de oportunidad crítica (%)", 10, 70, 50, 5)

# ----------------------------
# Input de tickers
# ----------------------------
tickers_default = "DECK, V, ADBE, NVO, NU, MSFT, MELI, FVRR"
tickers_input = st.text_input("Ingresá los tickers separados por coma:", tickers_default)
correr = st.button("🚀 Correr análisis", type="primary")


def analizar_ticker(ticker, wacc, tasa_perpetua, crecimiento_min, crecimiento_max):
    empresa = yf.Ticker(ticker)

    precio_actual = empresa.history(period="1d")['Close'].iloc[-1]

    flujo_caja = empresa.cashflow
    estado_resultados = empresa.financials

    if 'Free Cash Flow' in flujo_caja.index:
        fcf_actual = flujo_caja.loc['Free Cash Flow'].iloc[0]
    elif 'Operating Cash Flow' in flujo_caja.index:
        fcf_actual = flujo_caja.loc['Operating Cash Flow'].iloc[0]
    else:
        raise ValueError("No se encontró Free Cash Flow ni Operating Cash Flow")

    ventas = estado_resultados.loc['Total Revenue']
    tasa_crecimiento = (ventas.iloc[0] - ventas.iloc[1]) / ventas.iloc[1]
    tasa_crecimiento = max(min(tasa_crecimiento, crecimiento_max), crecimiento_min)

    fcf_proyectado = []
    fcf_temporal = fcf_actual
    for i in range(1, 6):
        fcf_temporal *= (1 + tasa_crecimiento)
        fcf_descontado = fcf_temporal / ((1 + wacc) ** i)
        fcf_proyectado.append(fcf_descontado)

    valor_terminal = (fcf_temporal * (1 + tasa_perpetua)) / (wacc - tasa_perpetua)
    valor_terminal_descontado = valor_terminal / ((1 + wacc) ** 5)

    valor_empresa_total = sum(fcf_proyectado) + valor_terminal_descontado

    acciones_totales = empresa.info.get('sharesOutstanding')
    if not acciones_totales:
        raise ValueError("No se encontró el número de acciones en circulación")

    valor_intrinseco_accion = valor_empresa_total / acciones_totales

    if valor_intrinseco_accion > precio_actual:
        margen_seguridad = (1 - (precio_actual / valor_intrinseco_accion)) * 100
    else:
        margen_seguridad = 0

    return {
        "Ticker": ticker,
        "Precio Mercado": round(precio_actual, 2),
        "Valor Intrínseco": round(valor_intrinseco_accion, 2),
        "Margen Seguridad %": round(margen_seguridad, 1),
        "Crecimiento Usado %": round(tasa_crecimiento * 100, 1),
    }


if correr:
    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

    if not tickers:
        st.warning("Ingresá al menos un ticker.")
    else:
        resultados = []
        errores = []
        progreso = st.progress(0, text="Procesando...")

        for i, ticker in enumerate(tickers):
            try:
                resultados.append(
                    analizar_ticker(ticker, wacc, tasa_perpetua, crecimiento_min, crecimiento_max)
                )
            except Exception as e:
                errores.append(f"{ticker}: {e}")
            progreso.progress((i + 1) / len(tickers), text=f"Procesando {ticker}...")

        progreso.empty()

        if resultados:
            df = pd.DataFrame(resultados).sort_values("Margen Seguridad %", ascending=False)

            def clasificar(margen):
                if margen >= umbral_oportunidad:
                    return f"🔥 Oportunidad crítica (≥{umbral_oportunidad}%)"
                elif margen > 0:
                    return "✅ Con descuento"
                else:
                    return "❌ Sobrevalorada"

            df["Veredicto"] = df["Margen Seguridad %"].apply(clasificar)

            st.subheader("📊 Resultados")
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Precio Mercado": st.column_config.NumberColumn(format="$%.2f"),
                    "Valor Intrínseco": st.column_config.NumberColumn(format="$%.2f"),
                    "Margen Seguridad %": st.column_config.NumberColumn(format="%.1f%%"),
                    "Crecimiento Usado %": st.column_config.NumberColumn(format="%.1f%%"),
                },
            )

            st.subheader("📈 Margen de seguridad por acción")
            chart_df = df.set_index("Ticker")["Margen Seguridad %"]
            st.bar_chart(chart_df)

            oportunidades = df[df["Margen Seguridad %"] >= umbral_oportunidad]
            if not oportunidades.empty:
                st.success(
                    f"🚨 {len(oportunidades)} oportunidad(es) crítica(s) encontrada(s): "
                    + ", ".join(oportunidades["Ticker"].tolist())
                )

        if errores:
            with st.expander(f"⚠️ {len(errores)} ticker(s) con errores"):
                for err in errores:
                    st.text(err)

st.divider()
st.caption(
    "⚠️ Este modelo es una simplificación educativa. No constituye asesoramiento financiero. "
    "Los supuestos de crecimiento y WACC afectan fuertemente el resultado."
)
