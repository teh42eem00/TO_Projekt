import unittest
import logic  # import modulu odpowiadajacego za logike
import helpers  # import funkcji pomocniczych

# inicjalizacja srodowiska testowego
test_machine = logic.ItemStorage()  # utworzenie automatu przechowujacego przedmioty klasy Item

# pobranie towarow z pliku i zaladowanie ich do automatu (jednolinijkowy odczyt pliku)
for product in [line.strip() for line in open("towary.txt")]:
    name, number, price, count = product.split(',')
    test_machine.add_item(logic.Item(name, int(number), helpers.decimal_2places_rounded(price), int(count)), logic.Item)

# utworzenie kontenerow na pieniadze umieszczane przez klienta oraz na pieniadze wydawane jako reszta
machine_coins = logic.CoinStorage()
machine_rest_coins = logic.CoinStorage()

# dodanie poczatkowych srodkow do kontenera na wydawanie reszty - list comprehension
[machine_rest_coins.add_multiple_coins(value, 1) for value in logic.possible_coins]


class TestDrinkMachine(unittest.TestCase):
    """Klasa testowa unittest"""

    def test_price(self):
        """Test 1. Sprawdzenie ceny jednego towaru - oczekiwana informacja o cenie."""
        # wybranie towaru zwraca text do okienka ale posrednio wykonuje funkcje get item price
        product_number = 30
        self.assertEqual(test_machine.get_item_price(product_number), 3)

    def test_buy_with_equal_money(self):
        """Test 2. Wrzucenie odliczonej kwoty, zakup towaru - oczekiwany brak reszty"""
        # zakup za odliczona kwote zwraca tylko komunikat o udanym zakupie
        self.assertEqual(test_machine.buy_item(30, 3, machine_rest_coins, machine_coins),
                         ('Sukces', 'Zakup produktu o numerze 30 udany'))

    def test_buy_with_change(self):
        """Test 3. Wrzucenie wiekszej kwoty, zakup towaru - oczekiwana reszta"""
        # zakup za wieksza kwote zwraca komunikat o udanym zakupie i zwroconej reszcie
        self.assertEqual(
            test_machine.buy_item(30, helpers.decimal_2places_rounded(4.5), machine_rest_coins, machine_coins),
            ('Sukces',
             'Zakup produktu o numerze 30 udany\n'
             'Wydaje reszte o wartosci 0.50zl.\n'
             'Wydaje reszte o wartosci 1.00zl.\n'))

    def test_buy_when_out_of_stock(self):
        """Test 4. Wykupienie calego asortymentu, proba zakupu po wyczerpaniu towaru - oczekiwana informacja o braku."""
        # czterokrotny zakup + 1 sztuka zabrana powyzej
        for _ in range(5):
            test_machine.buy_item(50, 2, machine_rest_coins, machine_coins)
        # proba zakupu po wyczerpaniu towaru
        self.assertEqual(test_machine.buy_item(50, 2, machine_rest_coins, machine_coins),
                         ('Brak towaru', 'Brak towaru w automacie'))

    def test_wrong_choice(self):
        """Test 5. Sprawdzenie ceny towaru o nieprawidlowym numerze (<30 lub >50) - oczekiwana informacja o bledzie."""
        choice = 20
        # sprawdzenie odbywa sie w metodzie interfejsu graficznego i ciezko to wywolac w tescie
        # odbywa sie ono poprzez (if 50 >= choice >= 30)
        self.assertFalse(50 >= choice >= 30)

    def test_money_return(self):
        """Test 6. Wrzucenie kilku monet, przerwanie transakcji - oczekiwany zwrot monet."""
        text = "Zwracam monete o wartosci 5.00 zl.\nZwracam monete o wartosci 5.00 zl.\nZwracam monete o wartosci 5.00 zl.\nZwracam monete o wartosci 5.00 zl.\nZwracam monete o wartosci 5.00 zl.\n"
        # dodaje 5 monet 5 zl
        machine_coins.add_multiple_coins(5, 5)
        # sprawdzam zwrotny komunikat
        self.assertEqual(machine_coins.return_coins(), text)

    def test_low_money_and_insert(self):
        """Test 7. Wrzucenie za malej kwoty, wybranie poprawnego numeru towaru, wrzucenie reszty monet do odliczonej kwoty
        ponowne wybranie poprawnego numeru towaru- oczekiwany brak reszty."""
        # ten test odbywa sie po stronie interfejsu i ciezko go wywolac w tescie
        # wrzucenie za malej kwoty
        choice = 30
        machine_coins.add_item(logic.Coin(2), logic.Coin)
        # sprawdzanie w interfejsie odbywa sie za pomoca machine_coins.coin_sum() < machine.get_item_price(choice)
        # kwota nie przejdzie tego zarunku wiec interfejs nie wpusci do zakupu za pomoca metody machine.buy_item
        self.assertTrue(machine_coins.coin_sum() < test_machine.get_item_price(choice))
        # wrzucenie brakujacej kwoty
        machine_coins.add_item(logic.Coin(1), logic.Coin)
        # po wrzuceniu brakujacej kwoty interfejs pozwoli na zakup
        self.assertFalse(machine_coins.coin_sum() < test_machine.get_item_price(choice))
        # i zakup sie powiedzie
        self.assertEqual(test_machine.buy_item(30, machine_coins.coin_sum(), machine_rest_coins, machine_coins),
                         ('Sukces', 'Zakup produktu o numerze 30 udany'))

    def test_buy_with_low_value_coins(self):
        """Test 8. Zakup towaru placac po 1 gr- suma stu monet ma byc rowna 1 zl (dla floatow suma sto razy 0.01 + 0.01 +
        ...+0.01 nie bedzie rowna 1.0). Platnoscia mozna dokonac za pomoca petli w interpreterze."""
        # zwrocenie wszystkich dotychczas przechowywanych monet
        machine_coins.add_multiple_coins(0.01, 100)
        # proba zakupu przy pomocy wplaconych srodkow
        self.assertEqual(test_machine.buy_item(47, machine_coins.coin_sum(), machine_rest_coins, machine_coins),
                         ('Sukces', 'Zakup produktu o numerze 47 udany'))


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDrinkMachine)
    testResult = unittest.TextTestRunner(verbosity=2).run(suite)
