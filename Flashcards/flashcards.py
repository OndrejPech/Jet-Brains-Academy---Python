import random
import json
from io import StringIO
import argparse

TERM = "term"
DEFINITION = "definition"


def print_log(message: str):
    print(message)
    memory_file.write(message + '\n')


def input_log():
    user_input = input()
    memory_file.write(user_input + '\n')
    return user_input


def check_answer(term: str, user_answer: str) -> None:
    correct_answer = all_cards[term]
    if correct_answer == user_answer:
        print_log('Correct')
    else:
        hard_cards[term] = hard_cards.get(term, 0) + 1

        for cur_term, cur_definition in all_cards.items():
            if cur_definition == user_answer:
                output = (f'Wrong. The right answer is "{correct_answer}", '
                          f'but your {DEFINITION} is correct for "{cur_term}"card.')
                print_log(output)
                break
        else:
            print_log(f'Wrong. The right answer is "{correct_answer}".')


def item_exists(item: str, collection: iter, item_name: str):
    if item in collection:
        print_log(f'The {item_name} "{item}" already exists. Try again:')
        return True
    return False


def add_card():
    print_log(f"The {TERM} for card:")
    while True:
        term = input_log()
        if not item_exists(term, all_cards, TERM):
            break

    print_log(f"The {DEFINITION} for card:")
    while True:
        definition = input_log()
        if not item_exists(definition, all_cards.values(), DEFINITION):
            break

    all_cards[term] = definition
    print_log(f'The pair ("{term}":"{definition}") has been added.')


def remove_card():
    print_log("Which card?")
    term = input_log()
    try:
        del all_cards[term]
        print_log("The card has been removed.")
    except KeyError:
        print_log(f"""Can't remove "{term}": there is no such card.""")


def import_cards(file_name=None):
    if not file_name:
        print_log("File name:")
        file_name = input_log()
    try:
        with open(file_name) as file:
            imported_cards = json.load(file)
    except FileNotFoundError:
        print_log("File not found.")
    else:
        all_cards.update(imported_cards)
        print_log(f"{len(imported_cards)} cards have been loaded.")


def export_cards(file_name=None):
    if not file_name:
        print_log("File name:")
        file_name = input_log()
    with open(file_name, 'w') as file:
        json.dump(all_cards, file)
        print_log(f"{len(all_cards)} cards have been saved.")


def lets_practice():
    print_log("How many times to ask?")
    while True:
        num = input_log()
        try:
            num = int(num)
            break
        except ValueError:
            print_log("Please insert an integer!")

    for i in range(num):
        term = random.choice(list(all_cards))
        print_log(f'Print the {DEFINITION} of "{term}":')
        answer = input_log()
        check_answer(term, answer)


def show_hardest_cards():
    if not hard_cards:
        print_log("There are no cards with errors.")
    else:
        most_mistakes_num = max(hard_cards.values())
        hardest_terms = [term for term, mistakes in hard_cards.items() if mistakes == most_mistakes_num]

        if len(hardest_terms) == 1:
            output = (f'The hardest card is "{hardest_terms[0]}". '
                      f'You have {most_mistakes_num} errors answering it')
            print_log(output)
        else:
            unpacked = ', '.join([f'"{item}"' for item in hardest_terms])
            output = (f'The hardest cards are {unpacked}. '
                      f'You have {most_mistakes_num} errors answering them')
            print_log(output)


def log():
    print_log("File name:")
    file_name = input_log()

    log_info = memory_file.getvalue()
    with open(file_name, 'w') as log_file:
        log_file.write(log_info)

    print_log("The log has been saved")


def main_menu():
    while True:
        output = 'Input the action (add, remove, import, export, ask, exit, log, hardest card, reset stats):'
        print_log(output)
        choice = input_log()

        if choice == "add":
            add_card()
        elif choice == "remove":
            remove_card()
        elif choice == "import":
            import_cards()
        elif choice == "export":
            export_cards()
        elif choice == "ask":
            lets_practice()
        elif choice == "log":
            log()
        elif choice == "hardest card":
            show_hardest_cards()
        elif choice == "reset stats":
            hard_cards.clear()
            print_log("Card statistics have been reset.")
        elif choice == "exit":
            print_log("Bye bye!")
            if args.export_to is not None:
                export_cards(file_name=args.export_to)
            quit()
        else:
            print_log("unknown action")


if __name__ == "__main__":
    all_cards = {}
    hard_cards = {}
    memory_file = StringIO()

    parser = argparse.ArgumentParser(description="About this program")
    parser.add_argument('--import_from', help='file to be imported from')
    parser.add_argument('--export_to', help='file to be exported to')
    args = parser.parse_args()

    if args.import_from is not None:
        import_cards(file_name=args.import_from)

    main_menu()
