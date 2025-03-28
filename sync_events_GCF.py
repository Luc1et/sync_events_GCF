
#  17. 03. 2025 Aktuální funkce pro zobrazení událostí na stránkách

from google.cloud import storage
import requests
import json
import unicodedata
import os
from datetime import datetime

# Funkce pro odstranění diakritiky
def normalize_text(text):
    return ''.join(
        c for c in unicodedata.normalize('NFD', text.lower()) if unicodedata.category(c) != 'Mn'
    )

# Funkce pro hledání zkráceného názvu
def find_short_name(city_name, bucket_name, json_file_name):
    """Hledání zkráceného názvu obce."""
    # Inicializace klienta Google Cloud Storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(json_file_name)

    # Načtení JSON souboru z bucketu
    content = blob.download_as_text(encoding="utf-8")
    obce = json.loads(content)

    # Normalizace vstupu
    city_name_norm = normalize_text(city_name)

    # Procházení prioritizovaných obcí
    for priority in [1, 2]:
        for obec in obce:
            if obec["region_priority"] == priority and normalize_text(obec["full_name"]) == city_name_norm:
                return obec["short_name"]

    return city_name  # Vrátí původní název místa

# Hlavní funkce pro zpracování
def main(request):
    try:
        # Nastavení
        API_KEY = os.environ.get("API_KEY")
        bucket_name = "fajraci-bucket"  # Nahraď názvem svého bucketu
        json_file_name = "obce_zl_jm.json"
        PHP_UPLOAD_URL = "https://fajraci.cz/upload.php"

        if not API_KEY:
            print("Chybí API_KEY!")
            return "Chyba: Chybí API klíč.", 500

        # Definuj API URL
        account_name = "FAJRaci"
        schedule_id = 703521
        API_URL = f"https://www.supersaas.cz/api/bookings.json?schedule_id={schedule_id}"


        # Načtení dat z API
        response = requests.get(API_URL, auth=(account_name, API_KEY))
        if response.status_code != 200:
            print(f"Chyba při načítání API: {response.status_code}")
            return f"Chyba při načítání API: {response.status_code}", 500

        data = response.json()
        
        # Zpracování událostí
        today = datetime.now().date()
        api_events = []

        for booking in data:
            start_date_str = booking.get("start", "").split("T")[0]
            try:
                start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            except ValueError:
                continue

            # Ověření stavu rezervace (B) - nový blok pro kontrolu stavu rezervace
            status_message = booking.get("status_message", "")  # (B) - načtení stavu rezervace
            if "Schválil" not in status_message:  # (B) - podmínka pro zpracování pouze schválených
                print(f"Rezervace není schválená, přeskočeno: {status_message}")  # (B) - logování
                continue  # (B) - přeskočí neschválené rezervace

            if start_date >= today:
                place = booking.get("field_1", "Neuvedeno")
                full_name = booking.get("field_2", "Bez názvu")

                # Zkrácení názvu místa
                short_name = find_short_name(place, bucket_name, json_file_name)

                # Přidání události
                api_events.append({
                    "date": start_date_str,
                    "place": short_name,  # Použij zkrácený název
                    "name": full_name,
                    "type": "FIRESHOW",
                })

        # Odeslání dat na PHP server
        json_data = json.dumps(api_events, indent=4, ensure_ascii=False)
        php_response = requests.post(
            PHP_UPLOAD_URL,
            data=json_data.encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )

        if php_response.status_code == 200:
            print("Data byla úspěšně nahrána!")
            return "Data byla úspěšně nahrána!", 200
        else:
            print(f"Chyba při nahrávání na PHP: {php_response.status_code}")
            return f"Chyba při nahrávání na PHP: {php_response.status_code}", 500

    except Exception as e:
        print(f"Chyba: {e}")
        return f"Chyba: {e}", 500

