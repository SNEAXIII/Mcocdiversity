from src.groups import *
from connector import *
from time import time
debut = time()

groups = Groups()
groups.execute_one_group(2, False)

connector = Connection("Gold Mcoc Planning Sheet")
connector.update_one_group(groups.groups[2], 2)
print(f"Il a fallut {round(time() - debut)} secondes")
