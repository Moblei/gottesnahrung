import streamlit as st
import openai
import json

# === Setup ===
openai.api_key = st.secrets["OPENAI_API_KEY"]
st.set_page_config(page_title="Ist das Gottesnahrung?", layout="centered", page_icon="🥩")
st.title("🥩 Ist das Gottesnahrung?")

# === Load Whitelist & Blacklist ===
try:
    with open("whitelist.json", "r", encoding="utf-8") as f:
        whitelist = json.load(f)

    with open("blacklist.json", "r", encoding="utf-8") as f:
        blacklist = json.load(f)
except Exception as e:
    st.error(f"Fehler beim Laden der Listen: {e}")
    st.stop()

# === Vorschläge ===
vorschlaege = [
    "Protein Pulver Vanille",
    "Tatar mit Eigelb",
    "Rohmilch",
    "Booster Apfel",
    "Clear Whey",
    "Linsensuppe",
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
        with st.spinner("Bewertung durch die Rohkost-Gemeinde läuft..."):
            prompt = (
                f"Ein Nutzer möchte wissen, ob folgendes Produkt 'Gottesnahrung' ist: {eingabe}\n\n"
                "Antworte aus Sicht eines fanatischen Rohkost-Gurus:\n"
                "- Nur natürliche, unverarbeitete Lebensmittel sind erlaubt\n"
                "- Tierische Produkte wie rohe Milch, Eier, Tatar oder Lachs sind ✅, solange naturbelassen\n"
                "- Pflanzlich ist erlaubt, wenn roh oder naturbelassen – z. B. Salat, rohes Gemüse, Avocado, Beeren\n"
                "- Zusätze, Fertiggerichte, Industrieprodukte, Süßstoffe, Isolate, künstliche Aromen, Booster, Riegel, Whey etc. = ❌\n"
                "- Suppen oder warme Gerichte dürfen nur aus natürlichen Zutaten selbst gemacht sein, keine Zusätze oder Tüten\n"
                "- Samenöle, Margarine, künstliche Zusatzstoffe = ❌\n"
                "- Humorvoll, ironisch, leicht bissig antworten\n"
                "Antwort auf Deutsch. Gib zuerst die Kategorie mit Emoji:\n"
                "✅ Gottesnahrung, 🤔 Vielleicht, ❌ Auf gar keinen Fall\n"
                "Dann ein witziger 1-2 Zeilen Kommentar im Stil der Rohkost-Gang."
            )

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Du bist ein fanatischer, ironischer Rohkost-Guru."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.85,
                    max_tokens=120
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
st.markdown("---")
st.markdown("🍯 #gottesnahrung #rohgang")
