import os

with open("All_Results.txt", "w") as outFile:
    outFile.write("Bacteria\tStrains\tElapsed Time\twatsThetaS\twatsTheta\tpiS\tpi\n")
    for specLabel in os.listdir("final_output/"):
        outStr = specLabel
        if os.path.exists("final_output/" + specLabel + "/Process_Time.txt"):
            with open("final_output/" + specLabel + "/Process_Time.txt") as readMe:
                outStr += "\t" + readMe.readlines()[1].strip().replace("Strains: ", "")
        else:
            outStr += "\tUnfound\tUnfound"
        if os.path.exists("final_output/" + specLabel + "/Results.txt"):
            with open("final_output/" + specLabel + "/Results.txt") as readMe:
                arr = readMe.readlines()[0].strip().split("\t")
                outStr += "\t" + arr[5] + "\t" + arr[6] + "\t" + arr[7] + "\t" + arr[8]
        else:
            outStr += "\tUnfound\tUnfound\tUnfound\tUnfound\tUnfound\tUnfound"
        outFile.write(outStr + "\n")

countSuccesses = 0
countFails = 0
with open("All_Successful_Results.txt", "w") as outFile:
    with open("All_Results.txt", "r") as readMe:
        for line in readMe.readlines():
            if not "-1\t-1\t-1\t-1\t-1\t-1" in line and not "\tUnfound\tUnfound\tUnfound\tUnfound\tUnfound\tUnfound" in line:
                outFile.write(line.strip() + "\n")
                countSuccesses += 1
            else:
                countFails += 1

print("Successes: " + str(countSuccesses) + "\nFails: " + str(countFails) + "\nFailure Rate: " + str(countFails / float(countSuccesses + countFails)))

