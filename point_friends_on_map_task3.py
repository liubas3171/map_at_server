import urllib.request, urllib.parse, urllib.error
import twurl
import json
import ssl
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
from flask import Flask, render_template, request

app = Flask(__name__)


# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

def make_json_file(nickname):
    '''str -> dict
    Accept name of Telegram account and return dict that represents .json file about this acc.
    '''
    TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'
    #
    # # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # if count bigger, geopy crashs
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': nickname, 'count': 25})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    js = json.loads(data)
    return js


def make_map(js):
    '''dict -> None
    Accept dict that represents .json file about account
    and put markers with locations of his friends at map on file 'map.html'.
    '''
    lst_name_location = []
    for user in js['users']:
        lst_name_location.append((user['screen_name'], user['location']))

    coordinates = []
    geolocator = Nominatim(user_agent="specify_your_app_name_here")
    geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1, max_retries=2)
    for tpl in lst_name_location:
        location = geolocator.geocode(tpl[1])
        # if geocode return None
        try:
            coordinates.append((tpl[0], (location.latitude, location.longitude)))
        except AttributeError:
            continue

    m = folium.Map(location=[coordinates[0][1][0], coordinates[0][1][1]], zoom_start=12)
    tooltip = 'click to know a name of account'
    y = 0
    for tpl in coordinates:
        # add a few degrees to latitude because don't know how create marker in the same location.
        folium.Marker(location=[tpl[1][0], tpl[1][1] + y], popup=tpl[0], tooltip=tooltip).add_to(m)
        y += 0.001
    mapp = m.get_root().render()
    return mapp


@app.route('/')
def register():
    return render_template('main.html')


@app.route('/map', methods=['GET', 'POST'])
def mapa():
    if request.method == 'POST':
        acct = str(request.form['account'])

        js = make_json_file(acct)
        res = {'point_on_map': make_map(js)}
    return render_template('map.html', **res)


if __name__ == '__main__':
    app.run(debug=True)
