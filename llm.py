from openai import OpenAI
import json
import streamlit as st

@st.cache_resource
def get_llm_response(plant_name):
    client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'])
    structure_json = {
        "nom_commun": "",
        "nom_scientifique": "",
        "description": "",
        "categorie": "",
        "origine": "",
        "taille_adulte": {
            "hauteur": "",
            "largeur": ""
        },
        "toxicite": {
            "animaux": "",
            "humains": ""
        },
        "entretien": {
            "lumiere": "",
            "arrosage": {
                "frequence": "",
                "quantite": ""
            },
            "humidite": "",
            "temperature": {
                "minimale": "",
                "optimale": ""
            },
            "sol": "",
            "engrais": {
                "frequence": "",
                "type": ""
            },
            "rempotage": "",
            "taille": ""
        },
        "problemes_courants": {
            "maladies": [
                {
                    "nom": "",
                    "symptomes": "",
                    "traitement": ""
                }
            ],
            "parasites": [
                {
                    "nom": "",
                    "symptomes": "",
                    "traitement": ""
                }
            ],
            "stress": [
                {
                    "symptomes": "",
                    "causes": "",
                    "solution": ""
                }
            ]
        },
        "fonctionnalites_utilisateur": {
            "calendrier_entretien": True,
            "reconnaissance_plante": True,
            "historique_soins": True,
            "alertes_meteo": True,
            "suggestions_personnalisees": True
        }
    }
    prompt = f"""Génère un JSON strictement conforme à cette structure pour la plante "{plant_name}" :

    {json.dumps(structure_json, indent=4)}

    Remplis les champs avec des valeurs pertinentes. Assure-toi que la sortie soit un JSON valide, sans texte supplémentaire.
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "Tu es un assistant botanique fournissant des données au format JSON."},
                  {"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

