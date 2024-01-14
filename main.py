from src.groups import *
from connector import *
from time import time
debut = time()

groups = Groups()
groups.doEverything()

connector = Connection("Gold Mcoc Planning Sheet")
connector.updateGroups(groups)
print(f"Il a fallut {round(time() - debut)} secondes")
