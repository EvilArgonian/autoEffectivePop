import os
import shutil

for folder in os.listdir("muscle_output/"):
    try:
        shutil.copytree(os.path.join("muscle_output", folder), os.path.join("temp", folder, "muscle_output"))
    except Exception:
        print("Move failed for " + str(folder))

