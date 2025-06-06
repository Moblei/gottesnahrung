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

eingabe = st.text_input("Gib ein Lebensmittel oder Produkt ein:", placeholder="z. B. Protein Pulver Vanille", value="")

# === Samenöl-Nachfrage-Logik ===
kritische_woerter = ["salat", "dressing", "suppe", "gemüse", "auflauf", "bowls", "pfanne", "müsli", "brot"]
samen_check = any(wort in eingabe.lower() for wort in kritische_woerter)
nutzerantwort = None

if samen_check:
    st.markdown("👀 **Enthält dein Gericht Samenöle, fertige Dressings oder Zusätze?**")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("✅ Nein, alles natürlich"):
            nutzerantwort = "no_samen"
    with col2:
        if st.button("❌ Ja, Fertigzeug oder Samenöl"):
            st.error("❌ Auf gar keinen Fall – Samenöl detected. Industrieware, die Gott weinen lässt.")
            st.stop()

# === Check starten ===
if st.button("Checken") and eingabe:
    produkt = eingabe.strip().lower()
    if produkt in [item.lower() for item in whitelist]:
        st.success("✅ Gottesnahrung – approved von der Rohgang. Ehre, wer Ehre verdient.")
    elif produkt in [item.lower() for item in blacklist]:
        st.error("❌ Auf gar keinen Fall – das schreit nach Industrie und Verirrung.")
    else:
        with st.spinner("Bewertung durch die Rohgang läuft..."):
            zusatz = ""
            if nutzerantwort == "no_samen":
                zusatz = "\nHinweis: Nutzer bestätigt, dass keine Samenöle oder Fertigprodukte enthalten sind."

            prompt = (
                f"Ein Nutzer möchte wissen, ob folgendes Produkt 'Gottesnahrung' ist: {eingabe}\n"
                f"{zusatz}\n"
                "Bewerte aus Sicht eines extrem kritischen Rohkost-Fans:\n"
                "- Unverarbeitet, natürlich, möglichst tierisch oder urtümlich = ✅\n"
                "- Industrie, Proteinpulver, Booster, Samenöle, ESN, Rocka, More etc. = ❌\n"
                "- Pflanzlich ist ok, solange nicht verarbeitet\n"
                "Sprache: ironisch, pointiert, kurz und witzig.\n"
                "Kategorien: ✅ Gottesnahrung, 🤔 Vielleicht, ❌ Auf gar keinen Fall\n"
                "Antwort auf Deutsch, Emoji + Kategorie zuerst, dann Kommentar."
            )

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "Du bist ein fanatischer, aber ironischer Rohkost-Guru."},
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
                st.error(f"Fehler: {e}")

# Footer
st.markdown("---\n🍯 #gottesnahrung #rohgang")
