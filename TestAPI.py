import http.client
import json
from datetime import date, datetime, timedelta
#from sorting import bubble_sort

# convert timezones
def convert_utc_to_est(utc_time_str):
    # Parse the input UTC time string
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    # Subtract 5 hours to convert to EST
    est_time = utc_time - timedelta(hours=5)
    
    return est_time.strftime("%Y-%m-%d %H:%M:%S")

# get the date of tommorow because of timezones
def get_tomorrow_date():
    return (date.today() + timedelta(days=1)).strftime("%Y-%m-%d")
conn = http.client.HTTPSConnection("v2.nba.api-sports.io")

headers = {
    'x-rapidapi-host': "v2.nba.api-sports.io",
    'x-rapidapi-key': "91b4b062e71c0e9038902434701dfa3e"  #replace with key
    }

conn.request("GET", "/games?date=" + get_tomorrow_date(), headers=headers)

res = conn.getresponse()
data1 = res.read()
conn.close()

data_json = json.loads(data1)

glist = data_json["response"]

print(data_json["results"])

Func = open("C:/Users/willz/OneDrive/webdevelopment/NBA Stat Tracking/NBA.html","w") 

if data_json["results"] > 0 :
    title = "NBA Project"    
    csspath = "styles.css"
    
    Func.write('<!DOCTYPE html>\n<html>\n<head>\n<meta charset="utf-8">\n' +
               '<meta name="viewport" content="width=device-width, initial-scale=1">\n' +
               '<title>' + title + '</title>\n' +
               '<link rel="stylesheet" href="' + csspath + '">\n</head>\n<body>\n')
    
    Func.write('<div class="gamesToday">\n<h1>NBA Games Today</h1>\n')                
    
    for game in glist :
        time = game["date"]["start"]
        eastern_time=convert_utc_to_est(time)
        status = game["status"]["long"]
        team_v = game["teams"]["visitors"]["name"]
        team_h = game["teams"]["home"]["name"]
        Func.write('<table class="gtable"><colgroup>\n' +
                    '<col span="1" style="width: 33%;">\n' +
                    '<col span="1" style="width: 34%;">\n' + 
                    '<col span="1" style="width: 33%;"></colgroup>\n' + 
                    '<tr><th colspan="3">'+ eastern_time +  ' (EST)</th></tr>\n' +
                    '<tr><td>' + team_v + '</td>' +
                    '<td>VS</td>' +
                    '<td>' + team_h + '</td></tr></table>\n')
    Func.write('</div>')




# sort the standings based on rank
def bubble_sort(teams):
    n = len(teams)
    for i in range(n):
        for j in range(0, n-i-1):
            if teams[j]["conference"]["rank"] > teams[j+1]["conference"]["rank"]:
                # Swap the elements
                teams[j], teams[j+1] = teams[j+1], teams[j]
    return teams


def makeStandingsTable(conference):
    conn.request("GET", "/standings?league=standard&season=2024&conference=" + conference, headers=headers)
    res = conn.getresponse()
    data = res.read()
    data_json = json.loads(data)
    standings = bubble_sort(data_json["response"])
    Func.write('<header class="standingsHeader">--- ' + conference.capitalize() + 'ern Conference ---</header>')
    Func.write('<table class="standingsTable">')
    Func.write('<tr><td>Team</td>\n' + '<td></td>\n' + '<td></td>\n' + '<td>W</td>\n' + '<td>L</td>\n' + '<td>Pct</td>\n' + '<td>GB</td>\n' + '<td>Home</td>\n' + '<td>Away</td>\n' + '<td>L10</td>\n' + '<td>Strk</td>\n' + '</tr>')
    def winOrLoss(tf):
        if tf == "false":
            return "L"
        else:
            return "W"
    def gb(value):
        if isinstance(value, str):
            return value
        else:
            return "-"
    for team in standings:
        rank = str(team["conference"]["rank"])
        name = team["team"]["name"]
        logo = team["team"]["logo"]
        wins = str(team["conference"]["win"])
        losses = str(team["conference"]["loss"])
        winPct = str(team["win"]["percentage"])
        gamesBehind = gb(team["gamesBehind"])
        homeRecord = str(team["win"]["home"]) + "-" + str(team["loss"]["home"])
        awayRecord = str(team["win"]["away"]) + "-" + str(team["loss"]["away"])
        lastTen = str(team["win"]["lastTen"]) + "-" + str(team["loss"]["lastTen"])
        streak = winOrLoss(str(team["winStreak"])) + str(team["streak"])
        print([name, logo, wins, losses, winPct, gamesBehind, homeRecord, awayRecord, lastTen, streak])
        Func.write('<tr><td>' + rank + '</td><td>' + '<img class = "logo" src="' + logo + '">' + '</td><td>'
                    + name + '</td><td>' + wins + '</td><td>' + losses 
                    + '</td><td>' + winPct + '</td><td>' + "test" + '</td><td>' + homeRecord 
                    + '</td><td>' + awayRecord + '</td><td>' + lastTen + '</td><td>' + streak + '</td></tr>')
    Func.write('</table>')


makeStandingsTable("east")
makeStandingsTable("west")



Func.write('<script> </script> </body> </html>')

# Saving the data into the HTML file 
Func.close()