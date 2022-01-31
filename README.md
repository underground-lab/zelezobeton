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
```

### Spuštění

```
poetry run streamlit run page.py
```

Stránka na adrese http://localhost:8501/ se automaticky otevře v prohlížeči.

### Testy

```
poetry run pytest
```

Pokud server na adrese http://localhost:8501/ běží, spustí se kromě
jiných testů také test webového rozhraní v novém okně Firefoxu.
