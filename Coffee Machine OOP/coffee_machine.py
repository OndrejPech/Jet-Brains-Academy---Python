class CoffeeMachine:
    all_text = dict(start="Starting to make a coffee",
                    grinding="Grinding coffee beans", boiling="Boiling water",
                    mixing="Mixing boiled water with crushed coffee beans",
                    pouring_coffe="Pouring coffee into the cup",
                    pourin_milk="Pouring some milk into the cup",
                    coffe_ready="Coffee is ready!")

    def __init__(self, water, milk, beans, cups, money):
        self.water = water  # ml
        self.milk = milk  # ml
        self.beans = beans  # g
        self.cups = cups
        self.money = money  # dollars

    def show_info(self):
        """print info of amount of each supply"""
        print("The coffee machine has:")
        print(f"{self.water} ml of water")
        print(f"{self.milk} ml of milk")
        print(f"{self.beans} g of coffee beans")
        print(f"{self.cups} disposable cups")
        print(f"${self.money} of money")

    def supplies_missing(self, drink_type):
        """return list with names of missing supplies"""
        missing = []
        if drink_type.water > self.water:
            missing.append('water')
        if drink_type.milk > self.milk:
            missing.append('milk')
        if drink_type.beans > self.beans:
            missing.append('beans')
        if drink_type.cups > self.cups:
            missing.append('cups')

        return missing

    def take(self):
        """withdraw all money from machine"""
        print(f'I gave you ${self.money}')
        self.money = 0

    def fill(self):
        """ask user how much of each supply he wants to add to machine"""
        water_tba = get_num("Write how many ml of water you want to add:")
        self.water += water_tba
        milk_tba = get_num("Write how many ml of milk you want to add:")
        self.milk += milk_tba
        beans_tba = get_num("Write how many grams of coffee beans you want to add")
        self.beans += beans_tba
        cups_tba = get_num("Write how many disposable cups of coffee you want to add:")
        self.cups += cups_tba

    def buy_coffee(self):
        """
        ask user to choose between coffees, if there is enough supplies for
        make a coffee of is choice
        """
        coffees = {'1': Espresso, '2': Latte, '3': Cappuccino}
        while True:
            print()
            print('What do you want to buy?', end=' ')
            for num, type_coffee in coffees.items():
                print(f'{num} - {type_coffee.__name__},', end=' ')
            print('back - to main menu:')
            user_choice = input('')
            if user_choice == 'back':
                break
            if user_choice not in coffees:
                print('Please choose between available options')
                continue
            else:
                coffee = coffees[user_choice]()  # create instance of coffee
                missing_supplies = self.supplies_missing(coffee)
                if len(missing_supplies) != 0:  # not enough supply in machine
                    for supply in missing_supplies:
                        print(f'Sorry, not enough {supply}!')
                    break
                else:  # making coffee
                    print('I have enough resources, making you a coffee!')
                    for info in self.all_text.items():
                        print(info)
                    self.water -= coffee.water
                    self.milk -= coffee.milk
                    self.beans -= coffee.beans
                    self.cups -= coffee.cups
                    self.money += coffee.price
                    break

    def choose_action(self):
        """looping UI """
        actions = {'buy': self.buy_coffee, 'fill': self.fill, 'take': self.take,
                   'remaining': self.show_info, 'exit': 'TOBE ADDED'}
        while True:
            print()
            print(f'Write action:{*actions,}:')
            choice = input()
            if choice == 'exit':
                break
            elif choice not in actions:
                print('Write option , you would like to choose')
                continue
            else:
                actions[choice]()  # execute chosen function immediately
                continue


class Coffee:
    cups = 1


class Espresso(Coffee):
    price = 4  # dollars
    water = 250  # ml
    milk = 0  # ml
    beans = 16  # g


class Latte(Coffee):
    price = 7  # dollars
    water = 350  # ml
    milk = 75  # ml
    beans = 20  # g


class Cappuccino(Coffee):
    price = 6  # dollars
    water = 200  # ml
    milk = 100  # ml
    beans = 12  # g


def get_num(question):
    """asking user for integer"""
    while True:
        print(question)
        answer = input()
        try:
            num = int(answer)
            return num
        except ValueError:
            print('Please insert integer')
            continue


de_loungi = CoffeeMachine(water=400, milk=540, beans=120, cups=9, money=550)
de_loungi.choose_action()
