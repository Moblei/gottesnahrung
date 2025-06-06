import streamlit as st
import openai

# === Konfiguration ===
openai.api_key = st.secrets["OPENAI_API_KEY"]

# === Whitelist & Blacklist (harte Regeln) ===
WHITELIST = [
    "rohmilch", "rohmilchkäse", "ziegenmilch", "tatar", "rindertatar", "leber", "eigelb",
    "knochenbrühe", "fermentiertes gemüse", "sauerkraut", "kimchi", "butter", "ghee", "schmalz",
    "tierisches fett", "wildlachs", "sardinen", "makrele", "rohe eier"
]

BLACKLIST = [
    "more nutrition", "esn", "rocka", "proteinpulver", "clear whey", "booster",
    "energy drink", "smacktastic", "veganer fleischersatz", "soja", "fertigprodukt",
    "riegel", "gummibärchen", "tütensuppe", "functional water", "süßstoff", "emulgator",
    "aroma", "künstlich", "pflanzliches eiweiß", "sojaprotein"
]

# === App UI ===
st.set_page_config(page_title="Ist das Gottesnahrung?", layout="centered", page_icon="🥩")
st.title("🥩 Ist das Gottesnahrung?")

# Eingabe
eingabe = st.text_input("Gib ein Lebensmittel oder Produkt ein:", placeholder="z. B. Protein Pulver Vanille")

# Check-Funktion
if st.button("Checken"):
    if eingabe.strip() == "":
        st.warning("Bitte gib etwas ein.")
    else:
        clean_input = eingabe.strip().lower()

        # Harte Regel: Blacklist
        if any(item in clean_input for item in BLACKLIST):
            st.error("❌ Auf gar keinen Fall\n\nDas ist Industriepampe par excellence – kein Funken Gottesnahrung in Sicht.")

        # Harte Regel: Whitelist
        elif any(item in clean_input for item in WHITELIST):
            st.success("✅ Gottesnahrung\n\nRein, ursprünglich, tierisch. Der Himmel öffnet seine Pforten.")

        # Sonst: GPT befragen
        else:
            with st.spinner("Bewertung wird geladen..."):
                prompt = f"""
Ein Nutzer möchte wissen, ob folgendes Produkt "Gottesnahrung" ist: {eingabe}

Beurteile es streng nach den folgenden Prinzipien der rohköstlichen Keto-Elite:

Whitelist-Kriterien (✅ automatisch positiv):
- Rohmilch, Rohmilchkäse, Ziegenmilch
- Tatar, Rindertatar, Leber, Eigelb, Knochenbrühe
- Fermentiertes Gemüse, selbstgemachtes Sauerkraut, Kimchi
- Butter, Ghee, Schmalz, tierisches Fett
- Wildlachs, Sardinen, Makrele (natur)
- Rohe Eier, rohe tierische Produkte ohne Zusätze

Blacklist-Kriterien (❌ automatisch negativ):
- Marken wie More Nutrition, ESN, Rocka Nutrition
- Produkte mit Süßstoffen, künstlichen Aromen, Emulgatoren
- Proteinpulver, Clear Whey, Booster
- Energy Drinks, Functional Water, Smacktastic
- Vegane Fleischersatzprodukte, pflanzliche Eiweißquellen, Soja
- Industrielle Fertigprodukte, Riegel, Gummibärchen, Tütensuppen
- Produkte mit über 5 Zutaten oder in Plastikverpackung

Bewerte ALLE anderen Produkte nach diesen Prinzipien:
- Natürlichkeit: je unverarbeiteter, desto besser
- Tierisch schlägt pflanzlich
- Zucker, Samenöle, Soja = absolutes No-Go
- Alles mit mehr als 3 Zutaten = kritisch
- Verarbeitung, Zusatzstoffe und Verpackung stark negativ

Sprache: ironisch, sarkastisch, bissig – aber erkennbar humorvoll.
Antwortkategorien:
✅ Gottesnahrung / 🤔 Vielleicht / ❌ Auf gar keinen Fall

Gib 1 Satz mit Bewertung + 1 kurzen Kommentar zurück (max. 2 Sätze).
"""
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[
                            {"role": "system", "content": "Du bist ein ironischer Rohkost-Keto-Experte."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.9,
                        max_tokens=120
                    )
                    antwort = response.choices[0].message.content.strip()
                    if antwort.startswith("✅"):
                        st.success(antwort)
                    elif antwort.startswith("❌"):
                        st.error(antwort)
                    else:
                        st.warning(antwort)
                except Exception as e:
                    st.error(f"Fehler bei der Verarbeitung: {e}")

# Fußzeile
st.markdown("""
---
🌱 Eine ironische App für die Rohkost-Gemeinde. Gebaut von Moritz & GPT.
""")
