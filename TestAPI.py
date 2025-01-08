import http.client
import json
from datetime import date, datetime, timedelta

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

if data_json["results"] > 0 :
    Func = open("nba.html","w") 

    title = "NBA Project"    
    csspath = "styles.css"
    
    Func.write('<!DOCTYPE html>\n<html>\n<head>\n<meta charset="utf-8">\n' +
               '<meta name="viewport" content="width=device-width, initial-scale=1">\n' +
               '<title>' + title + '</title>\n' +
               '<link rel="stylesheet" href="' + csspath + '">\n</head>\n<body>\n')
    
    Func.write('<div>\n<h1>NBA Games Today</h1>\n')                
    
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
                    '<tr><th colspan="3">'+ eastern_time +  ' (EST)' + '</th></tr>\n' +
                    '<tr><td>' + team_v + '</td>' +
                    '<td>VS</td>' +
                    '<td>' + team_h + '</td></tr></table>\n')
    Func.write('</div><script> </script> </body> </html>')

    # Saving the data into the HTML file 
    Func.close()
    



# EASTERN CONFERENCE
conn.request("GET", "/standings?league=standard&season=2024&conference=east", headers=headers)

res2 = conn.getresponse()
data2 = res2.read()

data2_json = json.loads(data2)

standings = data2_json["response"]


for team in standings:
    rank = team["conference"]["rank"]
    name = team["team"]["name"]
    logo = team["team"]["logo"]
    wins = team["conference"]["win"]
    losses = team["conference"]["loss"]
    winPct = team["win"]["percentage"]
    homeRecord = str(team["win"]["home"]) + "-" + str(team["loss"]["home"])
    awayRecord = str(team["win"]["away"]) + "-" + str(team["loss"]["away"])
    lastTen = str(team["win"]["lastTen"]) + "-" + str(team["loss"]["lastTen"])
    print([name, logo, wins, losses, winPct, homeRecord, awayRecord, lastTen])
    #Func.write('<tr><td>' + rank + '</td>' + '<td>' + name + '</td>' + '<td>'
                #+ logo + '</td>'+ '<td>' + wins + '</td>'+ '<td>' + losses + '</td>'
                #+ '<td>' + winPct + '</td>'+ '<td>' + homeRecord + '</td>'
                #+ '<td>' + awayRecord + '</td>'+ '<td>' + lastTen + '</td>')