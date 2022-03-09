# Železo, beton

Textová adventura ve webovém prohlížeči.

## Pro vývojáře

### Požadavky

- Git
- Python 3.7+
- [Poetry](https://github.com/python-poetry/poetry)
  (návod na instalaci [zde](https://python-poetry.org/docs/master/#installation))
- Firefox
- [geckodriver](https://github.com/mozilla/geckodriver/releases)
  (rozbalenou binárku zkopírujte do některého adresáře obsaženého v PATH, např. `$HOME/.local/bin`)

### Instalace

Naklonujte repozitář a nainstalujte knihovny:

```
git clone https://github.com/underground-lab/zelezobeton.git
cd zelezobeton
poetry install
```

Dále je potřeba vygenerovat tajný klíč pro Django (v adresáři se objeví
soubor `.key`) a inicializovat databázi taktéž pro Django (vytvoří se
soubor `db.sqlite3`):

```
poetry run python generate_key.py
poetry run python manage.py migrate
```

### Spuštění

Spusťte lokální server příkazem:

```
poetry run python manage.py runserver
```

a v prohlížeči otevřete stránku na adrese http://localhost:8000/.

### Testy

```
poetry run pytest
```

Pokud server na adrese http://localhost:8000/ běží, spustí se kromě jiných
testů také test webového rozhraní. Chcete-li sledovat průběh tohoto testu
v okně Firefoxu, spusťte testy s nastavenou proměnnou `NO_HEADLESS`:

```
NO_HEADLESS=1 poetry run pytest
```
