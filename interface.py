from tkinter import *  # import biblioteki odpowiedzialnej za rysowanie interfejsu
from tkinter import ttk, messagebox  # import biblioteki odpowiedzialnej za rysowanie interfejsu
from errors import interfaceErrors  # import obslugi wyjatkow
import logic  # import modulu odpowiadajacego za logike


class MachinePanel:
    """Klasa odpowiedzialna za interfejs uzytkownika. Przyjmuje jako argumenty kontener na przedmioty, kontener na
     monety klienty oraz kontener na monety do wydawania reszty. Ponadto w klasie tej odbywa sie konfiguracja
     interfejsu graficznego, przyciskow i akcji wykonywanych podczas ich naciskania.

     argumenty:
     machine_items - kontener (klasy ItemStorage) na przedmioty - napoje (klasy Item)
     machine_coins_input - kontener (klasy CoinStorage) na monety (klasy Coin) uzytkownika
     machine_coins_change - kontener (klasy CoinStorage) na monety (klasy Coin) do wydawania reszty
     """

    def __init__(self, machine_items, machine_coins_input, machine_coins_change):
        # obiekty przechowujace przedmioty i pieniadze
        self._machine_items = machine_items
        self._machine_coins_input = machine_coins_input
        self._machine_coins_change = machine_coins_change

        # Tworzenie okna
        self._window = Tk()
        self._window.title("Automat")

        # Zmienne przechowujace wyswietlana kwote i kod towaru
        self._money_amount = StringVar()
        self._item_choice = StringVar()
        self._buyers_choice = ""

        # Tworzenie siatki na przyciski
        self._mainframe = ttk.Frame(self._window)
        # Licznik przyciskow
        self._coin_row = 0

    def create_view(self):
        # Umieszczenie siatki w oknie
        self._mainframe.grid(column=0, row=0)

        # Dodanie przycisków do wrzucania monet
        for coin in logic.possible_coins:
            # lambda
            ttk.Button(self._mainframe, text="Wrzuć " + str(coin) + "zł",
                       command=lambda lcoin=coin: self.action_on_money(lcoin)).grid(column=4, row=self._coin_row)
            self._coin_row += 1

        # Dodanie przyciskow do wybierania towaru
        # lambda
        [ttk.Button(self._mainframe, text=str(digit + 1),
                    command=lambda ldigit=digit: self.action_on_choice(ldigit + 1)).grid(row=digit // 3 + 2,
                                                                                         column=digit % 3) for digit in
         range(9)]
        # lambda
        ttk.Button(self._mainframe, text="0", command=lambda: self.action_on_choice(0)).grid(row=5, column=1)

        # Dodanie przycisku przerwania transakcji, zwraca wplacone monety
        ttk.Button(self._mainframe, text="Zwrot",
                   command=lambda: self.action_on_cancel()).grid(column=0, row=5)  # lambda

        # Przyciski wypisujace w konsoli monety wplacone przez uzytkownika i te dostepne do wydawania reszty
        # lambda
        ttk.Button(self._mainframe, text="Monety - Reszta",
                   command=lambda: print(self._machine_coins_change.return_array_of_value())).grid(column=0, row=6)
        # lambda
        ttk.Button(self._mainframe, text="Monety - Wplacone",
                   command=lambda: print(self._machine_coins_input.return_array_of_value())).grid(column=0, row=7)
        # lambda
        # Dodanie przycisku cennika, wypisuje produkty, ich numery, ceny i stan sztuk w automacie
        ttk.Button(self._mainframe, text="Cennik",
                   command=lambda: messagebox.showinfo("Cennik", self._machine_items.get_item_list())).grid(column=0,
                                                                                                            row=8)

        # Wyswietlanie zawartosci zmiennych money_amount i item_choice jako Label
        ttk.Label(self._mainframe, textvariable=self._money_amount).grid(column=0, row=0)
        ttk.Label(self._mainframe, textvariable=self._item_choice).grid(column=0, row=1)

        # Glowna petla
        self._window.mainloop()

    def quit(self):
        """Metoda zamykajaca okno"""
        self._window.destroy()

    def action_on_choice(self, choice):
        """Metoda wykonywana w momencie wyboru numeru towaru. Gdy wybor mial dlugosc 0 lub 2 to ustawiamy dany kod towaru
        od nowa. Kod jest zmieniany na string i sklejany z dwoch fragmentow. W momencie gdy po kliknieciu wybor mial jeden
        znak, zostaje doklejony drugi i nastepuje przejscie do etapu weryfikacji kod towaru i ewentualnego zakupu. W metodzie
        tej sprawdzane sa rowniez warunki czy kod towaru miesci sie w danym zakresie, czy towar jest na stanie (jezeli nie
        bylo wplaconej wystarczajacej kwoty). W przypadku udanego zakupu zeruje wartosc wyswietlacza i przejmuje zwracane
        wartosci od metody buy_item (z klasy ItemStorage) i wypisuje je w messagebox.

         argumenty:
         choice - wybor kodu towaru podawany przez uzytkownika poprzez nacisniecie kolejno przyciskow (po jednym znaku)"""
        try:
            # jezeli dlugosc wyboru kupujacego jest rowna 0 lub 2 to zacznij zlaczanie stringa wejsciowego od nowa
            if len(self._buyers_choice) == 0 or len(self._buyers_choice) == 2:
                self._buyers_choice = str(choice)
                self._item_choice.set(self._buyers_choice)

            # jezeli jest rowna jeden zlacz string aby uzyskac dwucyfrowy kod towaru i przejdz do zakupu
            elif len(self._buyers_choice) == 1:
                self._buyers_choice += str(choice)
                self._item_choice.set(self._buyers_choice)
                choice = int(self._buyers_choice)
                # sprawdz czy towar miesci sie w dopuszczalnym zakresie
                if 50 >= choice >= 30:
                    # sprawdz czy wplacona kwota jest wystarczajaca i czy towar jest na stanie, jezeli nie to wyjatek
                    if (self._machine_coins_input.coin_sum() < self._machine_items.get_item_price(
                            choice) and not (self._machine_items.get_item(choice).check_item_count())):
                        raise interfaceErrors.TooLowMoneyAndNotOnStockError("Za mało!", "Produkt " +
                                                                            self._machine_items.get_item(
                                                                                choice).get_name() + " kosztuje " +
                                                                            str(self._machine_items.get_item_price(
                                                                                choice)) +
                                                                            "\nNiestety w tym momencie brak tego towaru!")
                    # sprawdz czy kwota jest wystarczajaca, jezeli nie to wyjatek
                    elif self._machine_coins_input.coin_sum() < self._machine_items.get_item_price(choice):
                        raise interfaceErrors.TooLowAmountOfMoneyError("Za mało!", "Produkt " +
                                                                       self._machine_items.get_item(
                                                                           choice).get_name() + " kosztuje " +
                                                                       str(self._machine_items.get_item_price(choice)))
                    # w przeciwnym wypadku przejdz do procedury zakupu
                    else:
                        buy_status, buy_message = (
                            self._machine_items.buy_item(choice, self._machine_coins_input.coin_sum(),
                                                         self._machine_coins_change, self._machine_coins_input))
                        messagebox.showinfo(buy_status, buy_message)
                        if self._machine_coins_input.check_empty_coin_list():
                            self._money_amount.set("")
                            self._item_choice.set("")
                # gdy kod towaru bledny zwroc wyjatek
                else:
                    raise interfaceErrors.WrongProductNumberError("Blad", "Bledny numer produktu!")
        # obsluga wyjatkow
        except interfaceErrors.TooLowMoneyAndNotOnStockError as not_on_stock:
            messagebox.showinfo(*not_on_stock.__str__())
        except interfaceErrors.TooLowAmountOfMoneyError as money_too_low:
            messagebox.showinfo(*money_too_low.__str__())
        except interfaceErrors.WrongProductNumberError as wrong_number:
            messagebox.showinfo(*wrong_number.__str__())

    def action_on_money(self, money):
        """Metoda wykonywana w momencie dodawania przez uzytkownika pieniedzy (poprzez klikanie w dane nominaly na panelu).
        Pieniadze trafiaja do kontenera przeznaczonego na wplaty uzytkownika. W tej metodzie zostaje takze ustawiana
        wartosc wplaconych pieniedzy wyswietlana na ekranie (suma monet w kontenerze).

        argumenty:
        money - nominal wybrany przez uzytkownika na panelu, zostaje utworzony obiekt klasy Coin o takim nominale i
        trafia do kontenera na monety."""
        # dodanie monety o kliknietej wartosci
        self._machine_coins_input.add_item(logic.Coin(money), logic.Coin)
        # ustawienie sumy wplaconych monet na wyswietlaczu
        self._money_amount.set(str(self._machine_coins_input.coin_sum()))

    def action_on_cancel(self):
        """Metoda wykonywana w momencie klikniecia przez uzytkownika PRZERWIJ. Wypisuje ona komunikat z informacja o zwrocie
        monet (dane wypisywane sa zwraca z funkcji return_coins (z klasy CoinStorage). Po zwrocie monet nastepuje wyczyszczenie
        wyswietlacza z wartoscia wplaconych monet."""
        # zwrocenie monet klientowi i wypisanie ich w messageboxie
        messagebox.showinfo("Zwrot monet", self._machine_coins_input.return_coins())
        # ustawienie wyswietlacza wplaconej kwoty na pusty
        self._money_amount.set("")
