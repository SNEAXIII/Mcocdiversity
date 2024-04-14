from src.groups import *
from connector import *
from time import time
debut = time()

groups = Groups()
groups.do_everything()

connector = Connection("DBZ Mcoc Planning Sheet")
connector.update_groups(groups)
print(f"Il a fallut {round(time() - debut)} secondes")
