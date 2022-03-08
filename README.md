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

```
git clone https://github.com/underground-lab/zelezobeton.git
cd zelezobeton
poetry install
poetry run python manage.py migrate
```

### Spuštění

```
poetry run python manage.py runserver
```

V prohlížeči otevřete stránku na adrese http://localhost:8000/.

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
