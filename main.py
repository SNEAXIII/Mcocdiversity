from groups import *
from connector import *

groups = Groups()
groups.doEverything()

updateOneGroup(groups.groups[1], 1)
# print(f"{groups.groups[1]}".split("\n"))