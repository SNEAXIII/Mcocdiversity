class Player:
    def __init__(self, name: str):
        self.name = name
        self.defs = []


class Group:
    def __init__(self):
        self.allDefs = {}
        self.selectDefs = {}
        self.allPlayer = {}
        self.allRanks = \
            {
                "7r3": 8,
                "7r2": 7,
                "7r1": 6,
                "6r6": 7,
                "6r5": 5,
                "6r4": 4,
                "6r3": 3,
                "6r2": 2,
                "6r1": 1
            }

    def addPlayer(self, player: Player):
        self.allPlayer[player.name] = player

    def addNewDef(self, owner: str, defName: str, rank: str, sig: int):
        if defName not in self.allDefs:
            self.allDefs[defName]={}
            for x in range(max(self.allRanks.values()), min(self.allRanks.values()) - 1, -1):
                self.allDefs[defName][x] = {}
        self.allDefs[defName][self.convertRank(rank)][owner] = sig

    def convertRank(self, rank: str):
        if not rank in self.allRanks:
            raise Exception(f"Le rang est mal saisi : {rank}")
        return self.allRanks[rank]

    # todo find le best rank pour un persos dans un groupe


class Groups:
    def __init__(self):
        self.groups = {1: Group(), 2: Group(), 3: Group()}

    def addPlayerToAGroup(self, idGroup: int, playerName: str):
        if len(self.groups[idGroup].allPlayer) != 10:
            self.groups[idGroup].addPlayer(Player(playerName))
            return
        raise Exception(f"Il ne peux pas y avoir plus de 10 joueurs dans le groupe {idGroup}!!!")

    def addDefToAGroup(self, idGroup: int, playerName: str, defName: str, rank: str, sig: int):
        self.groups[idGroup].addNewDef(playerName,defName,rank,sig)


groups = Groups()

# groups.addPlayerToAGroup(1, "Mrbal'")
# groups.addPlayerToAGroup(1, "Legacy'")
# groups.addDefToAGroup(1,"Mrbal'","Shuri","7r3",0)
# groups.addDefToAGroup(1,"Mrbal'","Absman","6r6",200)
# groups.addDefToAGroup(1,"Legacy'","Shuri","7r3",0)

with open("data", encoding="utf-8") as f:
    data = [line.replace("\n", "") for line in f.readlines()]

for line in data:
    if line == "#":
        playerName = None
        group = None
    elif line.startswith("+"):
        if playerName is not None:
            raise Exception("Le joueur ne peux être saisi 2 fois")
        playerName = line.lstrip("+")
    elif line.startswith("-"):
        if playerName is None:
            raise Exception("Le joueur doit être saisi avant son groupe")
        elif group is not None:
            raise Exception("Le groupe ne peux être saisi 2 fois")
        group = int(line.lstrip("-"))
        print(playerName, group)
        groups.addPlayerToAGroup(group,playerName)
    else:
        # todo erreur potancielle ici
        # defName,rank,sig = line.split(" ")
        groups.addDefToAGroup(group,playerName,*line.split(" "))
a = "test"
