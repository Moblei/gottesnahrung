import streamlit as st
import openai
import json
import os

# === Setup ===
openai.api_key = st.secrets["OPENAI_API_KEY"]
st.set_page_config(page_title="Ist das Gottesnahrung?", layout="centered", page_icon="🥩")
st.title("🥩 Ist das Gottesnahrung?")

# === Blacklist & Whitelist laden ===
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

eingabe = st.text_input("Gib ein Lebensmittel oder Produkt ein:", placeholder="z. B. Protein Pulver Vanille", value="")

if st.button("Checken"):
    produkt = eingabe.strip().lower()

    if produkt == "":
        st.warning("Bitte gib etwas ein.")
    elif produkt in [item.lower() for item in whitelist]:
        st.success("✅ Gottesnahrung – approved von der Rohgang. Ehre, wer Ehre verdient.")
    elif produkt in [item.lower() for item in blacklist]:
        st.error("❌ Auf gar keinen Fall – das schreit nach Industrie und Verirrung.")
    else:
        with st.spinner("Bewertung durch die Rohgang läuft..."):
            prompt = (
                f"Ein Nutzer möchte wissen, ob folgendes Produkt 'Gottesnahrung' ist: {eingabe}\n"
                "Bewerte es aus Sicht eines fanatischen Rohkost-Befürworters:\n"
                "- Natürlich, unverarbeitet = ✅\n"
                "- Verarbeitet, mit Zusätzen, Samenöl = ❌\n"
                "- Pflanzlich okay, solange roh und naturbelassen\n"
                "- Tierisch okay, roh oder traditionell zubereitet (z. B. gekochtes Ei, Steak, Innereien)\n"
                "- More Nutrition, Booster, Proteinpulver = No-Go\n"
                "Kategorien: ✅ Gottesnahrung, 🤔 Vielleicht, ❌ Auf gar keinen Fall\n"
                "Antwort auf Deutsch, Emoji + Kategorie zuerst, dann kurzer ironischer Kommentar."
            )

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Du bist ein radikaler, ironischer Rohkost-Guru mit Humor."},
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

# === Community-Vorschlag: lokal speichern ===
st.markdown("---")
st.subheader("🍽️ Community-Vorschlag")

food = st.text_input("Lebensmittel einreichen:", placeholder="z. B. Knäckebrot mit Hüttenkäse")
bewertung = st.selectbox("Deine Einschätzung", ["✅ Gottesnahrung", "🤔 Vielleicht", "❌ Auf gar keinen Fall"])

if st.button("Einreichen"):
    if food.strip() == "":
        st.warning("Bitte gib ein Lebensmittel ein.")
    else:
        eintrag = {"produkt": food.strip(), "bewertung": bewertung}
        try:
            if os.path.exists("community_submissions.json"):
                with open("community_submissions.json", "r", encoding="utf-8") as f:
                    daten = json.load(f)
            else:
                daten = []

            daten.append(eintrag)

            with open("community_submissions.json", "w", encoding="utf-8") as f:
                json.dump(daten, f, ensure_ascii=False, indent=2)

            st.success("Danke für deinen Beitrag zur Wahrheit der Nahrung 🙌")
        except Exception as e:
            st.error(f"Fehler beim Speichern: {e}")

# === Footer ===
st.markdown("""
---
🍯 Eine satirische App im Geiste der Rohgang. Gebaut mit 🐍 & ❤️ von Moritz & GPT.
""")
