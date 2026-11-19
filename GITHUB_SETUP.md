# Obrir el projecte i pujar-lo a GitHub

Nom proposat del repositori: `neutron-star-cooling`. Aquest paquet no inclou cap historial `.git` ni cap connexió remota.

## 1. Descomprimir i obrir

Descomprimeix `neutron-star-cooling-github.zip` on vulgues treballar. En Terminal, entra en la carpeta descomprimida, per exemple:

```bash
cd ~/Documents/neutron-star-cooling
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r code/requirements.txt
```

Si no tens l'ordre `python3.13`, usa `python3` després de comprovar `python3 --version`. En VSCode obri `neutron-star-cooling.code-workspace` amb **File > Open Workspace from File**. Alternativament, `code neutron-star-cooling.code-workspace` si tens instal·lada l'ordre `code`.

Selecciona `.venv/bin/python` amb **Python: Select Interpreter** si VSCode conserva un intèrpret anterior. El workspace proporciona aquesta ruta relativa com a valor per defecte.

Comprova un exemple curt:

```bash
python code/cooling_driver.py --no-animation --final-years 1000 --out results/short
```

## 2. Crear un repositori buit a GitHub

En [github.com/new](https://github.com/new), usa el compte `jpons19` i el nom `neutron-star-cooling` (o el que preferisques). Tria la visibilitat. Deixa desmarcada l'opció d'afegir README i no inicialitzes llicència ni `.gitignore`: el paquet ja té README i `.gitignore`. Aquesta seqüència pressuposa un repositori nou i buit.

## 3. Inicialitzar Git i pujar

Des de l'arrel del projecte:

```bash
git init -b main
git add .
git status --short
git commit -m "Initial cooling code, reproducible examples and article draft"
git remote add origin git@github.com:jpons19/neutron-star-cooling.git
git push -u origin main
```

Canvia el nom en l'URL si has triat un altre repositori. La connexió SSH del teu compte ja es va comprovar en la sessió anterior. Si l'agent no té la clau carregada:

```bash
ssh-add ~/.ssh/id_ed25519
ssh -T git@github.com
```

El missatge d'autenticació correcta indica que GitHub no proporciona accés de shell; és normal. No desactives la verificació de claus de servidor. Si `git commit` demana identitat, configura el teu nom i l'adreça que uses a GitHub amb `git config user.name "..."` i `git config user.email "..."`.

Després del push, refresca la pàgina: haurien d'aparéixer `code/`, `examples/`, `docs/` i el README amb les figures. Comprova també `docs/article/main.pdf` i les ordres d'exemple del README.

## 4. Canvis posteriors

```bash
git status
git add code examples docs README.md
git commit -m "Describe the scientific or code change"
git push
```

Els resultats nous, `.venv`, les caches i els auxiliars de LaTeX s'ignoren. Les figures i dades curades dins de `reference/` sí que es versionen. Per publicar una primera versió reproduïble, pots crear després una etiqueta Git i una release a GitHub; no cal per al primer push.

Referència oficial: [Adding locally hosted code to GitHub](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github?platform=mac).
