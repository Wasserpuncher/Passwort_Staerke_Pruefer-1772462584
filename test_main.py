```python
"""
Modul für Unit-Tests des Passwort-Stärke-Prüfers (main.py).
"""

import unittest
from main import pruefe_passwort_staerke, _berechne_passwort_punkte

class TestPasswortStaerkePruefer(unittest.TestCase):
    """
    Testklasse für die Funktionen des Passwort-Stärke-Prüfers.
    """

    def test_pruefe_passwort_staerke_sehr_schwach(self):
        """
        Testet die Funktion pruefe_passwort_staerke mit einem sehr schwachen Passwort.
        """
        staerke, punkte, empfehlungen = pruefe_passwort_staerke("kurz")
        self.assertEqual(staerke, "Sehr schwach")
        self.assertLessEqual(punkte, 20) # Punkte sollten im Bereich sehr schwach liegen
        self.assertIn("Machen Sie das Passwort länger", empfehlungen)
        self.assertIn("Fügen Sie Großbuchstaben hinzu", empfehlungen)

    def test_pruefe_passwort_staerke_schwach(self):
        """
        Testet die Funktion pruefe_passwort_staerke mit einem schwachen Passwort.
        """
        staerke, punkte, empfehlungen = pruefe_passwort_staerke("passwort123")
        self.assertEqual(staerke, "Schwach")
        self.assertGreater(punkte, 0)
        self.assertLessEqual(punkte, 40) # Punkte sollten im Bereich schwach liegen
        self.assertIn("Machen Sie das Passwort länger", empfehlungen)
        self.assertIn("Fügen Sie Großbuchstaben hinzu", empfehlungen)
        self.assertIn("Fügen Sie Sonderzeichen hinzu", empfehlungen)

    def test_pruefe_passwort_staerke_mittel(self):
        """
        Testet die Funktion pruefe_passwort_staerke mit einem mittelstarken Passwort.
        """
        staerke, punkte, empfehlungen = pruefe_passwort_staerke("MeinPasswort1!") # Länge 14
        self.assertEqual(staerke, "Mittel")
        self.assertGreater(punkte, 30) # Sollte deutlich mehr als schwach sein
        self.assertLessEqual(punkte, 60) # Punkte sollten im Bereich mittel liegen
        self.assertIn("Vermeiden Sie einfache, vorhersehbare Muster", empfehlungen) # Erwartung: generische Empfehlungen
        self.assertNotIn("Machen Sie das Passwort länger", empfehlungen) # Sollte lang genug sein

    def test_pruefe_passwort_staerke_gut(self):
        """
        Testet die Funktion pruefe_passwort_staerke mit einem guten Passwort.
        """
        staerke, punkte, empfehlungen = pruefe_passwort_staerke("SehrSicheresPasswort123$") # Länge 24
        self.assertEqual(staerke, "Gut")
        self.assertGreater(punkte, 60)
        self.assertLessEqual(punkte, 80) # Punkte sollten im Bereich gut liegen
        self.assertIn("Vermeiden Sie einfache, vorhersehbare Muster", empfehlungen) # Erwartung: generische Empfehlungen
        self.assertNotIn("Machen Sie das Passwort länger", empfehlungen) # Sollte lang genug sein

    def test_pruefe_passwort_staerke_sehr_gut(self):
        """
        Testet die Funktion pruefe_passwort_staerke mit einem sehr guten Passwort.
        """
        staerke, punkte, empfehlungen = pruefe_passwort_staerke("EinSehrKomplexesUndLangesPasswortMit123Sonderzeichen!!!")
        self.assertEqual(staerke, "Sehr gut")
        self.assertGreaterEqual(punkte, 80) # Punkte sollten im Bereich sehr gut liegen
        self.assertIn("Ausgezeichnet! Ihr Passwort ist sehr stark.", empfehlungen)
        self.assertEqual(len(empfehlungen), 1) # Nur die "Ausgezeichnet!" Nachricht

    def test_pruefe_passwort_staerke_leeres_passwort(self):
        """
        Testet die Funktion pruefe_passwort_staerke mit einem leeren Passwort.
        """
        staerke, punkte, empfehlungen = pruefe_passwort_staerke("")
        self.assertEqual(staerke, "Sehr schwach")
        self.assertEqual(punkte, 0)
        self.assertIn("Das Passwort ist leer. Bitte geben Sie ein Passwort ein.", empfehlungen)

    def test_pruefe_passwort_staerke_value_error(self):
        """
        Testet die Fehlerbehandlung für ungültige Eingabetypen.
        """
        with self.assertRaises(ValueError):
            pruefe_passwort_staerke(12345) # Keine Zeichenkette
        with self.assertRaises(ValueError):
            pruefe_passwort_staerke(None) # Keine Zeichenkette

    def test_berechne_passwort_punkte_laenge(self):
        """
        Testet die Punktberechnung basierend auf der Länge.
        """
        self.assertGreater(_berechne_passwort_punkte("a" * 12), _berechne_passwort_punkte("a" * 8))
        self.assertGreater(_berechne_passwort_punkte("a" * 8), _berechne_passwort_punkte("a" * 5))
        self.assertEqual(_berechne_passwort_punkte(""), 0)

    def test_berechne_passwort_punkte_kategorien(self):
        """
        Testet die Punktberechnung für verschiedene Zeichenkategorien.
        """
        # Nur Kleinbuchstaben
        punkte_klein = _berechne_passwort_punkte("abcdefgh")
        # Kleinbuchstaben und Großbuchstaben
        punkte_gross_klein = _berechne_passwort_punkte("Abcdefgh")
        self.assertGreater(punkte_gross_klein, punkte_klein)
        # Alle Kategorien
        punkte_alle = _berechne_passwort_punkte("Abcdefg1!")
        punkte_drei_kategorien = _berechne_passwort_punkte("Abcdefg1") # Keine Sonderzeichen
        self.assertGreater(punkte_alle, punkte_drei_kategorien)

    def test_berechne_passwort_punkte_abzuege(self):
        """
        Testet die Punktabzüge für einfache Muster.
        """
        # Sequenz
        punkte_normal = _berechne_passwort_punkte("passwortXYZ")
        punkte_sequenz = _berechne_passwort_punkte("passwort123")
        self.assertLess(punkte_sequenz, punkte_normal)

        # Wiederholte Zeichen
        punkte_normal_w = _berechne_passwort_punkte("passwortABC")
        punkte_wiederholung = _berechne_passwort_punkte("passwortAAA")
        self.assertLess(punkte_wiederholung, punkte_normal_w)

        # Negative Punkte vermeiden
        self.assertEqual(_berechne_passwort_punkte("abc"), 0) # Sehr kurzes, sequenzielles

if __name__ == "__main__":
    unittest.main()
```