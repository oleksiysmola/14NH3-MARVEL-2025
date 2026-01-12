import pandas as pd
from pandarallel import pandarallel
import math
import numpy as np
pandarallel.initialize(progress_bar=True)


statesFileColumns = ["i", "E", "g", "J", "weight", "p", "Gamma", "Nb", "n1", "n2", "n3", "n4", "l3", "l4", "inversion", "J'", "K", "pRot", "v1", "v2", "v3", "v4", "v5", "v6", "GammaVib", "Calc"]
states = pd.read_csv("../14N-1H3__CoYuTe.states", delim_whitespace=True, names=statesFileColumns)

states = states[states["J"] == 19]
states = states[states["K"] == 19]
states = states[states["Gamma"] == 6]
states = states[states["n1"] == 0]
states = states[states["n2"] == 1]
states = states[states["n3"] == 0]
states = states[states["n4"] == 0]
states = states[states["l3"] == 0]
states = states[states["l4"] == 0]
states = states[states["inversion"] == 0]
print(states.head(5).to_string(index=False))
