from groups import *
from connector import *
from time import time
debut = time()

groups = Groups()
groups.doEverything()

connector = Connection()
connector.updateGroups(groups)
print(f"Il a fallut {round(time() - debut)} secondes")
