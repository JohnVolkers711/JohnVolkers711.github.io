from xmlrpc.client import DateTime

import requests
from PIL.ImImagePlugin import number
from bs4 import BeautifulSoup
import re
import csv

from numpy.matlib import empty

mlb_teams = {
    "AZ": "Arizona Diamondbacks",
    "ATL": "Atlanta Braves",
    "BAL": "Baltimore Orioles",
    "BOS": "Boston Red Sox",
    "CHC": "Chicago Cubs",
    "CWS": "Chicago White Sox",
    "CIN": "Cincinnati Reds",
    "CLE": "Cleveland Guardians",
    "COL": "Colorado Rockies",
    "DET": "Detroit Tigers",
    "HOU": "Houston Astros",
    "KC": "Kansas City Royals",
    "LAA": "Los Angeles Angels",
    "LAD": "Los Angeles Dodgers",
    "MIA": "Miami Marlins",
    "MIL": "Milwaukee Brewers",
    "MIN": "Minnesota Twins",
    "NYM": "New York Mets",
    "NYY": "New York Yankees",
    "OAK": "Oakland Athletics",
    "PHI": "Philadelphia Phillies",
    "PIT": "Pittsburgh Pirates",
    "SD": "San Diego Padres",
    "SF": "San Francisco Giants",
    "SEA": "Seattle Mariners",
    "STL": "St. Louis Cardinals",
    "TB": "Tampa Bay Rays",
    "TEX": "Texas Rangers",
    "TOR": "Toronto Blue Jays",
    "WSH": "Washington Nationals"
}
count = 0

def write_game_to_csv(date, home_team, home_score, away_team, away_score):
    """Writes a game's details to a CSV file, creating headers if the file is new."""

    # Define the header and row data
    header = ["ID", "Date", "Home Team", "Home Score", "Away Team", "Away Score"]
    row = [count+1, date, home_team, home_score, away_team, away_score]

    # Open the file in append mode, create header only if the file is new
    try:
        with open("mlbGames.csv", mode="a", newline="") as file:
            writer = csv.writer(file)

            # Check if the file is empty, and write the header if needed
            if file.tell() == 0:
                writer.writerow(header)

            # Write the game data
            writer.writerow(row)
            print(f"Game added: {row}")

    except Exception as e:
        print(f"Error writing to file: {e}")

def clear_csv():
    """Clears all content from the specified CSV file."""
    with open("mlbGames.csv", mode="w", newline="") as file:
        pass  # Opening in "w" mode without writing anything clears the file

    print(f"mlbGames.csv has been cleared.")




##    WEB CRAWLER CODE BELOW    ##

# Target URL
# url = "https://www.myfitnesspal.com/food/search?search=banana"
urlPrefix = "https://www.mlb.com/schedule/"
# urlPostfix = "-schedule.shtml"

from datetime import date, timedelta

def list_dates(start_date, end_date):
  """Generates a list of dates between two dates (inclusive).

  Args:
    start_date: The start date (datetime.date object).
    end_date: The end date (datetime.date object).

  Returns:
    A list of datetime.date objects.
  """
  dates = []
  delta = end_date - start_date
  for i in range(delta.days + 1):
    day = start_date + timedelta(days=i)
    dates.append(day)
  return dates

# Example usage:
start_date = date(2010, 3, 1)
end_date = date(2025, 1, 1)
date_list = list_dates(start_date, end_date)
for date_item in date_list:
  print(date_item.strftime("%Y-%m-%d")) # Format date as YYYY-MM-DD

# clear_csv()

# Set headers to avoid bot detection
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


for date in date_list:
    url = urlPrefix + date.__str__()

# Send request
    response = requests.get(url, headers=headers)

    # Check if request was successful
    if response.status_code == 200:
        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")

        wrapper = soup.find("div", id="gridWrapper")
        header = wrapper.find("div").text
        # Skips Spring Training Games
        if header.__contains__("Spring"):
            continue
        temp = wrapper.find(lambda tag: tag.has_attr("class") and any("ScheduleCollectionGridstyle__SectionWrapper" in c for c in tag["class"]))

        if temp:
            # This skips all-star games and etc.
            ahh = temp.text.strip()
            ahhh = ahh[:2]
            ahhhh = ahh[:3]
            if not mlb_teams.__contains__(ahh[:2]):
                if not mlb_teams.__contains__(ahh[:3]):
                    temp = wrapper.find_all(lambda tag: tag.has_attr("class") and any("ScheduleCollectionGridstyle__SectionWrapper" in c for c in tag["class"]))
                    temp = temp[1]
            # games = wrapper.find_all("div", class_="ScheduleCollectionGridstyle__SectionWrapper-sc-c0iua4-0 guIOQi")
            games = temp.find_all("div", recursive=False)
            if games:
                for game in games:
                    subDivs = game.find_all("div", recursive=False)
                    if len(subDivs) == 0:
                        continue
                    firstDiv = subDivs[0]
                    subfirstDiv = firstDiv.find_all("div", recursive=False)
                    temp = subfirstDiv[len(subfirstDiv)-1].text
                    homeTeam = temp[:int(len(temp)/2)]

                    # This skips games that aren't a part of the regular season
                    if not mlb_teams.__contains__(homeTeam):
                        continue

                    secondSubDuv = subDivs[1]
                    scoreText = secondSubDuv.text
                    scores = scoreText.split(",")
                    for str in scores:
                        str = str.strip()

                    # If the game was canceled or postponed, it will skip and continue
                    if scores[0] == "Postponed" or scores[0] == "Canceled" or scores[1] == "Postponed" or scores[1] == "Canceled":
                        continue
                    else:
                        try:
                            team1name, team1score = scores[0].split()
                        except Exception as e:
                            print(f"Error splitting: {scores[0]}")

                        team2name, team2score = scores[1].split()
                        if (homeTeam == team1name):
                            write_game_to_csv(date.__str__(), mlb_teams.get(team1name), team1score, mlb_teams.get(team2name), team2score)
                        else:
                            write_game_to_csv(date.__str__(), mlb_teams.get(team2name), team2score, mlb_teams.get(team1name), team1score)
                        # write_game_to_csv(date, )
                        count = count+1
            else:
                print("No food items found. The site may use JavaScript.")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

print(f"Games Counted: {count}")


