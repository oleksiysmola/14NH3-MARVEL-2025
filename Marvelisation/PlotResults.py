import pandas as pd
from pandarallel import pandarallel
pandarallel.initialize(progress_bar=True)
import matplotlib.pyplot as plt
import scienceplots
plt.style.use('science')


plt.rcParams['axes.linewidth'] = 2

marvelEnergies = pd.read_csv("14N-1H3__MarvelAgainstStates.energies", delim_whitespace=True)
marvelEnergiesNoBootstrap = pd.read_csv("14N-1H3__MarvelAgainstStates-NoBootstrap.energies", delim_whitespace=True)

marvelEnergiesNew = marvelEnergies[marvelEnergies["Old"] == False]
marvelEnergiesOld = marvelEnergies[marvelEnergies["Old"]]
marvelEnergiesNewNoBootstrap = marvelEnergiesNoBootstrap[marvelEnergiesNoBootstrap["Old"] == False]
marvelEnergiesOldNoBootstrap = marvelEnergiesNoBootstrap[marvelEnergiesNoBootstrap["Old"]]


# energy levels plot
# fontsize=40
# plt.plot(marvelEnergiesNew["J"], marvelEnergiesNew["Em"], "b.", label="This work", markersize=20)
# plt.plot(marvelEnergiesOld["J"], marvelEnergiesOld["Em"], "r.", label="Furtenbacher et al. 2020", markersize=20)
# plt.xlim(0, 31)
# plt.ylim(-200, 17999)
# plt.xticks(fontsize=fontsize, weight="bold")
# plt.yticks(fontsize=fontsize, weight="bold")
# plt.xlabel(r"\textit{J}", fontsize=fontsize)
# plt.ylabel(r"\textit{E / hc} cm$^{-1}$", fontsize=fontsize)
# plt.legend(prop={"size": 40, "weight": "bold"}, frameon=True)
# plt.tick_params(axis='both', length=5, width=2, direction="out") 
# plt.show()

marvelEnergiesNewOneTransition = marvelEnergiesNew[marvelEnergiesNew["Transitions"] == 1]
marvelEnergiesNew = marvelEnergiesNew[marvelEnergiesNew["Transitions"] > 1]
marvelEnergiesNewOneTransitionNoBootstrap = marvelEnergiesNewNoBootstrap[marvelEnergiesNewNoBootstrap["Transitions"] == 1]
marvelEnergiesNewNoBootstrap = marvelEnergiesNewNoBootstrap[marvelEnergiesNewNoBootstrap["Transitions"] > 1]


# fontsize=40
# plt.plot(marvelEnergiesNew["Em"], marvelEnergiesNew["Uncertainty"], "b.", label="This work", markersize=20)
# plt.plot(oneTransition["Em"], oneTransition["Uncertainty"], "r.", label="This work", markersize=20)
# plt.xlim(3900, 18600)
# plt.ylim(-0.001, 0.05)
# plt.xticks(fontsize=fontsize, weight="bold")
# plt.yticks(fontsize=fontsize, weight="bold")
# plt.xlabel(r"\textbf{E/hc, cm$^{-1}$}", fontsize=fontsize)
# plt.ylabel(r"\textbf{Uncertainty, cm$^{-1}$}", fontsize=fontsize)
# # plt.yscale("log")
# plt.tick_params(axis='both', length=5, width=2, direction="out") 
# plt.show()

fontsize=40
plt.plot(marvelEnergiesNew["Em"], marvelEnergiesNew["Obs-Calc"], "b.", label="This work", markersize=20)
plt.plot(marvelEnergiesNewOneTransition["Em"], marvelEnergiesNewOneTransition["Obs-Calc"], "r.", label="This work", markersize=20)
plt.xlim(3900, 18600)
# plt.ylim(-0.001, 0.05)
plt.xticks(fontsize=fontsize, weight="bold")
plt.yticks(fontsize=fontsize, weight="bold")
plt.xlabel(r"\textit{E / hc} cm$^{-1}$", fontsize=fontsize)
plt.ylabel(r"$|$Obs-Calc$|$ /  \textit{hc} cm$^{-1}$", fontsize=fontsize)
plt.yscale("log")
plt.tick_params(axis='both', length=5, width=2, direction="out") 
plt.show()

marvelEnergiesNewOneTransition = marvelEnergiesNew[marvelEnergiesNew["Transitions"] == 1]
# plt.plot(marvelEnergiesNew["E"], marvelEnergiesNew["Uncertainty"], "b.")
# plt.plot(marvelEnergiesNewOneTransition["E"], marvelEnergiesNewOneTransition["Uncertainty"], "r.")
# plt.xlim(3700, 19000)
# plt.ylim(0, 0.05)
# plt.xticks(fontsize=fontsize)
# plt.yticks(fontsize=fontsize)
# plt.xlabel("E, cm$^{-1}$", fontsize=fontsize)
# plt.ylabel("Uncertainty, cm$^{-1}$", fontsize=fontsize)
# # plt.legend(prop={"size": 30}, frameon=True)
# plt.show()
# states = states[states["J"] <= 8] 

# Bootstrap vs no Bootstrap
# markersize=15
# plt.plot(marvelEnergiesNew["E"], marvelEnergiesNew["Uncertainty"], "b.", label="Bootstrap", markersize=markersize)
# plt.plot(marvelEnergiesNewOneTransition["E"], marvelEnergiesNewOneTransition["Uncertainty"], "b.", markersize=markersize)
# plt.plot(marvelEnergiesNewNoBootstrap["E"], marvelEnergiesNewNoBootstrap["Uncertainty"], "r.", label="No Bootstrap", markersize=markersize)
# plt.plot(marvelEnergiesNewOneTransitionNoBootstrap["E"], marvelEnergiesNewOneTransitionNoBootstrap["Uncertainty"], "r.", markersize=markersize)
# plt.xlim(3700, 19000)
# plt.ylim(9e-5)
# plt.yscale("log")
# plt.legend(fontsize=fontsize*1.3, frameon=True)
# plt.xticks(fontsize=fontsize)
# plt.yticks(fontsize=fontsize)
# plt.xlabel(r"\textit{E / hc} cm$^{-1}$", fontsize=fontsize)
# plt.ylabel(r"Uncertainty / cm$^{-1}$", fontsize=fontsize)
# # plt.legend(prop={"size": 30}, frameon=True)
# plt.show()

# marvelEnergiesNewOneTransition = marvelEnergiesNew[marvelEnergiesNew["Transitions"] == 1]
# plt.plot(marvelEnergiesNew["E"], marvelEnergiesNew["Obs-Calc"], "b.")
# plt.plot(marvelEnergiesNewOneTransition["E"], marvelEnergiesNewOneTransition["Obs-Calc"], "r.")
# plt.xlim(3700, 19000)
# plt.ylim(0, 0.05)
# plt.yscale("log")
# plt.xticks(fontsize=fontsize)
# plt.yticks(fontsize=fontsize)
# plt.xlabel("E, cm$^{-1}$", fontsize=fontsize)
# plt.ylabel(r"$|$Obs-Calc$|$, cm$^{-1}$", fontsize=fontsize)
# plt.legend(prop={"size": 30}, frameon=True)
# plt.show()
# marvelEnergiesNew = marvelEnergiesNew.to_string(index=False, header=False)
# newEnergiesFile = "MARVEL-NewEnergiesComparison-2024.states"
# with open(newEnergiesFile, "w+") as FileToWriteTo:
#     FileToWriteTo.write(marvelEnergiesNew)