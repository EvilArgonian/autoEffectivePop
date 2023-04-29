import random
import os
import sys
import shutil

inputFolder = "consensus_input"
category = sys.argv[1]
catPath = os.path.join(inputFolder, category)

if not os.path.exists(catPath):
    print("Category not recognized!")
    exit(1)

