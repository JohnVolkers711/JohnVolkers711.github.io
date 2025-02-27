import csv
import numpy as np
import matplotlib.pyplot as plt

def readCsv(filename):
    with open(filename, mode="r", newline="") as file:
        reader = csv.reader(file)
        header = next(reader)

        print(header)

        data = []
        for row in reader:
            temp = [row[0], row[1], row[2], row[3], row[4], row[5]]
            data.append(temp)

        return data

def createHistogram(title, data):
    min = 0
    max = 0
    for runs in data:
        if runs < min:
            min = runs
        if runs > max:
            max = runs

    # Create a histogram
    plt.figure(figsize=(8, 5))
    bins = np.arange(min, max + 2)  # Ensures each bin is exactly width 1
    plt.hist(data, bins=bins, edgecolor='black', alpha=0.7)

    # Highlight potential outliers (values far from the mean)
    mean = np.mean(data)
    print("Mean runs = "+str(mean))
    std_dev = np.std(data)
    outlier_threshold = 2.5 * std_dev  # Change threshold if needed
    print("Threshold : "+str(outlier_threshold))

    # Identify and mark outliers
    outlier_values = [x for x in data if abs(x - mean) > outlier_threshold]
    for outlier in outlier_values:
        plt.axvline(outlier, color='red', linestyle='dashed', label=f'Outlier: {outlier}')

    # Labels and title
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title(title)
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1))  # Moves legend outside
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    print("Number of outliers = " + str(len(outlier_values)))
    # Show plot
    plt.show()


if __name__ == "__main__":
    games1 = readCsv("mlbGames.csv")
    games2 = readCsv("mlbGames2.csv")

    matches = 0
    missingValuesInGames1 = []
    missingValuesInGames2 = []

    for game1 in games1:
        if game1[1] == "" or game1[2] == "" or game1[3] == "" or game1[4] == "" or game1[5] == "":
            missingValuesInGames1.append(game1)
            continue

        for game2 in games2:
            if game1[1] == game2[1] and game1[2] == game2[2] and game1[3] == game2[3] and game1[4] == game2[4] and game1[5] == game2[5]:
                matches = matches + 1
                break

    # Find any null values in mlbGames2.csv
    for game in games2:
        if game[1] == "" or game[2] == "" or game[3] == "" or game[4] == "" or game[5] == "":
            missingValuesInGames2.append(game[0])

    print("Games in CSV 1: "+str(len(games1)))
    print("Games in CSV 2: "+str(len(games2)))
    print("Data Matches: "+str(matches))
    print("Null Values in CSV 1: "+ str(len(missingValuesInGames1)))
    missingAvg = 0
    if len(missingValuesInGames1) > 0:
        for game in missingValuesInGames1:
            print(game)
            for i in range(len(game)):
                if game[i] == "":
                    missingAvg += 1

            # print(missingValuesInGames1[len(missingValuesInGames1)-1-i])
    print("Avg missing attributes in CSV 1: "+str(missingAvg/len(missingValuesInGames1)))
    print("Null Values in CSV 2: "+ str(len(missingValuesInGames2)))
    if len(missingValuesInGames2) > 0:
        for i in range(10):
            print(missingValuesInGames1[len(missingValuesInGames2)-1-i])

    nonNullGames1 = []
    nonNullGames2 = []
    if len(missingValuesInGames1) > 0:
        for game in games1:
            if not missingValuesInGames1.__contains__(game[0]):
                nonNullGames1.append(game)
    else:
        nonNullGames1 = games1.copy()
    if len(missingValuesInGames2) > 0:
        for game in games2:
            if not missingValuesInGames2.__contains__(game[0]):
                nonNullGames2.append(game)
    else:
        nonNullGames2 = games2.copy()

    runsCombined = []
    homeTeamRuns = []
    awayTeamRuns = []
    for game in nonNullGames1:
        runsCombined.append(int(game[3]))
        homeTeamRuns.append(int(game[3]))
        runsCombined.append(int(game[5]))
        awayTeamRuns.append(int(game[5]))
    for game in nonNullGames2:
        runsCombined.append(int(game[3]))
        homeTeamRuns.append(int(game[3]))
        runsCombined.append(int(game[5]))
        awayTeamRuns.append(int(game[5]))


    createHistogram("Histogram of Runs Scored in a Game", runsCombined)
    createHistogram("Runs Scored by Home Team", homeTeamRuns)
    createHistogram("Runs Scored by Away Team", awayTeamRuns)

