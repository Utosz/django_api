import requests


def is_num(data):
    try:
        int(data)
        return True
    except ValueError:
        return False


def data_gather(i, dictionary):
    temp = requests.POST.get(f'{i}')
    if temp:
        dictionary[f'{i}'] = temp
        return dictionary[f'{i}']


def connect(param):
    parms = {"q": param}
    try:
        r = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=parms)
    except requests.exceptions.RequestException as e:
        print(e)
        return False
    return r


def parse_n_find(r):
    rj = r.json()
    dict_r = dict(rj)
    if rj['totalItems'] == 0:
        return False
    results = [i[key] for i in dict_r['items'] for key in i if key == 'volumeInfo']
    return results


def get_data(parsed_list, find_key):
    counter = 0
    d_result = {}
    for dictionary in parsed_list:
        counter += 1
        d_result[counter] = {key: dictionary[key] for key in dictionary if key in find_key}
    return d_result
