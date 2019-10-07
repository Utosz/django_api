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
    #googleapikey = "AIzaSyBs6O9832V7DdVDyoLiRWqmBQw7KDN7qN0"
    parms = {"q": param}
    r = requests.get(url="https://www.googleapis.com/books/v1/volumes", params=parms)
    return r


def parse_n_find(r, ):
    rj = r.json()
    dict_r = dict(rj)
    results = [i[key] for i in dict_r['items'] for key in i if key == 'volumeInfo']
    return results


def get_data(parsed_list, find_key):
    counter = 0
    d_result = {}
    for dictionary in parsed_list:
        counter += 1
        d_result[counter] = {key: dictionary[key] for key in dictionary if key in find_key}
        print(str(counter) + " " + str(d_result[counter]))
    return d_result
