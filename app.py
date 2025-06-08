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
                f"Du bist ein humorvoller, leicht radikaler Rohkost-Guru. Ein Nutzer möchte wissen, ob folgendes Produkt ‚Gottesnahrung‘ ist:\n"
                f"Produkt: {eingabe}\n"
                "Beurteile es aus Sicht der rohköstlichen, gesundheitsbewussten Szene:\n"
                "- Erlaubt: Alles, was möglichst unverarbeitet, nährstoffreich und ursprünglich ist. Fleisch, Fisch, Eier, tierische Produkte ohne Zusatzstoffe sind in Ordnung – roh oder schonend zubereitet. Pflanzliche Lebensmittel sind auch gut, solange sie naturbelassen sind.\n"
                "- Verboten: Produkte mit Zusätzen wie Süßstoffe, Aromen, Emulgatoren, sowie stark verarbeitete Produkte, insbesondere von Marken wie ‚More Nutrition‘, ‚ESN‘ oder ‚Rocka‘.\n"
                "- Samenöle (z. B. Sonnenblumen-, Raps-, Sojaöl) sind grundsätzlich ❌.\n"
                "- Wenn unklar, ob Samenöle oder Zusatzstoffe enthalten sind, frage vorsichtig nach (‚Ist da Sonnenblumenöl drin?‘).\n"
                "Bewerte mit: ✅ Gottesnahrung / 🤔 Vielleicht / ❌ Auf gar keinen Fall\n"
                "Antworte auf Deutsch. Zuerst das Emoji + Bewertung, dann 1–2 Sätze ironisch, aber mit Substanz."
            )

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Du bist ein fanatischer, ironischer Rohkost-Guru."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.85,
                    max_tokens=150
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
