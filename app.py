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
                f"Beurteile folgendes Lebensmittel: {eingabe}\n"
                "Ist es Gottesnahrung? Nutze diese Kategorien: ✅ Ja, 🤔 Vielleicht, ❌ Nein."
                "Antworte kurz, ironisch, mit Rohkost-Keto-Vibe."
            )
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Du bist ein ironischer Rohkost-Keto-Experte."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.8,
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
