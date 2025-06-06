import streamlit as st
import openai
import json

# === Setup ===
openai.api_key = st.secrets["OPENAI_API_KEY"]
st.set_page_config(page_title="Ist das Gottesnahrung?", layout="centered", page_icon="🥩")
st.title("🥩 Ist das Gottesnahrung?")

# === Load Whitelist & Blacklist ===
with open("whitelist.json", "r", encoding="utf-8") as f:
    whitelist = json.load(f)

with open("blacklist.json", "r", encoding="utf-8") as f:
    blacklist = json.load(f)

# === Vorschläge ===
vorschlaege = [
    "Protein Pulver Vanille",
    "Tatar mit Eigelb",
    "Rohmilch",
    "Smacktastic",
    "Ziegenkäse roh",
    "Booster Apfel",
    "Chia Pudding",
    "Lachs mit Butter"
]

# === Eingabe ===
eingabe = st.text_input("Gib ein Lebensmittel oder Produkt ein:", placeholder="z. B. Protein Pulver Vanille", value="")
antwort = ""

# === Bewertung ===
if st.button("Checken"):
    produkt = eingabe.strip().lower()

    if produkt == "":
        st.warning("Bitte gib etwas ein.")
    elif produkt in [item.lower() for item in whitelist]:
        antwort = "✅ Gottesnahrung – approved von der Rohgang. Ehre, wer Ehre verdient."
        st.success(antwort)
    elif produkt in [item.lower() for item in blacklist]:
        antwort = "❌ Auf gar keinen Fall – das schreit nach Industrie und Verirrung."
        st.error(antwort)
    else:
        with st.spinner("Bewertung durch die Rohgang läuft..."):
            prompt = (
                f"Ein Nutzer möchte wissen, ob folgendes Produkt 'Gottesnahrung' ist: {eingabe}\n"
                "Bewerte es aus Sicht eines radikalen Rohkost-Anhängers:\n"
                "- Roh, tierisch und unverarbeitet = ✅\n"
                "- Verarbeitet, industriell, mit Zusätzen = ❌\n"
                "- Pflanzlich okay, solange naturbelassen\n"
                "- More Nutrition, Booster, Proteinpulver, ESN, Rocka = ❌ absolutes No-Go\n"
                "- Humorvoll, bissig, ironisch antworten\n"
                "Kategorien: ✅ Gottesnahrung, 🤔 Vielleicht, ❌ Auf gar keinen Fall\n"
                "Antwort auf Deutsch, Emoji + Kategorie zuerst, dann kurzer, witziger Kommentar."
            )

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Du bist ein fanatischer, ironischer Rohkost-Guru."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.85,
                    max_tokens=100
                )
                antwort = response.choices[0].message.content
                if "✅" in antwort:
                    st.success(antwort)
                elif "❌" in antwort:
                    st.error(antwort)
                else:
                    st.warning(antwort)

            except Exception as e:
                st.error(f"Fehler bei der Verarbeitung: {e}")


# === Footer ===
st.markdown("""
---
🍯 #gottesnahrung #rohgang
""")
