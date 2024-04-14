from src.groups import *
from connector import *
from time import time
debut = time()

groups = Groups()
groups.execute_one_group(3, False)

connector = Connection("DBZ Mcoc Planning Sheet")
connector.update_one_group(groups.groups[3], 3)
print(f"Il a fallut {round(time() - debut)} secondes")
