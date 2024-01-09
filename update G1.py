from src.groups import *
from connector import *
from time import time
debut = time()

groups = Groups()
groups.executeOneGroup(1,True)

connector = Connection()
connector.updateOneGroup(groups.groups[1],1)
print(f"Il a fallut {round(time() - debut)} secondes")
