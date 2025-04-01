import streamlit as st
# Configuration de la page
st.set_page_config(page_title="Dashboard Projet Yeleen", layout="wide")
import pandas as pd
import plotly.express as px
import sqlite3

# Configuration des couleurs professionnelles du dashboard
st.markdown("""
    <style>
        .stApp {
            background-color: #0F172A;
            color: #FFFFFF;
        }
        h1, h2, h3, h4 {
            color: #22C55E;
        }
        .stTabs [data-baseweb="tab-highlight"] {
            background-color: #22C55E;
        }
        div[data-testid="stSidebar"] {
            background-color: #22C55E;
            color: #000000;
        }
        div.stButton button {
            background-color: #22C55E;
            color: #FFFFFF;
        }
    </style>
""", unsafe_allow_html=True)



# Logos
col1, col2, col3 = st.columns([1, 6, 1])
with col1:
    st.image("logos/logo-cesag.jpg", width=150)
with col3:
    st.image("logos/Sonabel.png", width=150)

st.markdown("<h1 style='text-align:center;color:white;'>Dashboard Projet Yeleen</h1>", unsafe_allow_html=True)

# Connexion à SQLite
conn = sqlite3.connect("indicateurs.db")
cursor = conn.cursor()

# Chargement des données
df = pd.read_sql("SELECT rowid, * FROM historique", conn)
df["date"] = pd.to_datetime(df["date"])

# Sidebar pour sélection dynamique
st.sidebar.header("Sélection des Indicateurs")
indicateurs_selectionnes = st.sidebar.multiselect(
    "Indicateurs à afficher :",
    df["indicateurs"].unique(),
    default=df["indicateurs"].unique()
)

# Mot de passe sécurisé
PASSWORD = "yeleencsa2025"

# Formulaire protégé par mot de passe
st.sidebar.markdown("---")
st.sidebar.header("Actualisation des Indicateurs")
password = st.sidebar.text_input("Entrez le mot de passe pour modifier les données", type="password")

if password == PASSWORD:
    with st.sidebar.form("actualisation"):
        date_new = st.date_input("Date de l'indicateur")
        domaine_new = st.selectbox("Domaine de l'indicateur", df["indicateurs"].unique())
        valeur_new = st.number_input("Valeur de l'indicateur", min_value=0)
        submitted = st.form_submit_button("Ajouter")

        if submitted:
            cursor.execute("INSERT INTO historique (date, indicateurs, valeur) VALUES (?, ?, ?)",
                           (date_new.strftime('%Y-%m-%d'), domaine_new, valeur_new))
            conn.commit()
            st.success("Nouvel indicateur ajouté avec succès !")
            st.experimental_rerun()
else:
    st.sidebar.warning("Veuillez entrer un mot de passe valide pour modifier les données.")

# Dashboard structuré en onglets
onglets = st.tabs(["Historique", "Résumé", "Détails", "Carte", "Commentaires"])

# Onglet Historique
with onglets[0]:
    st.header("Historique des indicateurs")
    df_historique = df[df["indicateurs"].isin(indicateurs_selectionnes)]
    fig = px.line(df_historique, x="date", y="valeur", color="indicateurs", markers=True,
                  title="Évolution Temporelle des Indicateurs")
    st.plotly_chart(fig, use_container_width=True)

# Onglet Résumé
with onglets[1]:
    st.header("Résumé moyen par indicateur")
    df_resume = df.groupby("indicateurs")["valeur"].mean().reset_index()
    fig_resume = px.bar(df_resume, x="indicateurs", y="valeur", color="indicateurs", title="Résumé des Indicateurs")
    st.plotly_chart(fig_resume, use_container_width=True)

# Onglet Détails
with onglets[2]:
    st.header("Détails des indicateurs")
    st.dataframe(df[df["indicateurs"].isin(indicateurs_selectionnes)])

    st.markdown("---")
    if st.button("Actualiser les données"):
        st.experimental_rerun()

    if password == PASSWORD:
        st.markdown("### Supprimer une entrée")
        delete_id = st.number_input("ID de l'entrée à supprimer", min_value=1, max_value=df["rowid"].max())
        if st.button("Supprimer"):
            cursor.execute("DELETE FROM historique WHERE rowid=?", (delete_id,))
            conn.commit()
            st.success("Entrée supprimée avec succès !")
            st.experimental_rerun()
    else:
        st.warning("Entrez le mot de passe dans la barre latérale pour supprimer des entrées.")

# Onglet Carte
with onglets[3]:
    st.header("Carte des Localités Électrifiées")
    df_localites = pd.DataFrame({
        "Localité": ["Ouagadougou", "Bobo-Dioulasso", "Koudougou", "Banfora", "Dédougou"],
        "Latitude": [12.3714, 11.1772, 12.2526, 10.6333, 12.4550],
        "Longitude": [-1.5197, -4.2979, -2.3627, -4.7667, -3.4640]
    })
    fig_map = px.scatter_mapbox(
        df_localites, lat="Latitude", lon="Longitude", hover_name="Localité", zoom=6,
        mapbox_style="carto-positron", title="Localités Électrifiées"
    )
    st.plotly_chart(fig_map, use_container_width=True)

# Onglet Commentaires
with onglets[4]:
    st.header("Commentaires des utilisateurs")
    commentaire = st.text_area("Votre commentaire")
    if st.button("Soumettre le commentaire"):
        cursor.execute("CREATE TABLE IF NOT EXISTS commentaires (commentaire TEXT)")
        cursor.execute("INSERT INTO commentaires (commentaire) VALUES (?)", (commentaire,))
        conn.commit()
        st.success("Merci pour votre commentaire !")

# Footer
st.markdown("---")
st.write("### Auteur")
st.markdown("""
**Célestin Kambou**  
📧 celkam707@gmail.com  
🌍 [LinkedIn](https://www.linkedin.com/in/c%C3%A9lestin-kambou-eng-cem%C2%AE-phd-683748a4/)  
© 2025 Tous droits réservés
""")
