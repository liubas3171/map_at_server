import urllib.request, urllib.parse, urllib.error
import twurl
import ssl
import json
import pprint


# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py


def load_json_file(acct):
    '''
    :param acct: str, account that you want to explore.
    :return: dict, that represents .json file about account, received from Twitter API.
    '''
    TWITTER_URL = 'https://api.twitter.com/1.1/statuses/user_timeline.json'

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    js = json.loads(data)
    return js


def print_names(section):
    '''dict -> None
    Accept dict that represents part of .json file and prints keys.
    '''
    for name in section:
        pprint.pprint(name)


while True:
    acount = input('Enter Twitter Account:')
    if (len(acount) < 1): break
    js = load_json_file(acount)

    if len(js) < 1:
        print('no Data to this account')
        continue
    elif len(js) > 1:
        print('There are {} elements. Which you want to chose? (enter a number from 0 to {})'.format(len(js),
                                                                                                     len(js) - 1))
        zero_level = int(input(''))
        what_to_output = js[zero_level]
        path = '.json' + '/' + str(zero_level)
    else:
        zero_level = 0
        what_to_output = js[zero_level]
        path = '.json'

    while True:
        avaliable = 'available' if type(what_to_output) == dict else 'not available'
        print('\nPath: {}'.format(path))
        print('What to do next?')
        print('1 - show all possible keys of this object. ({})'.format(avaliable))
        print('2 - print this object.')
        print('3 - you will enter a key for this object. ({})'.format(avaliable))
        print('4 - go to higher level on path.')
        print('5 - go to step where you can enter Twitter Account.')
        ans = input('')

        if ans == '1':
            print_names(what_to_output)
        elif ans == '2':
            pprint.pprint(what_to_output)
        elif ans == '3':
            try:
                key = input('Enter a key, please: ')
                what_to_output = what_to_output[key]
                path += '/' + key
            except KeyError:
                print('You have entered the wrong key, please be more attentive.')
        elif ans == '4':
            new_path = path.split('/')[2: -1]
            what_to_output = js[zero_level]
            path = '.json' + '/' + str(zero_level)
            for i in new_path:
                what_to_output = what_to_output[i]
                path += '/' + i
        else:
            break
