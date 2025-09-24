import pandas as pd
from pandarallel import pandarallel
pandarallel.initialize(progress_bar=True)

df = pd.read_csv("25CaCa-Edited.txt", delim_whitespace=True, dtype=str)

# Return only assigned lines
df = df[df["28"].notna()]

marvelColumns = ["nu", "unc1", "unc2", "nu1'", "nu2'", "nu3'", "nu4'", "L3'", "L4'", "J'", "K'", "inv'", "Gamma'", "Nb'",
                      "nu1\"", "nu2\"", "nu3\"", "nu4\"", "L3\"", "L4\"", "J\"", "K\"", "inv\"", "Gamma\"", "Nb\"", "Source"]

df["nu"] = df["2"]
df["unc1"] = df["29"].astype(float)
df["unc2"] = df["29"].astype(float)
df["vib'"] = df["14"]
df["J'"] = df["12"]
df["K'"] = df["13"]
df["inv'"] = df["15"]
df["Gamma'"] = df["11"].astype(str)
df["Nb'"] = df["17"]
df["vib\""] = df["21"]

df["J\""] = df["19"]
df["K\""] = df["20"]
df["inv\""] = df["22"]
df["Gamma\""] = df["18"].astype(str)
df["Nb\""] = df["24"]

def extractVibrationalQuantumNumbers(row):
    row["nu1'"] = row["vib'"][0]
    row["nu2'"] = row["vib'"][1]
    row["nu3'"] = row["vib'"][2]
    row["nu4'"] = row["vib'"][3]
    row["L3'"] = row["vib'"][4]
    row["L4'"] = row["vib'"][5]
    row["Gamma'"] = row["Gamma'"][0]
    row["nu1\""] = row["vib\""][0]
    row["nu2\""] = row["vib\""][1]
    row["nu3\""] = row["vib\""][2]
    row["nu4\""] = row["vib\""][3]
    row["L3\""] = row["vib\""][4]
    row["L4\""] = row["vib\""][5]
    row["Gamma\""] = row["Gamma\""][0]
    return row

inversionMapping = {
    "0": "s",
    "1": "a"
}

df["inv'"] = df["inv'"].map(inversionMapping)
df["inv\""] = df["inv\""].map(inversionMapping)

df = df.parallel_apply(lambda x:extractVibrationalQuantumNumbers(x), result_type="expand", axis=1)

symmetryMapping = {
    "1":"A1'",
    "2":"A2'",
    "3":"E'",
    "4":"A1\"",
    "5":"A2\"",
    "6":"E\""
}

df["Gamma'"] = df["Gamma'"].map(symmetryMapping)
df["Gamma\""] = df["Gamma\""].map(symmetryMapping)
    
df = df[["nu", "unc1", "unc2", "nu1'", "nu2'", "nu3'", "nu4'", "L3'", "L4'", "J'", "K'", "inv'", "Gamma'", "Nb'", "nu1\"", "nu2\"", "nu3\"", "nu4\"", "L3\"", "L4\"", "J\"", "K\"", "inv\"", "Gamma\"", "Nb\""]]



print(df.to_string(index=False, header=False))

df = df.reset_index()
df["Source"] = pd.DataFrame({"Source": [f"25CaCa.{i + 1}" for i in range(len(df))]})
df = df.drop("index", axis=1)
# print(df.head(15).to_string(index=False))
df = df.to_string(index=False, header=False)
marvelFile = "25CaCa-MARVEL.txt"
with open(marvelFile, "w+") as FileToWriteTo:
    FileToWriteTo.write(df)
