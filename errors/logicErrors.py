# Wyjatki dla tego modulu
class LogicError(Exception):
    """Klasa bazowa dla zglaszanych w tym module wyjatkow"""
    pass


class NoChangeAvailableError(LogicError):
    """Wyjatek wywolywany gdy brak pieniedzy do wydania reszty

    atrybuty:
    message_title - tytul wiadomosci zwracanej w okienku
    message_content - tresc wiadomosci zwracanej w okienku"""

    def __init__(self, message_title, message_content):
        self.message_title = message_title
        self.message_content = message_content

    def __str__(self):
        return self.message_title, self.message_content


class NoProductOnStockError(LogicError):
    """Wyjatek wywolywany gdy brak towaru (rozni sie od tego z interfejsu, ze jest wywolywany gdy klient juz wrzucil
    odpowiednia kwote i automat rozpoczal proces zakupu)

    atrybuty:
    message_title - tytul wiadomosci zwracanej w okienku
    message_content - tresc wiadomosci zwracanej w okienku"""

    def __init__(self, message_title, message_content):
        self.message_title = message_title
        self.message_content = message_content

    def __str__(self):
        return self.message_title, self.message_content


class InvalidObjectTypeError(LogicError):
    """Wyjatek wywolywany gdy przedmiot umieszczany w kontenerze ma nieprawidlowy typ (np. w przypadku kontenerow
    ItemStorage, CoinStorage oczekiwane sa klasy Item, Coin

    atrybuty:
    message_title - tytul wiadomosci zwracanej w okienku
    message_content - tresc wiadomosci zwracanej w okienku"""

    def __init__(self, message, object_type):
        self._message = message
        self._object_type = object_type

    def __str__(self):
        return self._message, self._object_type
