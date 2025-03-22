
## Create a virtual environment
```
mkdir plante
cd plante
python -m venv .venv
```

## Activate the virtual environment

**Windows command prompt**
```
.venv\Scripts\activate.bat
```

**macOS and Linux**
```
source .venv/bin/activate
```


## Install requirements
pip install -r requirements.txt

## Creation du fichier .streamlit/secrets.toml
```
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

# Plant.id
1. Création de compte sur kindwise[https://admin.kindwise.com/signup] pour obtenir un compte API
2. Renseigner PLANT_ID_API_KEY avec la clé API dans le fichier .streamlit/secrets.toml

# OpenAI
1. Créer une clé API sur [https://platform.openai.com/settings/organization/api-keys] 
2. Renseigner OPENAI_API_KEY avec la clé API dans le fichier .streamlit/secrets.toml 

## Run the app
streamlit run app.py