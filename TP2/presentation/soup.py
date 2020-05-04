from bs4 import BeautifulSoup
import urllib3

http = urllib3.PoolManager()
r = http.request("GET", "https://steamdb.info/")


soup = BeautifulSoup(r.data, "lxml")

for div in soup.body.find_all("div", "span6"):
    if div.table.thead.tr.th.text == "Most Played Games":
        game_names = div.table.tbody.select("tr")


for game in game_names:
    element = game.select("td")
    if len(element) > 1:
        print(
            "---------------------------------------\n\nGame: ",
            element[1].text.replace("\n", ""),
            "\nPlayers Now: ",
            element[2].text,
            "\nPlayers Peak: ",
            element[3].text,
            "\n",
        )
