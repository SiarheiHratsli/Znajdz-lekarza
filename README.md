# 🩺 Znajdź Lekarza

**Projekt zespołowy realizowany w ramach przedmiotu _Nowatorski projekt zespołowy_**

Aplikacja webowa pozwalająca pacjentom wyszukiwać lekarzy na podstawie specjalizacji, lokalizacji i dostępności, a także rezerwować wizyty, dodawać opinie oraz prowadzić rozmowy z lekarzami.

## 👥 Zespół

- **Siarhei Hratsli** – 48738
- **Rafał Dutkiewicz** – 48725
- **Mateusz Kłosowski** – 48744

## 🧩 Opis funkcjonalności

- Rejestracja i logowanie użytkownika
- Przeglądanie dostępnych lekarzy
- Wyszukiwanie i filtrowanie według specjalizacji
- Rezerwacja wizyt
- System opinii i ocen
- Profil użytkownika
- Resetowanie hasła przez e-mail
- Kontakt z administracją
- **Możliwość czatu z lekarzem – widoczny w formie dymka w prawym dolnym rogu strony**
- Stylizacja przy użyciu **Tailwind CSS**

## 🛠️ Technologie

| Warstwa     | Technologia         |
| ----------- | ------------------- |
| Backend     | Python (Flask)      |
| Frontend    | HTML + Tailwind CSS |
| Baza danych | SQLite              |
| Inne        | Docker, Jinja2      |

## 📁 Struktura projektu

```
Znajdz-lekarza/
├── app.py                  # Główny plik uruchomieniowy Flask
├── config.py               # Konfiguracja aplikacji
├── db/
│   ├── init                # Inicjalizacja bazy
│   └── models              # Modele ORM
├── templates/              # Szablony HTML (Jinja2)
├── static/                 # Pliki statyczne (obrazy, CSS)
├── requirements.txt        # Wymagane biblioteki
├── Dockerfile              # Obraz Dockera
├── docker-compose.yml      # Konfiguracja Dockera
└── README.md               # Dokumentacja projektu
```

## ⚙️ Instalacja lokalna

1. **Sklonuj repozytorium:**

   ```bash
   git clone https://github.com/SiarheiHratsli/Znajdz-lekarza.git
   cd Znajdz-lekarza
   ```

2. **Utwórz środowisko wirtualne i zainstaluj zależności:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate      # lub: .\venv\Scripts\activate (Windows)
   pip install -r requirements.txt
   ```

3. **Uruchom aplikację:**

   ```bash
   python app.py
   ```

   Aplikacja dostępna będzie pod adresem: [http://127.0.0.1:5000](http://127.0.0.1:5000)

## 🐳 Uruchomienie przez Docker

1. **Zbuduj i uruchom kontener:**

   ```bash
   docker-compose up --build
   ```

2. Otwórz w przeglądarce: [http://localhost:5000](http://localhost:5000)

## 🧪 Przykładowe widoki

- `main.html`: Strona główna
- `search.html`: Wyszukiwarka lekarzy
- `reserve.html`: Formularz rezerwacji wizyty
- `user_profile.html`: Panel użytkownika
- `add_review.html` / `edit_review.html`: Opinie
- `chat_widget.html`: Widżet czatu z lekarzem

## 💬 Czat z lekarzem

W prawym dolnym rogu strony znajduje się **dymek czatu**, który umożliwia użytkownikowi bezpośrednią konwersację z lekarzem.

## 🔐 System uwierzytelniania

- Logowanie / rejestracja
- Reset hasła za pomocą e-maila
- Walidacja użytkowników przy rezerwacjach

## 🧼 Stylizacja

Projekt wykorzystuje **Tailwind CSS** do szybkiego i responsywnego stylowania interfejsu.

## 🔄 Przyszłe usprawnienia

- Dodanie panelu administracyjnego
- Ulepszenie systemu ocen i rekomendacji
- Wsparcie dla wielu języków
