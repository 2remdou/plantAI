import streamlit as st
import pandas as pd
import requests
import json
import base64
from llm import get_llm_response
st.title('PlantAI', )


def get_identification(image_file):
    url = "https://plant.id/api/v3/identification?language=fr&details=common_names,description,edible_parts,watering,propagation_methods,synonyms,description_all,description_gpt,best_watering,best_light_conditions,best_soil_condition"
    payload = {
        "images": image_file,
    }
    headers = {
        "Api-Key": st.secrets['PLANT_ID_API_KEY'],
        "Content-Type": "application/json"
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(payload))
    return response.json()

st.subheader('Selectionner ou charger une image')

left_column, right_column = st.columns(2)
plante = {}
with left_column:
    image_file = st.file_uploader('Upload Images', type=['jpg', 'png', 'jpeg'])
with right_column:
    if image_file is not None:
        st.image(image_file)

if image_file is not None:
    st.session_state['image_file'] = image_file
    button = st.button('Analyser')
    if button:
        st.write('Analyse en cours...')
        base64_image = base64.b64encode(image_file.getvalue()).decode('utf-8')
        response = get_identification(image_file=base64_image)
        # st.json(response)
        # response = json.load(open('detail.json'))           
        plante['access_token'] = response['access_token']
        plante['suggestions'] = response['result']['classification']['suggestions']
        plante['is_plant'] = response['result']['is_plant']
        if plante['is_plant']["probability"] > 0.5:
            plante_name = plante['suggestions'][0]['name']
            plante_data = get_llm_response(plante_name)

            plante_data = plante_data.replace('```json', '').replace('```', '')
            plante_json = json.loads(plante_data)
            nom_commun = plante_json['nom_commun']
            probabilite = plante['suggestions'][0]['probability']*100
            color = 'green' if probabilite > 50 else 'red'
            description = plante_json['description']
            nom_scientifique = plante_json['nom_scientifique']
            description_plant_id = plante['suggestions'][0]['details']['description']
            citation = None
            if 'citation' in description_plant_id:
                citation = description_plant_id['citation']
            st.markdown(f'### [{plante_name}]({citation}) à <span style="color: {color}"> {probabilite:.2f}%</span> de chance', unsafe_allow_html=True)
            st.markdown(f'##### Nom commun: {nom_commun}')
            st.markdown(f'##### Nom scientifique: {nom_scientifique}')
            if 'common_names' in plante['suggestions'][0]['details']:
                common_names = plante["suggestions"][0]["details"]["common_names"]
                if common_names is not None:
                    st.markdown(f'**Autres noms:** {", ".join(common_names) }')
            else:
                if 'synonyms' in plante['suggestions'][0]['details']:
                    synonyms = plante['suggestions'][0]['details']['synonyms']
                    if synonyms is not None:
                        st.markdown(f'**Synonymes:** {", ".join(synonyms) }')
            st.divider()
            st.subheader('Description')
            st.write(description)
            st.divider()
            st.markdown(f'#### Entretien')
            entretien = plante_json['entretien']
            col1, col2, col3 = st.columns(3)
            with col1:
                lumiere = entretien['lumiere']
                st.markdown(f'##### Lumiere')
                st.write(lumiere)
            with col2:
                arrosage = entretien['arrosage']
                st.markdown(f'##### Arrosage')
                st.markdown(f'**Frequence:** {arrosage["frequence"]}')
                st.markdown(f'{arrosage["quantite"]}')
            with col3:
                temperature = entretien['temperature']
                st.markdown(f'##### Temperature')
                st.markdown(f'**Minimale:** {temperature["minimale"]}')
                st.markdown(f'**Optimale:** {temperature["optimale"]}')
            sol = entretien['sol']
            engrais = entretien['engrais']
            st.divider()
            st.markdown(f'#### Problèmes courants')
            problemes_courants = plante_json['problemes_courants']
            if 'maladies' in problemes_courants:
                st.markdown(f'##### Maladies')
                maladies = problemes_courants['maladies']
                pd_maladies = pd.DataFrame(maladies)
                st.dataframe(pd_maladies, hide_index=True)
            if 'parasites' in problemes_courants:
                st.markdown(f'##### Parasites')
                parasites = problemes_courants['parasites']
                pd_parasites = pd.DataFrame(parasites)
                st.dataframe(pd_parasites, hide_index=True)
            if 'stress' in problemes_courants:
                st.markdown(f'##### Stress')
                stress = problemes_courants['stress']
                pd_stress = pd.DataFrame(stress)
                st.dataframe(pd_stress, hide_index=True)
        else:
            st.error('Cette image n\'est probablement pas une plante')
    if 'response' in st.session_state:
        st.json(st.session_state['response'])


    
