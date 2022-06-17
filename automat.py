import interface  # import modulu odpowiadajacego za interfejs
import logic  # import modulu odpowiadajacego za logike
import helpers  # import funkcji pomocniczych

if __name__ == '__main__':
    machine = logic.ItemStorage()  # utworzenie automatu przechowujacego przedmioty klasy Item

    # pobranie towarow z pliku i zaladowanie ich do automatu (jednolinijkowy odczyt pliku)
    for product in [line.strip() for line in open("towary.txt")]:
        name, number, price, count = product.split(',')
        machine.add_item(logic.Item(name, int(number), helpers.decimal_2places_rounded(price), int(count)), logic.Item)

    # utworzenie kontenerow na pieniadze umieszczane przez klienta oraz na pieniadze wydawane jako reszta
    machine_coins = logic.CoinStorage()
    machine_rest_coins = logic.CoinStorage()

    # dodanie poczatkowych srodkow do kontenera na wydawanie reszty - list comprehension
    [machine_rest_coins.add_multiple_coins(value, 1) for value in logic.possible_coins]

    # uruchomienie interfejsu graficznego
    display = interface.MachinePanel(machine, machine_coins, machine_rest_coins).create_view()
