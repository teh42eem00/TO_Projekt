from decimal import *  # import decimal
from errors import logicErrors

possible_coins = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]  # dozwolone nominaly


def decimal_2places_rounded(value_before):
    """Funkcja konwertujaca wprowadzona liczbe na Decimal zaokraglona do 2 miejsc po przecinku

    argumenty:
    value_before - wartosc przed zamiana"""
    value_before = Decimal(value_before)
    return round(value_before, 2)


def unpack_dict(value, count):
    """Funkcja rozpakowujaca slownik, zwracajaca dwie wartosci

    argumenty:
    value - pierwszy argument slownika - wartosc monet
    count - drugi argument slownika - ilosc monet danej wartosci"""
    # powrotna konwersja z groszy na zł
    return decimal_2places_rounded(value / 100), count


def return_change(coins, to_return, coin_index=0):
    """Metoda rekursywnie obliczajaca reszte do zwrotu korzystajac z zalaczonej listy przechowujacej slowniki zliczonych
    monet bedacych na stanie w automacie. W przypadku nieudanego poszukiwania (brak monet pozwalajacych wydac reszte) zwraca
    None.

    argumenty:
    coins - lista slownikow monet (w formacie {'value':value, 'count':count}
    to_return - kwota reszty do obliczenia/wyplacenia
    coin_index - index od ktorego rozpoczynamy poszukiwania w liscie, domyslnie 0
    """
    if to_return == 0:
        return []  # sukces gdy pozostalo 0 do zwrocenia
    if coin_index >= len(coins):
        return None  # nie udalo sie znalezc reszty
    coin = coins[coin_index]
    coin_index += 1
    # rozpoczynam od pobierania jak najwiekszej ilosci monet
    can_take = min(to_return // coin["value"], coin["count"])
    # pobieram monety az do osiagniecia kwoty 0
    for counter in range(can_take, -1, -1):  # odliczanie do 0
        # rekursywnie przechodze do kolejnych monet w celu dobrania odpowiednich kolejnych nominalow
        change = return_change(coins, to_return - coin["value"] * counter, coin_index)
        if change is not None:  # jezeli rekursywny przypadek nie zwrocil None
            if counter:  # i zostalo cos naliczone to dodaj do reszty
                return change + [{"value": coin["value"], "count": counter}]
            return change  # lub zwroc reszte


class Thing:
    """Klasa definiujaca przedmioty jak monety, towary"""
    pass


class Storage:
    """Klasa bedaca kontenerem na przedmioty takie jak monety, towary"""
    pass


class Coin(Thing):
    """Klasa definiujaca monete.

    argumenty:
    value - wartosc monety"""

    def __init__(self, value):
        # konwersja na decimal, 2 miejsca po przecinku
        self._value = decimal_2places_rounded(value)

    def get_value(self):
        """Metoda zwracajaca zaokraglona do dwoch miejsc po przecinku wartosc monety (typu Decimal)"""
        # pobranie wartosci decimal, 2 miejsca po przecinku
        return decimal_2places_rounded(self._value)


class CoinStorage(Storage):
    """Klasa przechowujaca monety. Monety sa przechowywane w liscie."""

    def __init__(self):
        # lista przechowujaca monety
        self._coin_list = []

    def add_coin(self, added_coin):
        """Metoda sluzaca do dodawania monet do kontenera. Przesylany obiekt musi byc klasy Moneta.

        argumenty:

        added_coin - obiekt klasy Moneta, ktory chcemy dodac do kontenera"""
        try:
            # jezeli moneta jest klasy Coin to dodaj, w przeciwnym wypadku wyjatek
            if isinstance(added_coin, Coin):
                self._coin_list.append(added_coin)
            else:
                raise logicErrors.InvalidObjectTypeError("Przeslany obiekt nie jest moneta! Jest on typu ",
                                                         type(added_coin))
        except logicErrors.InvalidObjectTypeError as inv_type:
            print(*inv_type.__str__())

    def add_multiple_coins(self, coin_value, coin_count):
        """Metoda sluzaca do hurtowego dodania wielu monet danego nominalu.

        argumenty:
        coin_value - nominal monety
        coin_count - liczba monet"""
        # dodaj okreslona ilosc monet o okreslonym nominale
        for ccount in range(coin_count):
            self._coin_list.append(Coin(coin_value))

    def get_coin_index(self, chosen_coin_value):
        """Metoda zwracajaca index pierwsej napotkanej monety o danej wartosci

        argumenty:
        chosen_coin_value - wartosc poszukiwanej monety"""
        # wyrazenie generujace zwracajace index pierwszej napotkanej monety o danej wartosci
        return next(i for i, coin in enumerate(self._coin_list) if coin.get_value() == chosen_coin_value)

    def return_array_of_value(self):
        """Metoda zwracajaca liste skladajaca sie tylko z wartosci wszystkich przechowywanych przez kontener monet"""
        # list comprehension zwracajace liste wartosci wszystkich monet
        value_list = [float(o.get_value()) for o in self._coin_list]
        return value_list

    def return_rest(self, rest_coin_value, rest_coin_count):
        """Metoda zwracajaca komunikat typu string zawierajacy informacje o zwracanych monetach. Jest ona wywolywana przez
        metode buy_item klasy ItemStorage skad potem trafia do interfejsu i jest wypisywana jako messagebox. Pobiera index
        zwracanej monety za pomoca metody get_coin_index i zwraca monety przez metode pop listy _coin_list.

        argumenty:
        rest_coin_value - wartosc monety do zwrocenia
        rest_coin_count - ilosc monet o danej wartosci do zwrocenia"""
        rest_coin_txt = ""
        # dla podanej ilosci sciaga z listy monety o okreslonym nominale i dodaje ich wartosc do zwracanego komunikatu
        for rcount in range(rest_coin_count):
            selected_coin_index = self.get_coin_index(rest_coin_value)
            rest_coin_txt += "Wydaje reszte o wartosci " + str(
                self._coin_list.pop(selected_coin_index).get_value()) + "zl.\n"
        return rest_coin_txt

    def return_coins(self):
        """Metoda zwracajaca wszystkie monety w danym kontenerze. Wywolywana w momencie klikniecia przez uzytkownika przerwij.
        Wykonuje pop do momentu oproznienia listy. Zwraca tekst z informacje o tym jakie monety zostaly zwrocone."""
        returned_coins_txt = ""
        # dopoki lista nie jest pusta sciaga z listy wszystkie monety i zwraca ich wartosc w komunikacie
        while len(self._coin_list):
            returned_coins_txt += "Zwracam monete o wartosci " + str(self.pop_coin_object().get_value()) + " zl.\n"
        return returned_coins_txt

    def pop_coin_object(self):
        """Metoda zdejmujaca z listy ostatnia monete, zwraca obiekt typu Moneta."""
        # zdejmij z listy ostatni obiekt
        return self._coin_list.pop()

    def return_len(self):
        """Metoda zwracajaca dlugosc listy przechowujacej monety."""
        # zwroc dlugosc listy przechowujacej monety
        return len(self._coin_list)

    def check_empty_coin_list(self):
        """Metoda zwracajaca typ bool (True/False). Zwraca true gdy lista jest pusta, false gdy lista nie jest pusta."""
        # jezeli lista monet jest pusta zwroc True, w przeciwnym wypadku false
        if not self._coin_list:
            return True
        else:
            return False

    def take_money_inside(self, customer_money):
        """"Metoda przejmujaca pieniadze z jednego kontenera do drugiego. Dopoki kontener z ktorego sa pobierane pieniadze
        nie jest pusty nastepuje pop() na kontenerze zrodlowy, ktory nastepnie jest umieszczany w kontenerze docelowym za
        pomoca append

        argumenty:
        customer_money - obiekt typu CoinStorage z ktorego maja zostac przeniesione wszystkie pieniadze"""
        # dopoki kontener z pieniedzmi klienta nie jest pusty pobieraj monety i dodawaj je do kontenera automatu
        while customer_money.return_len():
            self._coin_list.append(customer_money.pop_coin_object())

    def coin_sum(self):
        """Metoda, ktora za pomoca wyrazenia generujacego zwraca sume wartosci wszystkich monet w kontenerze. Uzywana
        min. do sprawdzania czy kwota wplacona przez uzytkownika jest poprawna lub do wypisywania wartosci wplaconych monet
         na wyswietlaczu."""
        # wyrazenie generujace zwracajace sume wartosci wszystkich monet
        return sum(c.get_value() for c in self._coin_list)


class Item(Thing):
    """Klasa definiujaca przedmioty sprzedawane w automacie.

    argumenty:
    name - nazwa towaru
    number - numer (kod towaru podawany w automacie przez uzytkownika)
    price - koszt zakupu towaru
    count - liczba sztuk danego towaru
    """

    def __init__(self, name, number, price, count):
        self._name = name
        self._number = number
        self._price = decimal_2places_rounded(price)
        self._count = count

    def get_name(self):
        """Metoda zwracajaca nazwe towaru"""
        return self._name

    def get_number(self):
        """Metoda zwracajaca numer towaru"""
        return self._number

    def get_price(self):
        """Metoda zwracajaca cene towaru (zaokraglona do 2 miejsc po przecinku, typ Decimal)"""
        return decimal_2places_rounded(self._price)

    def get_count(self):
        """Metoda zwracajaca ilosc towaru"""
        return self._count

    def lower_count(self):
        """Metoda zmniejszajaca ilosc towaru o 1 sztuke"""
        self._count -= 1

    def check_item_count(self):
        """Metoda sprawdzajaca czy ilosc towaru jest wieksza od 0. Zwraca wartosc True gdy towar jest na stanie, w przeciwnym
        wypadku zwraca False."""
        return self._count > 0


class ItemStorage(Storage):
    """Klasa przechowujaca przedmioty bedace na sprzedaz. Przedmioty przechowywane sa w liscie."""

    def __init__(self):
        self._item_list = []

    def add_item(self, added_item):
        """Metoda dodajaca przedmiot do listy.

        argumenty:
        added_item - obiekt typu Item dodawany do listy"""
        try:
            # jezeli przedmiot jest klasy Item to dodaj go do listy, w przeciwnym wypadku wyjatek
            if isinstance(added_item, Item):
                self._item_list.append(added_item)
            else:
                raise logicErrors.InvalidObjectTypeError("Przeslany obiekt nie jest przedmiotem! Jest on typu ",
                                                         type(added_item))
        except logicErrors.InvalidObjectTypeError as inv_type:
            print(*inv_type.__str__())

    def get_item(self, chosen_item_number):
        """Metoda przeszukujaca przedmioty za pomoca generator expression w celu znalezienia towaru o podanym numerze.
        Zwraca obiekt typu Item.

        argumenty:
        chosen_item_number - zadany numer produktu, ktorego poszukujemy"""
        # wyrazenie generujace, zwracajace pierwszy napotkany przedmiot o danym kodzie towaru
        return next(item for item in self._item_list if item.get_number() == chosen_item_number)

    def get_item_list(self):
        """Metoda zwracajaca liste towarow na sprzedaz"""
        output = ""
        for item in self._item_list:
            output += str(item.get_number()) + ". " + item.get_name() + " " + str(item.get_price()) + "PLN " + str(
                item.get_count()) + "szt\n"
        return output

    def get_item_price(self, chosen_item_number):
        """Metoda zwracajaca cene towaru o podanym numerze

        argumenty:
        chosen_item_number - numer produktu, ktorego cene chcemy poznac"""
        # zwroc cene towaru o wskazanym kodzie towaru
        item_obj = self.get_item(chosen_item_number)
        return item_obj.get_price()

    def return_item(self, chosen_item_number):
        """Metoda zwracajaca przedmiot, zmniejsza atrybut count (liczba sztuk) towaru klasy Item

        argumenty:
        chosen_item_number - numer produktu, ktorego ilosc chcemy zmniejszyc o 1"""
        # zmniejsz ilosc towaru
        self.get_item(chosen_item_number).lower_count()

    def buy_item(self, chosen_item_number, money_placed, machine_rest_coins, machine_coins):
        """Metoda odpowiedzialna za zakup towaru z kontenera ItemStorage. Sa przeprowadzane tutaj wszelakie testy sprawdzajace
        warunki zakupu takie jak czy towar jest na stanie, czy jest do wydania reszta, czy maszyna posiada na stanie wystarczajaca
        ilosc monet aby wydac reszte. Metoda zwraca komunikaty posredniczy w przekazaniu komunikatow do interfejsu w celu
        wypisania informacji o zakupach/reszcie/braku towaru w messagebox.

        argumenty:
        chosen_item_number - numer produktu, ktory chcemy kupic
        money_placed - kwota wplacona przez uzytkownika
        machine_rest_coins - obiekt typu CoinStorage przechowujacy pieniadze do wydawania reszty
        machine_coins - obiekty typu CoinStorage przechowujacy wplacone przez klienta pieniadze"""
        try:
            # sprawdzenie stanu danego towaru
            selected_item_count = self.get_item(chosen_item_number).check_item_count()
            # jezeli towar na stanie
            if selected_item_count:
                # pobierz cene
                selected_item_price = self.get_item_price(chosen_item_number)
                # oblicz reszte
                rest = money_placed - selected_item_price
                if rest == 0:
                    # jezeli brak reszty zabierz pieniadze od klienta i wydaj towar
                    machine_rest_coins.take_money_inside(machine_coins)
                    self.return_item(chosen_item_number)
                    # zwrot komunikatu do messageboxa
                    return "Sukces", "Zakup produktu o numerze " + str(chosen_item_number) + " udany"
                else:
                    # list comprehension - lista dostepnych monet do wydania reszty, zmiana na grosze, sortowanie
                    rest_available_coins = sorted([int(i * 100) for i in machine_rest_coins.return_array_of_value()],
                                                  reverse=True)
                    counted_rest_coins = {}  # slownik przechowujacy monety w formie {wartosc , ilosc}
                    counted_rest_coins_list = list()  # lista przechowujaca slowniki zliczonych monet

                    for r in rest_available_coins:  # zliczenie ilosci monet dostepnych do wydania reszty
                        counted_rest_coins[r] = counted_rest_coins.get(r, 0) + 1

                    for key, (d_value, d_count) in enumerate(counted_rest_coins.items()):  # dodanie slownikow do listy
                        d = {"value": d_value, "count": d_count}
                        counted_rest_coins_list.append(d)

                    returned_change_dict_list = return_change(counted_rest_coins_list, int(rest * 100))  # licz reszte
                    if returned_change_dict_list is None:  # jezeli nie udalo sie obliczyc reszty zglos wyjatek
                        raise logicErrors.NoChangeAvailableError("Brak reszty!", "Tylko odliczona kwota!\n")
                    else:  # w przeciwnym razie pobierz pieniadze i wydaj reszte
                        change_txt = ""
                        for rc in returned_change_dict_list:  # dla wszystkich slownikow reszty (nominal, ilosc)
                            # zwroc reszte z rozpakowanego slownika
                            change_txt += machine_rest_coins.return_rest(*unpack_dict(**rc))
                        # zabranie pieniedzy od klienta i umieszczenie w kontenerze na wydawanie reszty
                        machine_rest_coins.take_money_inside(machine_coins)
                        # wydanie przedmiotu, zabranie jednej sztuki
                        self.return_item(chosen_item_number)
                        # zwrot komunikatu do messageboxa
                        return "Sukces", ("Zakup produktu o numerze " + str(chosen_item_number) +
                                          " udany\n" + str(change_txt))
            else:
                raise logicErrors.NoProductOnStockError("Brak towaru", "Brak towaru w automacie")
            # obsluga wyjatkow
        except logicErrors.NoChangeAvailableError as no_change:
            return no_change.message_title, no_change.message_content
        except logicErrors.NoProductOnStockError as no_product:
            return no_product.message_title, no_product.message_content
