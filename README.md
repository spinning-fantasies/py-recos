# py-recos

> Une liste de #recommandations qui s'envoie par email ou par SMS quand on se trouve dans une ville et qu'on cherche des choses à faire ou à visiter.

## TODO LIST

### Backend

- [x] Fonction de liste des activités 
- [x] Fonction d'ajout, edition, suppression des activités
- [ ] Fonction d'envoi de SMS (api free mobile pour le POC)
- [ ] Fonction d'envoi d'email
- [ ] Développement de la base de données d'activités sur Brest, Grenoble, Lannion, Morlaix, Montpellier, Nantes, Paris, Quimper, Rennes

### Frontend (mobile friendly)

- [x] Interface de liste des activités filtrées par localisation 
- [x] Interface d'ajout, edition, suppression des activités


## Usage

Install the dependency:

```
pip install flask
```

Run the ``app.py`` script to create the SQLite database and tables using schema.sql:

```
python app.py
```

This will create the ``activities.db`` file in the project directory and initialize the tables.

The Flask server should be up and running. Open your web browser and go to http://127.0.0.1:5000



