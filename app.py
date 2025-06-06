import streamlit as st
import openai

# === Konfiguration ===
openai.api_key = st.secrets["OPENAI_API_KEY"]

# === Vorschläge ===
vorschlaege = [
    "Protein Pulver Vanille",
    "Käse",
    "Tatar",
    "Smacktastic",
    "Booster Apfel",
    "Clear Whey",
    "Rindertatar mit Eigelb"
]

# === App UI ===
st.set_page_config(page_title="Ist das Gottesnahrung?", layout="centered", page_icon="🥩")
st.title("🥩 Ist das Gottesnahrung?")

# Eingabe mit Vorschlägen
eingabe = st.text_input("Gib ein Lebensmittel oder Produkt ein:", placeholder="z. B. Protein Pulver Vanille")

# Prompt senden
if st.button("Checken"):
    if eingabe.strip() == "":
        st.warning("Bitte gib etwas ein.")
    else:
        with st.spinner("Bewertung wird geladen..."):
            prompt = (
                   f"Ein Nutzer möchte wissen, ob folgendes Produkt 'Gottesnahrung' ist: {eingabe}\n"
    "Beurteile aus Sicht eines radikalen Rohkost-Keto-Vertreters:\n"
    "- Nur naturbelassene tierische Lebensmittel sind wahre Gottesnahrung.\n"
    "- Alles Verarbeitete (auch Proteinpulver) = ❌\n"
    "- Marken wie More Nutrition, ESN, Foodspring = ❌\n"
    "- Sprache: provokant, witzig, mit Haltung.\n"
    "Antwort auf Deutsch, in einem Satz.\n"
    "Kategorien: ✅ Gottesnahrung, 🤔 Vielleicht, ❌ Auf gar keinen Fall."
                "Antwort auf Deutsch, 1–2 Sätze mit Kommentar."
            )
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Du bist ein ketogener Rohkost-Purist mit Humor."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.85,
                    max_tokens=100
                )
                antwort = response.choices[0].message.content
                st.success(antwort)
                st.divider()
                st.markdown("📣 **Teilen?** Kopiere das Ergebnis und teile es auf Insta oder X!")
            except Exception as e:
                st.error(f"Fehler bei der Verarbeitung: {e}")

# Vorschlag einreichen
st.divider()
st.subheader("🍽️ Fehlt ein Lebensmittel?")
user_idea = st.text_input("Reiche dein Food ein:", placeholder="z. B. Knäckebrot mit Hüttenkäse")
if st.button("Vorschlagen"):
    if user_idea.strip() != "":
        st.success("Danke! Dein Vorschlag wurde gespeichert (oder an den Entwickler übermittelt).")
    else:
        st.warning("Bitte gib einen Vorschlag ein.")

# Fußzeile
st.markdown("""
---
🌱 Eine ironische App für die Rohkost-Gemeinde. Mit Liebe gebaut von Moritz & GPT.
""")
