ைகளைக்```python
"""
Modul für einen professionellen Passwort-Stärke-Prüfer.

Dieses Modul bietet Funktionen zur Bewertung der Sicherheit eines Passworts
basierend auf verschiedenen Kriterien wie Länge, Verwendung von Groß- und Kleinbuchstaben,
Zahlen und Sonderzeichen.
"""

import re

def _berechne_passwort_punkte(passwort: str) -> int:
    """
    Berechnet einen Punktwert für die Stärke des Passworts.

    Args:
        passwort (str): Das zu bewertende Passwort.

    Returns:
        int: Der berechnete Punktwert.

    Raises:
        ValueError: Wenn das Passwort leer oder kein String ist.
    """
    if not isinstance(passwort, str):
        raise ValueError("Passwort muss ein String sein.")
    if not passwort:
        return 0 # Ein leeres Passwort hat 0 Punkte

    punkte = 0
    laenge = len(passwort)

    # 1. Länge des Passworts
    if laenge >= 12:
        punkte += 25
    elif laenge >= 8:
        punkte += 15
    elif laenge >= 6:
        punkte += 5

    # 2. Verwendung von Großbuchstaben
    if re.search(r"[A-Z]", passwort):
        punkte += 10

    # 3. Verwendung von Kleinbuchstaben
    if re.search(r"[a-z]", passwort):
        punkte += 10

    # 4. Verwendung von Zahlen
    if re.search(r"[0-9]", passwort):
        punkte += 10

    # 5. Verwendung von Sonderzeichen
    if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?~`"]", passwort):
        punkte += 15

    # 6. Bonus für Vielfalt (Kombinationen)
    kriterien_erfuellt = 0
    if re.search(r"[A-Z]", passwort): kriterien_erfuellt += 1
    if re.search(r"[a-z]", passwort): kriterien_erfuellt += 1
    if re.search(r"[0-9]", passwort): kriterien_erfuellt += 1
    if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?~`"]", passwort): kriterien_erfuellt += 1

    if kriterien_erfuellt >= 4:
        punkte += 20
    elif kriterien_erfuellt == 3:
        punkte += 10
    elif kriterien_erfuellt == 2:
        punkte += 5

    # 7. Abzüge für einfache Muster (vereinfacht, da keine Wortliste)
    # Sequentielle Zahlen/Buchstaben
    for i in range(len(passwort) - 2):
        char1 = passwort[i]
        char2 = passwort[i+1]
        char3 = passwort[i+2]
        if (ord(char2) == ord(char1) + 1 and ord(char3) == ord(char2) + 1) or \
           (ord(char2) == ord(char1) - 1 and ord(char3) == ord(char2) - 1):
            punkte -= 10
            break # Nur einmal abziehen

    # Wiederholte Zeichen (z.B. "aaa")
    if re.search(r"(.)\1\1", passwort):
        punkte -= 10

    # Sicherstellen, dass die Punkte nicht negativ werden
    return max(0, punkte)


def pruefe_passwort_staerke(passwort: str) -> tuple[str, int, list[str]]:
    """
    Bewertet die Stärke eines Passworts und gibt eine Bewertung,
    den Punktwert und Empfehlungen zurück.

    Args:
        passwort (str): Das zu bewertende Passwort.

    Returns:
        tuple[str, int, list[str]]: Ein Tupel bestehend aus:
            - str: Die Stärkeeinstufung ("Sehr schwach", "Schwach", "Mittel", "Gut", "Sehr gut").
            - int: Der numerische Punktwert.
            - list[str]: Eine Liste von Empfehlungen zur Verbesserung.

    Raises:
        ValueError: Wenn das Passwort leer oder kein String ist.
    """
    if not isinstance(passwort, str):
        raise ValueError("Passwort muss ein String sein.")
    if not passwort:
        return "Sehr schwach", 0, ["Das Passwort ist leer. Bitte geben Sie ein Passwort ein."]

    punkte = _berechne_passwort_punkte(passwort)
    empfehlungen = []

    # Bestimme die Stärkeeinstufung
    if punkte >= 80:
        staerke = "Sehr gut"
    elif punkte >= 60:
        staerke = "Gut"
    elif punkte >= 40:
        staerke = "Mittel"
    elif punkte >= 20:
        staerke = "Schwach"
    else:
        staerke = "Sehr schwach"

    # Sammle Empfehlungen
    laenge = len(passwort)
    if laenge < 12:
        empfehlungen.append(f"Machen Sie das Passwort länger (mindestens 12 Zeichen, aktuell {laenge}).")
    if not re.search(r"[A-Z]", passwort):
        empfehlungen.append("Fügen Sie Großbuchstaben hinzu.")
    if not re.search(r"[a-z]", passwort):
        empfehlungen.append("Fügen Sie Kleinbuchstaben hinzu.")
    if not re.search(r"[0-9]", passwort):
        empfehlungen.append("Fügen Sie Zahlen hinzu.")
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?~`"]", passwort):
        empfehlungen.append("Fügen Sie Sonderzeichen hinzu.")

    # Weitere generische Empfehlungen, falls das Passwort nicht "Sehr gut" ist und keine spezifischen Empfehlungen mehr nötig
    if staerke != "Sehr gut" and not empfehlungen:
        empfehlungen.append("Vermeiden Sie einfache, vorhersehbare Muster oder persönliche Informationen.")
        empfehlungen.append("Nutzen Sie eine Kombination aus verschiedenen Zeichentypen.")
        empfehlungen.append("Denken Sie über die Verwendung einer Passphrase nach.")

    if not empfehlungen: # Wenn bereits sehr gut und keine spezifischen Empfehlungen mehr nötig (und die obige Bedingung nicht zutraf)
        empfehlungen.append("Ausgezeichnet! Ihr Passwort ist sehr stark.")

    return staerke, punkte, empfehlungen

def main():
    """
    Hauptfunktion des Passwort-Stärke-Prüfers.
    Fordert den Benutzer zur Eingabe eines Passworts auf und zeigt die Stärke an.
    """
    print("--------------------------------------------------")
    print("         Willkommen zum Passwort-Stärke-Prüfer    ")
    print("--------------------------------------------------")
    print("Geben Sie 'beenden' ein, um das Programm jederzeit zu verlassen.")
    print("")

    while True:
        try:
            benutzer_passwort = input("Bitte geben Sie ein Passwort zur Überprüfung ein: ")

            if benutzer_passwort.lower() == "beenden":
                print("Vielen Dank für die Nutzung des Passwort-Stärke-Prüfers. Auf Wiedersehen!")
                break

            staerke, punkte, empfehlungen = pruefe_passwort_staerke(benutzer_passwort)

            print("\n--- Ergebnis der Passwortprüfung ---")
            # Aus Sicherheitsgründen nicht das Passwort selbst ausgeben
            print(f"Passwort: {'*' * len(benutzer_passwort)}") 
            print(f"Stärke: {staerke} (Punkte: {punkte})")
            print("\nEmpfehlungen zur Verbesserung:")
            if empfehlungen:
                for i, empf in enumerate(empfehlungen, 1):
                    print(f"  {i}. {empf}")
            else:
                print("  Keine spezifischen Empfehlungen. Ihr Passwort ist bereits sehr gut!")
            print("--------------------------------------------------\n")

        except ValueError as e:
            print(f"\nFehler bei der Eingabe: {e}. Bitte versuchen Sie es erneut.\n")
        except Exception as e:
            print(f"\nEin unerwarteter Fehler ist aufgetreten: {e}. Bitte kontaktieren Sie den Support.\n")

if __name__ == "__main__":
    main()
```