import json
import time
from geopy import geocoders

teams_lookup = [
    { 'abbr': 'bos', 'full_name': 'boston-celtics', 'location': 'Boston', 'nickname': 'Celtics', 'city': 'Boston', 'arena': 'TD Garden', 'lat': 'dummy', 'lon': 'dummy', 'address': '100 Legends Way, Boston, MA 02114', 'conference': 'East', 'division': 'Atlantic'},
    { 'abbr': 'bkn', 'full_name': 'brooklyn-nets', 'location': 'Brooklyn', 'nickname': 'Nets', 'city': 'Brooklyn', 'arena': 'Barclays Center', 'lat': 'dummy', 'lon': 'dummy', 'address': '620 Atlantic Avenue, Brooklyn, NY 112','conference': 'East', 'division': 'Atlantic'},
    { 'abbr': 'ny', 'full_name': 'new-york-knicks', 'location': 'New York', 'nickname': 'Knicks', 'city': 'New York City', 'arena': 'Madison Square Garden', 'lat': 'dummy', 'lon': 'dummy', 'address': 'Four Pennsylvania Plaza, New York, NY 10001', 'conference': 'East', 'division': 'Atlantic'},
    { 'abbr': 'phi', 'full_name': 'philadelphia-76ers', 'location': 'Philadelphia', 'nickname': '76ers', 'city': 'Philadelphia', 'arena': 'Wells Fargo Center', 'lat': 'dummy', 'lon': 'dummy', 'address': '3601 S. Broad St., Philadelphia, PA 19148', 'conference': 'East', 'division': 'Atlantic'},
    { 'abbr': 'tor', 'full_name': 'toronto-raptors', 'location': 'Toronto', 'nickname': 'Raptors', 'city': 'Toronto', 'arena': 'Air Canada Centre', 'lat': 'dummy', 'lon': 'dummy', 'address': '40 Bay St., Toronto, ON M5J 2X2', 'conference': 'East', 'division': 'Atlantic'},
    { 'abbr': 'gs', 'full_name': 'golden-state-warriors', 'location': 'Golden State', 'nickname': 'Warriors', 'city': 'Oakland', 'arena': 'Oracle Arena', 'lat': 'dummy', 'lon': 'dummy', 'address':'7000 Coliseum Way, Oakland, CA 94621', 'conference': 'West', 'division': 'Pacific'},
    { 'abbr': 'lac', 'full_name': 'los-angeles-clippers', 'location': 'Los Angeles', 'nickname': 'Clippers', 'city': 'Los Angeles', 'arena': 'Staples Center', 'lat': 'dummy', 'lon': 'dummy', 'address': '1111 S. Figueroa St., Los Angeles, CA 90015', 'conference': 'West', 'division': 'Pacific' },
    { 'abbr': 'lal', 'full_name': 'los-angeles-lakers', 'location': 'Los Angeles', 'nickname': 'Lakers', 'city': 'Los Angeles', 'arena': 'Staples Center', 'lat': 'dummy', 'lon': 'dummy', 'address': '1111 S. Figueroa St., Los Angeles, CA 90015', 'conference': 'West', 'division': 'Pacific'},
    { 'abbr': 'phx', 'full_name': 'phoenix-suns', 'location': 'Phoenix', 'nickname': 'Suns', 'city': 'Phoenix', 'arena': 'US Airways Center', 'lat': 'dummy', 'lon': 'dummy', 'address': '201 E. Jefferson St., Phoenix, AZ 85004', 'conference': 'West', 'division': 'Pacific'},
    { 'abbr': 'sac', 'full_name': 'sacramento-kings', 'location': 'Sacramento', 'nickname': 'Kings', 'city': 'Sacramento', 'arena': 'Sleep Train Arena', 'lat': 'dummy', 'lon': 'dummy', 'address':'One Sports Parkway, Sacramento, CA 95834', 'conference': 'West', 'division': 'Pacific'},
    { 'abbr': 'chi', 'full_name': 'chicago-bulls', 'location': 'Chicago', 'nickname': 'Bulls', 'city': 'Chicago', 'arena': 'United Center', 'lat': 'dummy', 'lon': 'dummy', 'address': '1901 W. Madison St., Chicago, IL 60612', 'conference': 'East', 'division': 'Central'},
    { 'abbr': 'cle', 'full_name': 'cleveland-cavaliers', 'location': 'Cleveland', 'nickname': 'Cavaliers', 'city': 'Cleveland', 'arena': 'Quicken Loans Arena', 'lat': 'dummy', 'lon': 'dummy', 'address': 'One Center Court, Cleveland, OH 44115', 'conference': 'East', 'division': 'Central'},
    { 'abbr': 'det', 'full_name': 'detroit-pistons', 'location': 'Detroit', 'nickname': 'Pistons', 'city': 'Auburn Hills', 'arena': 'The Palace of Auburn Hills', 'lat': 'dummy', 'lon': 'dummy', 'address': 'Six Championship Drive, Auburn Hills, MI 48326', 'conference': 'East', 'division': 'Central'},
    { 'abbr': 'ind', 'full_name': 'indiana-pacers', 'location': 'Indiana', 'nickname': 'Pacers', 'city': 'Indianapolis', 'arena': 'Bankers Life Fieldhouse', 'lat': 'dummy', 'lon': 'dummy', 'address': '125 S. Pennsylvania St., Indianapolis, IN 46204', 'conference': 'East', 'division': 'Central'},
    { 'abbr': 'mil', 'full_name': 'milwaukee-bucks', 'location': 'Milwaukee', 'nickname': 'Bucks', 'city': 'Milwaukee', 'arena': 'BMO Harris Bradley Center', 'lat': 'dummy', 'lon': 'dummy', 'address': '1001 N. Fourth St., Milwaukee, WI 53203', 'conference': 'East', 'division': 'Central'},
    { 'abbr': 'dal', 'full_name': 'dallas-mavericks', 'location': 'Dallas', 'nickname': 'Mavericks', 'city': 'Dallas', 'arena': 'American Airlines Center', 'lat': 'dummy', 'lon': 'dummy', 'address': '2500 Victory Ave., Dallas, TX 75219', 'conference': 'West', 'division': 'Southwest'},
    { 'abbr': 'hou', 'full_name': 'houston-rockets', 'location': 'Houston', 'nickname': 'Rockets', 'city': 'Houston', 'arena': 'Toyota Center', 'lat': 'dummy', 'lon': 'dummy', 'address': '1510 Polk St., Houston, TX 77002', 'conference': 'West', 'division': 'Southwest'},
    { 'abbr': 'mem', 'full_name': 'memphis-grizzlies', 'location': 'Memphis', 'nickname': 'Grizzlies', 'city': 'Memphis', 'arena': 'FedExForum', 'lat': 'dummy', 'lon': 'dummy', 'address': '191 Beale St., Memphis, TN 38103', 'conference': 'West', 'division': 'Southwest'},
    { 'abbr': 'no', 'full_name': 'new-orleans-pelicans', 'location': 'New Orleans', 'nickname': 'Pelicans', 'city': 'New Orleans', 'arena': 'New Orleans Arena', 'lat': 'dummy', 'lon': 'dummy', 'address': '1501 Girod St., New Orleans, LA 70113', 'conference': 'West', 'division': 'Southwest'},
    { 'abbr': 'sa', 'full_name': 'san-antonio-spurs', 'location': 'San-Antonio', 'nickname': 'Spurs', 'city': 'San Antonio', 'arena': 'AT&T Center', 'lat': 'dummy', 'lon': 'dummy', 'address': 'One AT&T Center Parkway, San Antonio, TX 78219', 'conference': 'West', 'division': 'Southwest'},
    { 'abbr': 'atl', 'full_name': 'atlanta-hawks', 'location': 'Atlanta', 'nickname': 'Hawks', 'city': 'Atlanta', 'arena': 'Philips Arena', 'lat': 'dummy', 'lon': 'dummy', 'address': 'One Philips Drive, Atlanta, GA 30303', 'conference': 'East', 'division': 'Southeast'},
    { 'abbr': 'cha', 'full_name': 'charlotte-bobcats', 'location': 'Charlotte', 'nickname': 'Bobcats', 'city': 'Charlotte', 'arena': 'Time Warner Cable Arena', 'lat': 'dummy', 'lon': 'dummy', 'address': '330 E. Trade St., Charlotte, NC 28202', 'conference': 'East', 'division': 'Southeast'},
    { 'abbr': 'mia', 'full_name': 'miami-heat', 'location': 'Miami', 'nickname': 'Heat', 'city': 'Miami', 'arena': 'AmericanAirlines Arena', 'lat': 'dummy', 'lon': 'dummy', 'address': '601 Biscayne Blvd., Miami, FL 33132', 'conference': 'East', 'division': 'Southeast'},
    { 'abbr': 'orl', 'full_name': 'orlando_magic', 'location': 'Orlando', 'nickname': 'Magic', 'city': 'Orlando', 'arena': 'Amway Center', 'lat': 'dummy', 'lon': 'dummy', 'address': '400 W. Church St., Orlando, FL 32801', 'conference': 'East', 'division': 'Southeast'},
    { 'abbr': 'wsh', 'full_name': 'washington-wizards', 'location': 'Washington', 'nickname': 'Wizards', 'city': 'Washington D.C.', 'arena': 'Verizon Center', 'lat': 'dummy', 'lon': 'dummy', 'address': '601 F St. N.W., Washington, D.C. 20004', 'conference': 'East', 'division': 'Southeast'},
    { 'abbr': 'den', 'full_name': 'denver-nuggets', 'location': 'Denver', 'nickname': 'Nuggets', 'city': 'Denver', 'arena': 'Pepsi Center', 'lat': 'dummy', 'lon': 'dummy', 'address': '1000 Chopper Circle, Denver, CO 80204', 'conference': 'West', 'division': 'Northwest'},
    { 'abbr': 'min', 'full_name': 'minnesota-timberwolves', 'location': 'Minnesota', 'nickname': 'Timberwolves', 'city': 'Minneapolis', 'arena': 'Target Center', 'lat': 'dummy', 'lon': 'dummy', 'address': '600 First Ave. North, Minneapolis, MN 55403', 'conference': 'West', 'division': 'Northwest'},
    { 'abbr': 'okc', 'full_name': 'oklahoma-city-thunder', 'location': 'Oklahoma City', 'nickname': 'Thunder', 'city': 'Oklahoma City', 'arena': 'Chesapeake Energy Arena', 'lat': 'dummy', 'lon': 'dummy', 'address': '100 W. Reno Ave., Oklahoma City, OK 73102', 'conference': 'West', 'division': 'Northwest'},
    { 'abbr': 'por', 'full_name': 'portland-trail-blazers', 'location': 'Portland', 'nickname': 'Trail Blazers', 'city': 'Portland', 'arena': 'Rose Garden', 'lat': 'dummy', 'lon': 'dummy', 'address': 'One Center Court, Portland, OR 97227', 'conference': 'West', 'division': 'Northwest'},
    { 'abbr': 'utah', 'full_name': 'utah-jazz', 'location': 'Utah', 'nickname': 'Jazz', 'city': 'Salt Lake City', 'arena': 'EnergySolutions Arena', 'lat': 40.768268, 'lon': -111.901087, 'address': '301 W. South Temple St., Salt Lake City, UT 84101', 'conference': 'West', 'division': 'Northwest'}
]

if __name__ == '__main__':

    for team in teams_lookup:
        if team['lat'] == 'dummy': # Utah's arena doesn't geocode for some reason so got it manually
            g = geocoders.GoogleV3()
            place, (lat, lon) = g.geocode(team['address'])
            team['lat'] = lat
            team['lon'] = lon
            time.sleep(3)
    f = open('../data/json/teams.json', 'w')
    teams = { 'teams' : teams_lookup }
    final_json = json.dumps(teams, sort_keys=False, indent=2)
    f.write(final_json)
    f.close()