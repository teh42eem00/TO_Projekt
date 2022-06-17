from decimal import *  # import decimal


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
