# Mikrus Interactive Console API

## Co to jest?
Projekt powstał w celu implementacji interaktywnej sesji z API mikrusa.
W przyszłości planuję dodać również możliwość aplikowania własnych dodatkowych modułów napisanych w pythonie w celu rozszerzenia możliwości aplikacji.

## Jak skorzystać?
1. Zainsaluj Python'a w wersji 3.
2. Pobierz to repozytorium
3. Wydaj polecenie: `pip install -r requirements.txt`
4. Skrypt już jest gotowy do odpalenia!
5. Uruchom skrypt za pomocą polecenia: `python ./app.py`

## Jak ustawić zmienne środowiskowe by nie musieć wpisywać za każdym razem klucza?
```bash
export MIKRUS_API=Klucz API z https://mikr.us/panel/?a=api
export MIKRUS_SRV=numer serwera
```


### Co na ten moment nie działa?
Wszystkie komendy, które powinny ustawiać dodatkowo jakieś wartości, jak chociażby /**logs/ID**.

### Masz pytania?
Pisz na DC: Hirrito.py#3072