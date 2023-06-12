import os
import shutil

for folder in os.listdir("muscle_output/"):
    success = True
    try:
        shutil.copytree(os.path.join("muscle_output", folder), os.path.join("temp", folder, "muscle_output"))
    except Exception:
        success = False

    if success:
        print(str(folder) + " completed.")
    else:
        print("Move failed for " + str(folder))

