import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import json
import statistics
import mplcursors

st.set_page_config(page_title="Zahlenanalyse – Q1 Lernapp", layout="centered")

st.title("📊 Zahlenanalyse – Lernapp (Q1)")
st.write("Gib ganze Zahlen ein und analysiere sie Schritt für Schritt.")

# -----------------------------
# Eingabe
# -----------------------------

text_input = st.text_area(
    "Ganze Zahlen eingeben (mit Leerzeichen oder Komma trennen):",
    height=120
)

def parse_numbers(text):
    try:
        numbers = list(map(int, text.replace(",", " ").split()))
        if not numbers:
            raise ValueError
        return numbers
    except:
        st.error("❌ Bitte nur ganze Zahlen eingeben.")
        return None

# -----------------------------
# Analyse
# -----------------------------

if st.button("🔍 Analysieren"):
    numbers = parse_numbers(text_input)

    if numbers:
        analysis = {
            "Aufsteigend": sorted(numbers),
            "Absteigend": sorted(numbers, reverse=True),
            "Maximum": max(numbers),
            "Minimum": min(numbers),
            "Positive Zahlen": [n for n in numbers if n >= 0],
            "Negative Zahlen": [n for n in numbers if n < 0],
            "Durchschnitt": statistics.mean(numbers),
            "Wiederholungen": {n: numbers.count(n) for n in sorted(set(numbers))}
        }

        st.session_state["numbers"] = numbers
        st.session_state["analysis"] = analysis

# -----------------------------
# Ausgabe Text
# -----------------------------

if "analysis" in st.session_state:
    st.subheader("📘 Analyseergebnisse")

    a = st.session_state["analysis"]

    st.write("**Sortiert (aufsteigend):**", a["Aufsteigend"])
    st.write("**Sortiert (absteigend):**", a["Absteigend"])
    st.write("**Höchster Wert:**", a["Maximum"])
    st.write("**Tiefster Wert:**", a["Minimum"])
    st.write("**Positive Zahlen:**", a["Positive Zahlen"])
    st.write("**Negative Zahlen:**", a["Negative Zahlen"])
    st.write("**Durchschnitt:**", round(a["Durchschnitt"], 2))

    st.write("**Wiederholungen:**")
    st.json(a["Wiederholungen"])

# -----------------------------
# Diagramm
# -----------------------------

if "numbers" in st.session_state:
    st.subheader("📈 Interaktives Diagramm")

    numbers = st.session_state["numbers"]
    mean = st.session_state["analysis"]["Durchschnitt"]

    fig, ax = plt.subplots()
    line = ax.plot(numbers, marker="o", label="Zahlen")[0]

    ax.axhline(mean, linestyle="--", label="Durchschnitt")
    ax.scatter(
        [i for i, n in enumerate(numbers) if n == max(numbers)],
        [max(numbers)] * numbers.count(max(numbers)),
        color="green", s=80, label="Maximum"
    )
    ax.scatter(
        [i for i, n in enumerate(numbers) if n == min(numbers)],
        [min(numbers)] * numbers.count(min(numbers)),
        color="red", s=80, label="Minimum"
    )

    ax.set_xlabel("Position")
    ax.set_ylabel("Wert")
    ax.set_title("Zahlenfolge mit Hoch- & Tiefpunkten")
    ax.legend()
    ax.grid(True)

    cursor = mplcursors.cursor(line, hover=True)
    cursor.connect(
        "add",
        lambda sel: sel.annotation.set_text(
            f"Wert: {numbers[int(sel.target.index)]}"
        )
    )

    st.pyplot(fig)

# -----------------------------
# Speichern & Laden
# -----------------------------

st.subheader("💾 Projekt speichern / laden")

if "numbers" in st.session_state:
    project = json.dumps(st.session_state["numbers"])
    st.download_button(
        "⬇️ Projekt speichern",
        data=project,
        file_name="zahlen_projekt.json",
        mime="application/json"
    )

uploaded = st.file_uploader("📂 Projekt laden", type="json")
if uploaded:
    loaded_numbers = json.load(uploaded)
    st.session_state["numbers"] = loaded_numbers
    st.session_state["analysis"] = {
        "Aufsteigend": sorted(loaded_numbers),
        "Absteigend": sorted(loaded_numbers, reverse=True),
        "Maximum": max(loaded_numbers),
        "Minimum": min(loaded_numbers),
        "Positive Zahlen": [n for n in loaded_numbers if n >= 0],
        "Negative Zahlen": [n for n in loaded_numbers if n < 0],
        "Durchschnitt": statistics.mean(loaded_numbers),
        "Wiederholungen": {n: loaded_numbers.count(n) for n in sorted(set(loaded_numbers))}
    }
    st.success("✅ Projekt erfolgreich geladen!")
