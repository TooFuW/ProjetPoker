from os import listdir
from os.path import isfile, join
monRepertoire = __file__[:-24]
fichiers = [f for f in listdir(monRepertoire) if isfile(join(monRepertoire, f)) and f[-3:] == ".py"]

print(monRepertoire, fichiers)

print("\n\n")
count = 0

for rep in fichiers:
    file = open(monRepertoire+rep,"r",encoding="utf-8")
    count+=len(file.readlines())
    file.close()

print(count)