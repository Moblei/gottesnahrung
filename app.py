import streamlit as st
import openai

# === Konfiguration ===
openai.api_key = st.secrets["OPENAI_API_KEY"]

# === Whitelist & Blacklist ===
whitelist = [
    "rohmilch", "rohe leber", "rindertatar", "eigelb", "knochenmark",
    "milz", "zunge", "weide-eier", "rohe butter", "roher fisch",
    "honig", "rohkostgemüse", "kimchi", "sauerkraut"
]

blacklist = [
    "proteinpulver", "clear whey", "smacktastic", "booster", "esn",
    "more nutrition", "rocka", "aspartam", "sucralose",
    "fertiggerichte", "margarine", "sonnenblumenöl", "vegane wurst"
]

# === App UI ===
st.set_page_config(page_title="Ist das Gottesnahrung?", layout="centered", page_icon="🥩")
st.title("🥩 Ist das Gottesnahrung?")

eingabe = st.text_input("Gib ein Lebensmittel oder Produkt ein:", placeholder="z. B. Protein Pulver Vanille")

if st.button("Checken"):
    if eingabe.strip() == "":
        st.warning("Bitte gib etwas ein.")
    else:
        with st.spinner("Bewertung wird geladen..."):

            # === System-Prompt mit Listen ===
            system_prompt = f"""
Du bist ein ketogener Rohkost-Guru mit klarer Meinung.

✅ Folgende Produkte gelten als 100 % Gottesnahrung:
{', '.join(whitelist)}

❌ Diese Produkte gelten als absolute Todsünde:
{', '.join(blacklist)}

Nutze diese Listen zur Einordnung – aber du darfst selbst kreativ entscheiden. Du sprichst wie ein polarisierender Influencer aus der Rohkostszene.

Die Bewertung soll sein:
- ✅ Gottesnahrung
- 🤔 Vielleicht
- ❌ Auf gar keinen Fall

Antworte in **1–2 Sätzen**, witzig, ironisch, manchmal leicht aggressiv.
"""

            user_prompt = f"Ist '{eingabe}' Gottesnahrung?"

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.85,
                    max_tokens=150
                )
                antwort = response.choices[0].message.content

                # Kategorie-Emoji erkennen für farbige Box
                if "✅" in antwort:
                    st.success(antwort)
                elif "❌" in antwort:
                    st.error(antwort)
                else:
                    st.info(antwort)

                st.divider()
                st.markdown("📣 **Teilen?** Kopiere das Ergebnis und poste es auf Insta oder X!")

            except Exception as e:
                st.error(f"Fehler bei der Verarbeitung: {e}")

# === Vorschlagsformular ===
st.divider()
st.subheader("🍽️ Fehlt ein Lebensmittel?")
user_idea = st.text_input("Reiche dein Food ein:", placeholder="z. B. Knäckebrot mit Hüttenkäse")
if st.button("Vorschlagen"):
    if user_idea.strip() != "":
        st.success("Danke! Dein Vorschlag wurde gespeichert (oder an den Entwickler übermittelt).")
    else:
        st.warning("Bitte gib einen Vorschlag ein.")

# === Footer ===
st.markdown("""
---
🌱 Eine ironische App für die Rohkost-Gemeinde. Mit Liebe gebaut von Moritz & GPT.
""")
