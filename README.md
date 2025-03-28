### 🌟 Zobrazení událostí na stránkách 🌟

---

#### 📝 Popis projektu

Tento projekt slouží k automatickému načítání a zobrazení událostí na webových stránkách. Události jsou získávány z API služby SuperSaaS, filtrovány podle schváleného stavu a odesílány na PHP server pro další zpracování a zobrazení.

Projekt byl vytvořen jako součást integrace online rezervačního systému do vlastního webu, aby bylo možné prezentovat nadcházející akce s minimalizovaným úsilím na ruční správu. Cílem bylo automatizovat sběr a přenos dat, přičemž je dbáno na bezpečnost přístupových údajů.

---

#### 💻 Funkce

1. **Načítání událostí z API** - Skript se připojí k API SuperSaaS a stáhne aktuální seznam událostí.
2. **Filtrování schválených rezervací** - Zpracovávají se pouze schválené rezervace, aby se předešlo zobrazení neschválených akcí.
3. **Zkrácení názvů míst** - Automatické zkrácení názvů míst pro přehlednější zobrazení na stránkách.
4. **Odeslání na PHP server** - Data jsou odeslána na server pro další zpracování a vizualizaci.

---

#### 🚀 Jak projekt spustit

1. Nastavte správně proměnné prostředí, zejména API klíč:

   ```
   export API_KEY=VasApiKlic
   ```

2. Spusťte aplikaci příkazem:

   ```
   python3 sync_events_GCF.py
   ```

3. Skript se připojí k API, stáhne události, provede zpracování a odeslání na PHP server.

---

#### 🛠️ Použité technologie

- **Python 3** - hlavní programovací jazyk
- **Google Cloud Functions** - nasazení funkce
- **Google Cloud Storage** - ukládání pomocných dat
- **SuperSaaS API** - načítání událostí
- **Requests** - knihovna pro HTTP požadavky
- **JSON** - formát dat pro přenos

---

#### 📂 Struktura projektu

```
.
├── sync_events_GCF.py   # Hlavní skript pro zpracování událostí
└── README.md                    # Dokumentace projektu
```

---

#### 💡 Možná vylepšení

- Zobrazení poslední proběhlé akce pro lepší přehled.
- Přidání více typů událostí a jejich kategorizace.
- Rozšíření o další datové zdroje (např. Google Calendar).
- Logování událostí pro účely monitoringu a ladění.

---

#### 📜 Licence

Tento projekt je licencován pod licencí MIT - podrobnosti naleznete v souboru LICENSE.

---

#### 🤝 Přispění a podpora

Pokud máte nápady na rozšíření nebo návrhy na vylepšení, neváhejte mě kontaktovat! 😊

🌟 **Automatizujte své události jednoduše a efektivně!** 🌟
