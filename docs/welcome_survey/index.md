# 📋 Welcome Survey – Dashboard ankietowy

**Autor:** Roman – *Aspiring Data Scientist & Python Streamlit Developer*

Interaktywny dashboard do eksploracji wyników ankiety – notatnik w sidebarze, losowa próbka danych, wartości unikatowe oraz wizualizacje (korelacje, boxploty, barploty).

## Materiały dla rekrutera

[📥 Pobierz Notebook](research.ipynb){ .md-button .md-button--primary }
[🧪 Uruchom aplikację lokalnie](#uruchomienie-aplikacji-lokalnie){ .md-button }

---

## 🧠 Opis projektu

Aplikacja umożliwia analizę wyników ankiety bez kodowania:
- ✍️ dodawanie notatek (zapis do pliku),
- 🔄 losowe próbki danych,
- 🔼 sortowanie kolumn,
- 🔢 analiza wartości unikatowych,
- 📊 wizualizacje: korelacje, boxploty, barploty.

---

## 🧪 Uruchomienie aplikacji lokalnie

```bash
# 1. przejdź do folderu z aplikacją
cd docs/welcome_survey/app

# 2. zainstaluj zależności
pip install -r requirements.txt

# 3. uruchom aplikację
streamlit run app.py
