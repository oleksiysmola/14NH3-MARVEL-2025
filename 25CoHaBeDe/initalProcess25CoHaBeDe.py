import pandas as pd
from pandarallel import pandarallel
import math
import numpy as np
pandarallel.initialize(progress_bar=True)


columns = ["PQR", "nu", "S", "gamma1", "gamma2"]

df = pd.read_csv("25CoHaBeDe-raw.txt", names=columns, delim_whitespace=True)
df = df[["PQR", "nu"]]
df["point"] = [i + 1 for i in range(len(df))]
print(df.to_string(index=False, header=False))


marvelColumns = ["nu1", "nu2", "nu3", "nu4", "L3", "L4", "J", "K", "inv", "Gamma", "Nb", "E", "Uncertainty", "Transitions"]
marvelEnergies = pd.read_csv("../CombinationDifferencesTests/14NH3-MarvelEnergies-2024.txt", delim_whitespace=True, names=marvelColumns)
# rotationalEnergies = marvelEnergies[marvelEnergies["nu1"] == 0]
# rotationalEnergies = rotationalEnergies[rotationalEnergies["nu2"] == 0]
# rotationalEnergies = rotationalEnergies[rotationalEnergies["nu3"] == 0]
# rotationalEnergies = rotationalEnergies[rotationalEnergies["nu4"] == 0]
# rotationalEnergies = rotationalEnergies[rotationalEnergies["L3"] == 0]
# rotationalEnergies = rotationalEnergies[rotationalEnergies["L4"] == 0]
# rotationalEnergies = rotationalEnergies[rotationalEnergies["inv"] == "s"]

groupMultiplicationTable = {}
# groupMultiplicationTable["A1'"] = {
#     "A1'": "A1'",
#     "A2'": "A2'",
#     "E'": "E'",
#     "A1\""
# }

mapPQR = {
    "p": -1,
    "q": 0,
    "r": 1,
}

def columnSplitter(row, marvelEnergies):
    row["unc1"] = float(row["nu"].split("(")[1][:-1])*1e-6
    if row["unc1"] < 1e-6:
        row["unc1"] += 1e-6
    row["unc2"] = row["unc1"]
    row["nu"] = row["nu"].split("(")[0]
    row["J\""] = row["PQR"].split("(")[1].split(",")[0]
    row["K\""] = row["PQR"].split("(")[1].split(",")[1].split(")")[0]
    row["J'"] = int(row["J\""])  + mapPQR[row["PQR"][1].lower()]
    row["K'"] = int(row["K\""])  + mapPQR[row["PQR"][0].lower()]
    row["inv\""] = row["PQR"][-1].lower()
    row["nu1\""] = 0 
    row["nu2\""] = 0
    row["nu3\""] = 0 
    row["nu4\""] = 0 
    row["L3\""] = 0 
    row["L4\""] = 0
    row["Nb\""] = 0
    matchingEnergies = marvelEnergies[marvelEnergies["J"] == int(row["J\""])]
    matchingEnergies = matchingEnergies[matchingEnergies["K"] == int(row["K\""])]
    matchingEnergies = matchingEnergies[matchingEnergies["inv"] == row["inv\""]]
    matchingEnergies = matchingEnergies[matchingEnergies["nu1"] == int(row["nu1\""])]
    matchingEnergies = matchingEnergies[matchingEnergies["nu3"] == int(row["nu3\""])]
    matchingEnergies = matchingEnergies[matchingEnergies["L3"] == int(row["L3\""])]
    # if  row["inv\""] == "s":
    #     row["GammaVib\""] = "A1'"
    # else:
    #     row["GammaVib\""] = "A2\""
    row["nu1'"] = 0
    row["nu2'"] = 0
    row["nu3'"] = 0
    row["nu4'"] = 0
    row["L3'"] = 0
    row["L4'"] = 0
    if 203 >= row["point"]:
        row["nu2'"] = 1
        if row["inv\""] == "a":
            row["inv'"] = "s"
        else:
            row["inv'"] = "a"
    if 523 > row["point"] > 203:
        row["nu2\""] = 1
        row["nu2'"] = 2
        if row["inv\""] == "a":
            row["inv'"] = "s"
        else:
            row["inv'"] = "a"
    elif row["point"] >= 523:
        row["nu4\""] = 1
        row["L4\""] = 1
        # if  row["inv\""] == "s":
        #     row["GammaVib\""] = "E'"
        # else:
        #     row["GammaVib\""] = "E\""
    matchingEnergies = matchingEnergies[matchingEnergies["nu2"] == int(row["nu2\""])]
    matchingEnergies = matchingEnergies[matchingEnergies["nu4"] == int(row["nu4\""])]
    matchingEnergies = matchingEnergies[matchingEnergies["L4"] == int(row["L4\""])]
    matchingEnergy = matchingEnergies.head(1).squeeze()
    if len(matchingEnergies) >= 1:
        row["Gamma\""] = matchingEnergy["Gamma"]
        row["Nb\""] = int(matchingEnergy["Nb"])
    row["Matches"] = len(matchingEnergies)
    return row

df = df.parallel_apply(lambda x:columnSplitter(x, marvelEnergies), result_type="expand", axis=1)


transitionsColumns = ["nu", "unc1", "unc2", "nu1'", "nu2'", "nu3'", "nu4'", "L3'", "L4'", "J'", "K'", "inv'", "Gamma'", "Nb'",
                      "nu1\"", "nu2\"", "nu3\"", "nu4\"", "L3\"", "L4\"", "J\"", "K\"", "inv\"", "Gamma\"", "Nb\"", "Source"]
marvelTransitions = pd.read_csv("../Marvel-14NH3-2020.txt", delim_whitespace=True, names=transitionsColumns)

def matchTransitions(row, marvelTransitions):
    matchingTransitions = marvelTransitions[marvelTransitions["J\""] == int(row["J\""])]
    matchingTransitions = matchingTransitions[matchingTransitions["K\""] == int(row["K\""])]
    matchingTransitions = matchingTransitions[matchingTransitions["inv\""] == row["inv\""]]
    matchingTransitions = matchingTransitions[matchingTransitions["nu1\""] == int(row["nu1\""])]
    matchingTransitions = matchingTransitions[matchingTransitions["nu2\""] == int(row["nu2\""])]
    matchingTransitions = matchingTransitions[matchingTransitions["nu3\""] == int(row["nu3\""])]
    matchingTransitions = matchingTransitions[matchingTransitions["nu4\""] == int(row["nu4\""])]
    matchingTransitions = matchingTransitions[matchingTransitions["L3\""] == int(row["L3\""])]
    matchingTransitions = matchingTransitions[matchingTransitions["L4\""] == int(row["L4\""])]
    matchingTransitions["Obs-Calc"] = abs(float(row["nu"]) - matchingTransitions["nu"])
    matchingTransitions = matchingTransitions.sort_values(by="Obs-Calc")
    # if len(matchingTransitions) >= 1:
    matchingTransition = matchingTransitions.head(1).squeeze()
    row["Obs-Calc"] = matchingTransition["Obs-Calc"]
    row["J'"] =  matchingTransition["J'"]
    row["K'"] =  matchingTransition["K'"]
    row["Gamma\""] = matchingTransition["Gamma\""]
    row["Nb\""] =  matchingTransition["Nb\""]
    row["Nb'"] =  matchingTransition["Nb'"]
    row["Gamma'"] = matchingTransition["Gamma'"]
    row["inv'"] = matchingTransition["inv'"]
    row["nu1'"] = matchingTransition["nu1'"]
    row["nu2'"] = matchingTransition["nu2'"]
    row["nu3'"] = matchingTransition["nu3'"]
    row["nu4'"] = matchingTransition["nu4'"]
    row["L3'"] = matchingTransition["L3'"]
    row["L4'"] = matchingTransition["L4'"]
    # if row["point"] >= 523:
            
    return row

df = df.parallel_apply(lambda x:matchTransitions(x, marvelTransitions), axis=1, result_type="expand")

df = df[["PQR", "nu", "unc1", "unc2", "nu1'", "nu2'", "nu3'", "nu4'", "L3'", "L4'", "J'", "K'", "inv'", "Gamma'", "Nb'", "nu1\"", "nu2\"", "nu3\"", "nu4\"", "L3\"", "L4\"", "J\"", "K\"", "inv\"", "Gamma\"", "Nb\"", "point", "Matches", "Obs-Calc"]]
df2 = df[df["Obs-Calc"] > 5e-2]
df = df[df["Obs-Calc"] < 5e-2]
df["Source"] = [f"25CoHaBeDe.{i+1}" for i in range(len(df))] 
df = df[["nu", "unc1", "unc2", "nu1'", "nu2'", "nu3'", "nu4'", "L3'", "L4'", "J'", "K'", "inv'", "Gamma'", "Nb'", "nu1\"", "nu2\"", "nu3\"", "nu4\"", "L3\"", "L4\"", "J\"", "K\"", "inv\"", "Gamma\"", "Nb\"", "Source"]]
selectionRules = {
    "A1'": "A1\"", # Technically the nuclear spin statistical weights of the A1 states are zero
    "A1\"": "A1'",
    "A2'": "A2\"",
    "A2\"": "A2'",
    "E'": "E\"",
    "E\"": "E'",
}

statesFileColumns = ["i", "E", "g", "J", "weight", "p", "Gamma", "Nb", "n1", "n2", "n3", "n4", "l3", "l4", "inversion", "J'", "K", "pRot", "v1", "v2", "v3", "v4", "v5", "v6", "GammaVib", "Calc"]
states = pd.read_csv("../14N-1H3__CoYuTe.states", delim_whitespace=True, names=statesFileColumns)
# states = states[states["E"] < 7000]
# states = states[states["g"] > 0]
# states = states[states["J"] == Jupper]
# states = states[states["E"] > 6500]
# print(states.to_string(index=False))
# statesList = [
#     "21CaCeBeCa.1673",
#     "21CaCeBeCa.1674"
# ]
# def findMatchingStates(row, states):
#     matchingStates = states[states["J"] == row["J'"]]
#     matchingStates = matchingStates[matchingStates["Gamma"] == row["Gamma'"]]
#     matchingStates = matchingStates[matchingStates["Nb"] == row["Nb'"]]
#     row["CoYuTe E'"] = matchingStates.squeeze()["E"]
#     return row

# transitions = transitions.parallel_apply(lambda x:findMatchingStates(x, states), axis=1, result_type="expand")
# statesFromList = transitions[transitions["Source"].isin(statesList)]
# print("Selected states with CoYuTe upper state energy:")
# print(statesFromList[["nu", "unc1", "Tag'", "Tag\"", "Source", "Average E'", "E'", "CoYuTe E'", "E\"", "Problem"]].to_string(index=False))


# processedTransitions = df.sort_values(by=["nu"])
df = df.to_string(index=False, header=False)
marvelFile = "25CoHaBeDe-Marvel.txt"
with open(marvelFile, "w+") as FileToWriteTo:
    FileToWriteTo.write(df)

inversionMap = {
    "s": 0,
    "a": 1
}
symmetryMap = {
    "A1'": 1,
    "A2'": 2,
    "E'": 3,
    "A1\"": 4,
    "A2\"": 5,
    "E\"": 6,
}
symmetryMap2 = {
    1: "A1'",
    2: "A2'",
    3: "E'",
    4: "A1\"",
    5: "A2\"",
    6: "E\"",
}
def sortUnmatched(row, states):
    # row["unc1"] = float(row["nu"].split("(")[1][:-1])*1e-6
    # if row["unc1"] < 1e-6:
    #     row["unc1"] += 1e-6
    # row["unc2"] = row["unc1"]
    # row["nu"] = row["nu"].split("(")[0]
    row["J\""] = row["PQR"].split("(")[1].split(",")[0]
    row["K\""] = row["PQR"].split("(")[1].split(",")[1].split(")")[0]
    row["J'"] = int(row["J\""])  + mapPQR[row["PQR"][1].lower()]
    row["K'"] = int(row["K\""])  + mapPQR[row["PQR"][0].lower()]
    row["inv\""] = row["PQR"][-1].lower()
    row["nu1\""] = 0 
    row["nu2\""] = 0
    row["nu3\""] = 0 
    row["nu4\""] = 0 
    row["L3\""] = 0 
    row["L4\""] = 0
    row["Nb\""] = 0
    matchingEnergies = states[states["J"] == int(row["J\""])]
    matchingEnergies = matchingEnergies[matchingEnergies["K"] == int(row["K\""])]
    matchingEnergies = matchingEnergies[matchingEnergies["inversion"] == inversionMap[row["inv\""]]]
    matchingEnergies = matchingEnergies[matchingEnergies["n1"] == int(row["nu1\""])]
    matchingEnergies = matchingEnergies[matchingEnergies["n3"] == int(row["nu3\""])]
    matchingEnergies = matchingEnergies[matchingEnergies["l3"] == int(row["L3\""])]
    # if  row["inv\""] == "s":
    #     row["GammaVib\""] = "A1'"
    # else:
    #     row["GammaVib\""] = "A2\""
    row["nu1'"] = 0
    row["nu2'"] = 0
    row["nu3'"] = 0
    row["nu4'"] = 0
    row["L3'"] = 0
    row["L4'"] = 0
    if 203 >= row["point"]:
        row["nu2'"] = 1
        if row["inv\""] == "a":
            row["inv'"] = "s"
        else:
            row["inv'"] = "a"
    if 523 > row["point"] > 203:
        row["nu2\""] = 1
        row["nu2'"] = 2
        if row["inv\""] == "a":
            row["inv'"] = "s"
        else:
            row["inv'"] = "a"
    elif row["point"] >= 523:
        row["nu4\""] = 1
        row["L4\""] = 1
        # if  row["inv\""] == "s":
        #     row["GammaVib\""] = "E'"
        # else:
        #     row["GammaVib\""] = "E\""
    matchingEnergies = matchingEnergies[matchingEnergies["n2"] == int(row["nu2\""])]
    matchingEnergies = matchingEnergies[matchingEnergies["n4"] == int(row["nu4\""])]
    matchingEnergies = matchingEnergies[matchingEnergies["l4"] == int(row["L4\""])]
    matchingEnergy = matchingEnergies.head(1).squeeze()
    if len(matchingEnergies) >= 1:
        row["Gamma\""] = symmetryMap2[matchingEnergy["Gamma"]]
        row["Nb\""] = int(matchingEnergy["Nb"])
    row["Matches"] = len(matchingEnergies)
    matchingEnergies2 = states[states["J"] == int(row["J'"])]
    matchingEnergies2 = matchingEnergies2[matchingEnergies2["K"] == int(row["K'"])]
    matchingEnergies2 = matchingEnergies2[matchingEnergies2["inversion"] == inversionMap[row["inv'"]]]
    matchingEnergies2 = matchingEnergies2[matchingEnergies2["n1"] == int(row["nu1'"])]
    matchingEnergies2 = matchingEnergies2[matchingEnergies2["n2"] == int(row["nu2'"])]
    matchingEnergies2 = matchingEnergies2[matchingEnergies2["n3"] == int(row["nu3'"])]
    matchingEnergies2 = matchingEnergies2[matchingEnergies2["n4"] == int(row["nu4'"])]
    matchingEnergies2 = matchingEnergies2[matchingEnergies2["l3"] == int(row["L3'"])]
    matchingEnergies2 = matchingEnergies2[matchingEnergies2["l4"] == int(row["L4'"])]
    matchingEnergies2 = matchingEnergies2[matchingEnergies2["Gamma"] == symmetryMap[row["Gamma'"]]]
    matchingEnergies2["Obs-Calc"] = abs(matchingEnergies2["E"] - (float(row["nu"]) + matchingEnergy["E"]))
    matchingEnergies2 = matchingEnergies2.sort_values(by="Obs-Calc")
    matchingEnergy2 = matchingEnergies2.head(1).squeeze()
    row["Nb'"] = matchingEnergy2["Nb"]
    row["Obs-Calc"] = matchingEnergy2["Obs-Calc"]
    row["Matches"] = len(matchingEnergies2)
    return row


df2 = df2.parallel_apply(lambda x:sortUnmatched(x, states), result_type="expand", axis=1)
df2["Source"] = [f"25CoHaBeDe.{i+618}" for i in range(len(df2))] 
df2 = df2[["nu", "unc1", "unc2", "nu1'", "nu2'", "nu3'", "nu4'", "L3'", "L4'", "J'", "K'", "inv'", "Gamma'", "Nb'", "nu1\"", "nu2\"", "nu3\"", "nu4\"", "L3\"", "L4\"", "J\"", "K\"", "inv\"", "Gamma\"", "Nb\"", "Source", "Obs-Calc", "Matches"]]
df2 = df2.to_string(index=False, header=False)
marvelFile = "25CoHaBeDe-Unmatched.txt"
with open(marvelFile, "w+") as FileToWriteTo:
    FileToWriteTo.write(df2)

print("\n")
print(states.head(5).to_string(index=False))