import requests
from PIL.ImImagePlugin import number
from bs4 import BeautifulSoup
import re
import csv

from numpy.matlib import empty
count = 0

def convertDateString(date_string):
    from datetime import datetime

    # Convert to datetime object
    date_object = datetime.strptime(date_string, "%A, %B %d, %Y")

    # Format as YYYY-MM-DD
    return date_object.strftime("%Y-%m-%d")


def write_game_to_csv(date, home_team, home_score, away_team, away_score):
    """Writes a game's details to a CSV file, creating headers if the file is new."""

    # Define the header and row data
    header = ["ID", "Date", "Home Team", "Home Score", "Away Team", "Away Score"]
    row = [count+1, convertDateString(date), home_team, home_score, away_team, away_score]

    # Open the file in append mode, create header only if the file is new
    try:
        with open("mlbGames2.csv", mode="a", newline="") as file:
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
    with open("mlbGames2.csv", mode="w", newline="") as file:
        pass  # Opening in "w" mode without writing anything clears the file

    print(f"mlbGames.csv has been cleared.")

# Target URL
# url = "https://www.myfitnesspal.com/food/search?search=banana"
urlPrefix = "https://www.baseball-reference.com/leagues/majors/"
urlPostfix = "-schedule.shtml"

clear_csv()

# Set headers to avoid bot detection
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

years = [2010,2011,2012,2013,2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024]
# years = [2024]

for year in years:
    url = urlPrefix + str(year) + urlPostfix

# Send request
    response = requests.get(url, headers=headers)

    # Check if request was successful
    if response.status_code == 200:
        # Parse HTML
        soup = BeautifulSoup(response.text, "html.parser")


        content = soup.find("div", id="content")
        group = content.find("div", class_="section_content")  # Adjust based on site structure
        days = group.find_all("div")
        if days:
            for day in days:
                date = day.find("h3").text.strip()
                games = day.find_all("p",recursive=False)
                if date == "Thursday, March 28, 2024":
                    print()
                for i in range(len(games)):
                    if i != len(games)-1:
                        game = games[i]
                        teams = game.find_all("a")  # Try different tags
                        team1 = teams[0]  # Adjust class
                        team2 = teams[1]
                        team1score = None
                        team2score = None

                        gameString = game.text.strip()
                        # Extract numbers inside parentheses
                        numbers = re.findall(r"\((\d+)\)", gameString)
                        if numbers:
                            numbers = [int(num) for num in numbers]  # Convert to integers
                            team1score = numbers[0]
                            team2score = numbers[1]


                        if team1 and team2 and team1score and team2score:
                            # print(f"{date} : Team 1: {team1.text.strip()} ({team1score}) - Team 2: {team2.text.strip()} ({team2score})")
                            write_game_to_csv(date, team2.text.strip(), team2score, team1.text.strip(), team1score)
                            count = count + 1
        else:
            print("No food items found. The site may use JavaScript.")
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")

print(f"Games Counted: {count}")

