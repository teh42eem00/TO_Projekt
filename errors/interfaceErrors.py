# Wyjatki dla tego modulu
class PanelError(Exception):
    """Klasa bazowa dla zglaszanych w tym module wyjatkow"""
    pass


class TooLowMoneyAndNotOnStockError(PanelError):
    """Wyjatek wywolywany gdy brak produktu na stanie oraz wrzucona kwota byla za mala

    atrybuty:
    message_title - tytul wiadomosci zwracanej w okienku
    message_content - tresc wiadomosci zwracanej w okienku"""

    def __init__(self, message_title, message_content):
        self._message_title = message_title
        self._message_content = message_content

    def __str__(self):
        return self._message_title, self._message_content


class TooLowAmountOfMoneyError(PanelError):
    """Wyjatek wywolywany gdy zostalo wplaconych zbyt malo srodkow

    atrybuty:
    message_title - tytul wiadomosci zwracanej w okienku
    message_content - tresc wiadomosci zwracanej w okienku"""

    def __init__(self, message_title, message_content):
        self._message_title = message_title
        self._message_content = message_content

    def __str__(self):
        return self._message_title, self._message_content


class WrongProductNumberError(PanelError):
    """Wyjatek wywolywany gdy zostal wybrany bledny numer produktu

    atrybuty:
    message_title - tytul wiadomosci zwracanej w okienku
    message_content - tresc wiadomosci zwracanej w okienku"""

    def __init__(self, message_title, message_content):
        self._message_title = message_title
        self._message_content = message_content

    def __str__(self):
        return self._message_title, self._message_content
