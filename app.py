import streamlit as st
import openai
import json

# === Setup ===
openai.api_key = st.secrets["OPENAI_API_KEY"]
st.set_page_config(page_title="Ist das Gottesnahrung?", layout="centered", page_icon="🥩")
st.title("🥩 Ist das Gottesnahrung?")

# === Whitelist & Blacklist laden ===
with open("whitelist.json", "r", encoding="utf-8") as f:
    whitelist = json.load(f)

with open("blacklist.json", "r", encoding="utf-8") as f:
    blacklist = json.load(f)

# === Vorschläge für schnelleingabe ===
vorschlaege = [
    "Rohmilch",
    "Protein Pulver Vanille",
    "Tatar mit Eigelb",
    "Linsensuppe",
    "Pizza Margherita",
    "More Nutrition Booster",
    "Ziegenkäse roh",
    "Lachs mit Butter"
]

eingabe = st.text_input(
    "Gib ein Lebensmittel oder Produkt ein:",
    placeholder="z. B. Protein Pulver Vanille",
    value=""
)

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

            # === Klarer, differenzierter Prompt ===
            prompt = (
                f"Ein Nutzer möchte wissen, ob folgendes Produkt 'Gottesnahrung' ist: {eingabe}\n"
                "Bewerte es aus Sicht eines radikalen, aber humorvollen Rohkost-Gurus:\n"
                "- Unverarbeitet, naturbelassen, nährstoffreich = ✅ Gottesnahrung\n"
                "- Hoch verarbeitet, Fertigprodukt, Zusatzstoffe, Industriefood (z. B. Pizza, Booster, Proteinpulver, ESN, Rocka) = ❌ Auf gar keinen Fall\n"
                "- Pflanzlich ist okay, solange nicht verarbeitet (Samenöle, Margarine, Emulgatoren etc. sind No-Gos)\n"
                "- Suppe, Salat etc. = 🤔 Vielleicht, je nach Zutaten (nur natürliche erlaubt, keine Samenöle oder Zusatzstoffe)\n"
                "- Keine Rohkost-Dogmen: Gekochte Eier, Suppen, Fleisch etc. sind ok, wenn pur und sauber\n"
                "Sprache: Ironisch, direkt, humorvoll – mit Ehre!\n"
                "Format: Emoji + Kategorie (✅/🤔/❌), dann 1–2 Sätze mit witzigem Kommentar."
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
                antwort = response.choices[0].message.content.strip()

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
st.markdown("🍯 #gottesnahrung #rohgang #ehrenernährung")
