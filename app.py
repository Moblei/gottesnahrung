import streamlit as st
import openai
import json

# === Konfiguration ===
openai.api_key = st.secrets["OPENAI_API_KEY"]

# === Whitelist / Blacklist laden ===
with open("whitelist.json", "r", encoding="utf-8") as f:
    whitelist = json.load(f)

with open("blacklist.json", "r", encoding="utf-8") as f:
    blacklist = json.load(f)

# === App UI ===
st.set_page_config(page_title="Ist das Gottesnahrung?", layout="centered", page_icon="🥩")
st.title("🥩 Ist das Gottesnahrung?")

eingabe = st.text_input("Gib ein Lebensmittel oder Produkt ein:", placeholder="z. B. Protein Pulver Vanille")

if st.button("Checken"):
    if eingabe.strip() == "":
        st.warning("Bitte gib etwas ein.")
    else:
        eingabe_lower = eingabe.strip().lower()

        if any(term in eingabe_lower for term in whitelist):
            st.success("✅ Gottesnahrung! Keine Fragen mehr.")
        elif any(term in eingabe_lower for term in blacklist):
            st.error("❌ Auf gar keinen Fall. Das ist reine Industriebrühe.")
        else:
            with st.spinner("Bewertung wird geladen..."):
                prompt = (
                    f"Ein Nutzer fragt, ob folgendes Produkt Gottesnahrung ist: {eingabe}.\n"
                    "Beurteile aus Sicht der radikalen Rohkost- und Tierprodukt-Fraktion (Rohgang-Style).\n"
                    "Bewertungskriterien:\n"
                    "- Tierisch, roh, unverarbeitet = ✅ Gottesnahrung\n"
                    "- Stark verarbeitet, Industrie, vegane Ersatzprodukte, Samenöle, Booster etc. = ❌ Auf gar keinen Fall\n"
                    "- Graubereiche oder moderne Fitness-Produkte = 🤔 Vielleicht\n"
                    "Sprich ironisch, bissig, gerne leicht provokant – als wärst du Teil der Rohkost-Elite auf TikTok.\n"
                    "Antwortformat: Beginne mit der Kategorie (✅ / 🤔 / ❌), danach 1–2 kurze Sätze Kommentar."
                )

                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "Du bist ein witziger, radikaler Rohkost-Influencer."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.85,
                        max_tokens=100
                    )
                    antwort = response.choices[0].message.content
                    st.success(antwort)
                except Exception as e:
                    st.error(f"Fehler bei der Verarbeitung: {e}")

# === Vorschlag einreichen ===
st.divider()
st.subheader("🍽️ Fehlt ein Lebensmittel?")
user_idea = st.text_input("Reiche dein Food ein:", placeholder="z. B. Smacktastic Brotaufstrich")
if st.button("Vorschlagen"):
    if user_idea.strip() != "":
        st.success("Danke! Dein Vorschlag wurde gespeichert (oder an den Entwickler übermittelt).")
    else:
        st.warning("Bitte gib einen Vorschlag ein.")

# === Fußzeile ===
st.markdown("""
---
🌱 Eine ironisch gemeinte App rund um Rohkost, Keto und TikTok-Kultur.  
Entwickelt mit Liebe von Moritz & GPT.
""")
