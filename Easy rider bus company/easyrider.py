import json
from datetime import datetime as dt
import collections


def required_and_int(item):
    if item == '':
        # print('missing')
        return False
    if not isinstance(item, int):
        # print('wrong type')
        return False
    return True


def correct_stop_name(item):
    if not item:
        return False
    if not isinstance(item, str):
        return False

    parts = item.split()
    if len(parts) < 2:
        return False
    if not parts[0].istitle():
        return False
    if parts[-1] not in ["Road", "Avenue", "Boulevard", "Street"]:
        return False

    return True


def correct_stop_type(item):
    if item not in ["", "S", "O", "F"]:
        return False
    return True


def correct_time(item):
    if item == '':
        # print('missing')
        return False
    if not isinstance(item, str):
        # print('wrong type')
        return False
    try:
        dt.strptime(item, '%H:%M')
    except ValueError:
        return False
    else:
        return len(item) == 5


def find_errors(data):
    fields_errors = dict(bus_id=0, stop_id=0, stop_name=0, next_stop=0,
                         stop_type=0, a_time=0)
    # take each bus_info one by one and check it
    for bus in data:
        if not required_and_int(bus['bus_id']):
            fields_errors['bus_id'] += 1
        if not required_and_int(bus['stop_id']):
            fields_errors['stop_id'] += 1
        if not correct_stop_name(bus['stop_name']):
            fields_errors['stop_name'] += 1
        if not required_and_int(bus['next_stop']):
            fields_errors['next_stop'] += 1
        if not correct_stop_type(bus['stop_type']):
            fields_errors['stop_type'] += 1
        if not correct_time(bus['a_time']):
            fields_errors['a_time'] += 1

    total_errors = sum(fields_errors.values())
    print(f'Type and required field validation: {total_errors} errors')
    for field, errors in fields_errors.items():
        print(f'{field}: {errors}')


def count_lines(data):
    lines_data = {}
    for bus in data:
        name = bus['bus_id']
        lines_data[name] = lines_data.get(name, 0) + 1

    print('Line names and number of stops:')


def count_special_stops(data):
    start_stops = []
    finish_stops = []
    other = {}

    c_types = collections.defaultdict(list)

    for bus in data:
        line = bus['bus_id']
        stop_name = bus['stop_name']
        stop_type = bus['stop_type']

        other[stop_name] = other.get(stop_name, 0) + 1
        if stop_type == 'S':
            start_stops.append(stop_name)
            c_types[line].append(stop_type)
        elif stop_type == 'F':
            finish_stops.append(stop_name)
            c_types[line].append(stop_type)

    for line, sf_stops in c_types.items():
        if 'F' not in sf_stops or 'S' not in sf_stops:
            print(f'There is no start or end stop for the line: {line}.')
            break

    else:
        transfer_stops = [stop for stop, count in other.items() if count > 1]

        s = sorted(set(start_stops))
        t = sorted(transfer_stops)
        f = sorted(set(finish_stops))

        print(f'Start stops: {len(s)} {s}')
        print(f'Transfer stops: {len(t)} {t}')
        print(f'Finish stops: {len(f)} {f}')

        return set(s+t+f)


def time_increase(data):
    print('Arrival time test:')
    checked_lines = []

    for bus in data:
        line = bus['bus_id']
        next_id = bus['next_stop']

        if line in checked_lines:
            continue

        next_bus = next((item for item in data if item["stop_id"] == next_id and item['bus_id'] == line), None)
        try:
            if bus['a_time'] >= next_bus['a_time']:
                print(f'bus_id line {line}: wrong time on station {next_bus["stop_name"]}')
                checked_lines.append(line)
        except TypeError:
            continue

    if len(checked_lines) == 0:
        print('OK')


def check_on_demand(data, forbidden_list):
    print('On demand stops test:')
    wrong_stops = set()
    for bus in data:
        stop_type = bus['stop_type']
        stop_name = bus['stop_name']
        if stop_type == 'O' and stop_name in forbidden_list:
            wrong_stops.add(stop_name)
    if len(wrong_stops):
        print(sorted(wrong_stops))
    else:
        print('OK')


json_string = input()
data = json.loads(json_string)

# with open('try.json') as file:
#     data = json.load(file)

x = count_special_stops(data)
check_on_demand(data, x)
