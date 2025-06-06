import streamlit as st
import openai
import json
import os

# === OpenAI Key aus secrets laden ===
openai.api_key = st.secrets["OPENAI_API_KEY"]

# === Streamlit Setup ===
st.set_page_config(page_title="Ist das Gottesnahrung?", layout="centered", page_icon="🥩")
st.title("🥩 Ist das Gottesnahrung?")

# === Eingabe-Feld ===
eingabe = st.text_input("Gib ein Lebensmittel oder Produkt ein:", placeholder="z. B. Protein Pulver Vanille")

# === Prompt-Vorlage ===
def build_prompt(food_input):
    return f"""
Ein Nutzer fragt, ob folgendes Produkt 'Gottesnahrung' ist: {food_input}

Beurteile es aus Sicht der Rohkost- und Tierprodukt-Elite (à la Rohgang, Coach Aaron). Sei provokant, ironisch und klar.

🔎 Regeln:
- ✅ Gottesnahrung: Alles, was es schon vor 100 Jahren gab – unverarbeitet, natürlich, tierisch oder pflanzlich. Beispiele: Steak, Eier, Gemüse, fermentiertes Kraut, Brühe, Leber, Olivenöl
- 🤔 Vielleicht: Pflanzlich, roh, naturbelassen – aber nur, wenn nicht mit komischem Dressing oder Zusätzen gekauft
- ❌ Kein Gottesnahrung: Industrieprodukte, Proteinpulver, Booster, veganer Käse, Functional Food, Energy-Drinks, Marken wie More, Rocka, ESN

👀 Merksatz: Was dein Urgroßvater als Essen erkannt hätte, ist safe. Alles andere kommt in den gelben Sack.

🎯 Beginne mit einer Kategorie (✅ / 🤔 / ❌), dann 1–2 freche Sätze im TikTok-Rohkost-Guru-Stil.

Optional Hashtags (#gottesnahrung #rohgangapproved)
"""

# === Bewertung durch OpenAI ===
def gottes_check(food_input):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du bist ein ironischer Rohkost-Keto-Guru."},
                {"role": "user", "content": build_prompt(food_input)}
            ],
            temperature=0.8,
            max_tokens=150
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Fehler: {e}"

# === Button zur Ausführung ===
if st.button("Checken"):
    if eingabe.strip() == "":
        st.warning("Bitte gib ein Produkt ein.")
    else:
        with st.spinner("Bewertung wird geladen..."):
            ergebnis = gottes_check(eingabe)
            # Versuche, Emoji und Text zu splitten
            if ergebnis.startswith("✅"):
                st.success(ergebnis)
            elif ergebnis.startswith("❌"):
                st.error(ergebnis)
            elif ergebnis.startswith("🤔"):
                st.warning(ergebnis)
            else:
                st.info(ergebnis)

# === Fußzeile ===
st.markdown("---")
st.markdown("🌱 Eine ironische App für die Rohkost-Gemeinde. Mit Liebe gebaut von Moritz & GPT.")
