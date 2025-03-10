import csv
from datetime import datetime, timedelta
from rapidfuzz import fuzz

def readCsv(filename):
    with open(filename, mode="r", newline="") as file:
        reader = csv.reader(file)
        header = next(reader)

        print(header)

        data = []
        for row in reader:
            temp = []
            for i in range(len(row)):
                temp.append(row[i])
            data.append(temp)

        return header, data

def write_to_csv(filename, headers, data):
    headerRow = ["ID"]
    for i in range(len(headers)):
        for att in headers[i]:
            if i == 0:
                headerRow.append("ltable_" + att)
            if i == 1:
                headerRow.append("rtable_" + att)
            if i == 2:
                headerRow.append("stable_" + att)


    # Open the file in append mode, create header only if the file is new
    try:
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)

            writer.writerow(headerRow)
            print(headerRow)

            counter = 1
            # Write the game data
            for game in data:
                temp = [counter]
                for att in game:
                    temp.append(att)
                writer.writerow(temp)
                counter += 1

    except Exception as e:
        print(f"Error writing to file: {e}")


def match_team_names(team1, team2):

    similarity_score = fuzz.ratio(team1.lower(), team2.lower()) / 100  # Convert to 0-1 scale
    return round(similarity_score, 2)  # Round for clarity


def verifyGameResults(row1, row2):
    if (row1[1] == row2[1] and # Date
            (match_team_names(row1[2],row2[2]) >= 0.6) and # Home Team
            (int(row1[3]) == int(row2[3])) and #Home Score
            (match_team_names(row1[4],row2[4]) >= 0.6) and # Away Team
            (int(row1[5]) == int(row2[5]))): # Away Score
        return True
    return False

def getStadium(homeTeam, date, stadiums):
    year = datetime.strptime(date, "%Y-%m-%d").year
    validStadiums = []
    for stadium in stadiums:
        if (stadium[1] in homeTeam or homeTeam in stadium[1]) and year >= int(stadium[5]):
            validStadiums.append(stadium)
    if len(validStadiums) == 1:
        return validStadiums[0]
    if validStadiums:
        validStadiums.sort(key=lambda x: int(x[5]))
        validStadiums.reverse()
        return validStadiums[0]


if __name__ == "__main__":
    header1, games1 = readCsv("mlbGames.csv")
    header2, games2 = readCsv("mlbGames2.csv")
    stadiumHeaders, stadiums = readCsv("MLBStadiums.csv")
    stadiumHeaders[0] = "ID" # Fixing weird formatting issue

    # Consolidating Headers to follow standard format
    for i in  range(len(header1)):
        temp = header1[i].split(" ")
        if len(temp) > 1:
            header1[i] = temp[0] + temp[1]
    for i in  range(len(header2)):
        temp = header2[i].split(" ")
        if len(temp) > 1:
            header2[i] = temp[0] + temp[1]
    for i in  range(len(stadiumHeaders)):
        temp = stadiumHeaders[i].split(" ")
        if len(temp) > 1:
            stadiumHeaders[i] = temp[0] + temp[1]

    matches = []

    prob = match_team_names("LA Angels of Anaheim", "Los Angeles Angels")
    prob2 = match_team_names("Los Angeles Dodgers", "Los Angeles Angels")

    noMatch = []
    for game1 in games1:
        matched = False

        for game2 in games2:
            if verifyGameResults(game1, game2):
                stadium = getStadium(game1[2], game1[1], stadiums)
                if stadium:
                    temp = []
                    for att in game1:
                        temp.append(att)
                    for att in game2:
                        temp.append(att)
                    for att in stadium:
                        temp.append(att)
                    matches.append(temp)
                    matched = True
                    break
                else:
                    print(game1)
        if not matched:
            noMatch.append(game1)



    write_to_csv("concatenatedGames.csv",[header1,header2,stadiumHeaders], matches)
    write_to_csv("noMatches.csv", header1, noMatch)
    print(len(games1))
    print(len(games2))
    print(len(matches))


