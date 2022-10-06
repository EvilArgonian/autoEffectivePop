import sys
import datetime

folder = sys.argv[1]
date = datetime.datetime.now()

resultsFolder = folder + '/OrthoFinder/Results_' + date.strftime("%b%d")
print(resultsFolder)
