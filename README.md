# Fooder - Solution Factory

![Logo](https://cdn.discordapp.com/attachments/980840788332253184/988739618197364736/logo_colore_blanc.png)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Fooder is a Recipe recommendation system.
Users can swipe through thousands of recipes with a Tinder like interface and are able to save recipes to their digital cookbook.

# Summary
- [Fooder - Solution Factory](#fooder---solution-factory)
- [Summary](#summary)
- [Global description](#global-description)
- [Prerequisite](#prerequisite)
- [Installation](#installation)
      - [Back](#back)
      - [Front](#front)
- [Screenshots](#screenshots)
- [Authors](#authors)
- [LICENSE](#license)

# Global description
L'alimentation est un sujet au cœur de nombreuses
problématiques : santé, bien être et écologie. Par exemple la
consommation excessive de viande engendre l'émission de
CO2 et une grande consommation d'eau.
Proposer une solution qui suggère des recettes saines, équilibrées, à la fois bonnes et vertueuses.

Ce projet s'inscrit dans le cadre du projet de fin de 3ème année en Data Science, la Solution Factory 2022.

# Prerequisite
Make sure you have installed all of the following prerequisites on your development machine:

- [Conda]("https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html")
- [Python 3.7](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/)
- [nltk](https://www.nltk.org/install.html) 

    ```
    ntlk.download()
    ```
# Installation
1. To install, you first need to clone or download the project.

```bash
git clone https://github.com/TBillaudeau/Solution-Factory
```

2. Install dependencies

```cmd
npm install --global http-server
```

3. Run the website

#### Front
```cmd
cd frontend/
```
```cmd
http-server
```
#### Back
```cmd
cd backend/
```
```cmd
python -m venv venv
```
```cmd
venv/Scripts/activate.bat
```
```cmd
pip install flask flask-cors
```
```cmd
pip install pandas
```
```cmd
python app.py
```

# Screenshots
![App Screenshot](Screenshots/swipePage.png)

# Authors
This project have been designed and developped by :
- `Louis Arbey`
- `Thomas Billaudeau`
- `Pierre-Louis Cretinon`
- `Eva Chambaron`
- `Hugo Nahon--Bernical`
- `Marc Bernard`

# LICENSE
[MIT](https://choosealicense.com/licenses/mit/)
