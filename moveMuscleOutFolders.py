import os
import shutil

for folder in os.listdir("muscle_output/"):
    shutil.copytree(os.path.join("muscle_output", folder), os.path.join("temp", folder, "muscle_output"))
    break

