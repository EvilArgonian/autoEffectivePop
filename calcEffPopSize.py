import sys
import datetime

# watsTheta = 2 * (Eff. Pop. Size) * (Mut. Rate)
# Rearranged:
# (Eff. Pop. Size) = watsTheta / (2 * (Mut. Rate))
# watsTheta roughly equates to pi; watsThetaS roughly equates to piS

watsThetaS = sys.argv[1]
watsThetaN = sys.argv[2]
watsTheta = sys.argv[3]
piS = sys.argv[4]
piN = sys.argv[5]
pi = sys.argv[6]
dendropyTheta = sys.argv[7]
dendropyPi = sys.argv[8]
mutRate = sys.argv[9]
specName = sys.argv[10]
strains = -1
if len(sys.argv) > 10:
    strains = sys.argv[11]

if mutRate != "Unknown":
    effPopSizeThS = float(watsThetaS) / (2 * float(mutRate))
    effPopSizeThN = float(watsThetaN) / (2 * float(mutRate))
    effPopSizeTh = float(watsTheta) / (2 * float(mutRate))
    effPopSizePiS = float(piS) / (2 * float(mutRate))
    effPopSizePiN = float(piN) / (2 * float(mutRate))
    effPopSizePi = float(pi) / (2 * float(mutRate))
    effPopSizeDendropyTh = float(dendropyTheta) / (2 * float(mutRate))
    effPopSizeDendropyPi = float(dendropyPi) / (2 * float(mutRate))
else:
    effPopSizeThS = "Unknown"
    effPopSizeThN = "Unknown"
    effPopSizeTh = "Unknown"
    effPopSizePiS = "Unknown"
    effPopSizePiN = "Unknown"
    effPopSizePi = "Unknown"
    effPopSizeDendropyTh = "Unknown"
    effPopSizeDendropyPi = "Unknown"

currDate = datetime.datetime.now().strftime("%b%d")


with open("final_output/" + specName + "/Results.txt", "w") as f1:
    with open("consolidated_output/All_Results_" + currDate + ".txt", "a+") as f2:
        header = "Species\tNE (ThS)\tNE (ThN)\tNE (Th)\tNE (PiS)\tNE (PiN)\tNE (Pi)\tNE (DenTh)\tNE (DenPi)" \
                 "\tThetaS\tThetaN\tTheta\tPiS\tPiN\tPi\tDenTh\tDenPi\tStrains\n"
        f1.write(header)
        if not f2.read(1):  # If the file is empty, put headers in it.
            f2.write(header)
        outStr = specName + "\t" + str(effPopSizeThS) + "\t" + str(effPopSizeThN) + "\t" + str(effPopSizeTh) \
                 + "\t" + str(effPopSizePiS) + "\t" + str(effPopSizePiN) + "\t" + str(effPopSizePi) \
                 + "\t" + str(effPopSizeDendropyTh) + "\t" + str(effPopSizeDendropyPi) \
                 + "\t" + str(watsThetaS) + "\t" + str(watsThetaN) + "\t" + str(watsTheta) \
                 + "\t" + str(piS) + "\t" + str(piN) + "\t" + str(pi) \
                 + "\t" + str(dendropyTheta) + "\t" + str(dendropyPi) + "\t" + str(strains) + "\n"
        f1.write(outStr)
        f2.write(outStr)

print(specName + " calculations complete! Effective Population Size " +
      "(Using ThetaS): " + str(effPopSizeThS) + "\t(Using ThetaN): " + str(effPopSizeThN) + "\t(Using Theta): " + str(effPopSizeTh)
      + "\t(Using PiS): " + str(effPopSizePiS) + "\t(Using PiN): " + str(effPopSizePiN) + "\t(Using Pi): " + str(effPopSizePi)
      + "\t(Using DendropyTheta):" + str(effPopSizeDendropyTh) + "\t(Using DendropyPi):" + str(effPopSizeDendropyPi))

