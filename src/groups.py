from src.group import Group
from src.player import Player
from src.utils import checkDefName


class Groups:
    def __init__(self):
        self.groups = {1: Group(1), 2: Group(2), 3: Group(3)}

    def addPlayerToAGroup(self, idGroup: int, playerName: str):
        if len(self.groups[idGroup].allPlayer) != 10:
            self.groups[idGroup].addPlayer(Player(playerName))
            return
        raise Exception(f"Il ne peux pas y avoir plus de 10 joueurs dans le groupe {idGroup}!!!")

    def addDefToOneGroup(self, idGroup: int, playerName: str, defName: str, rank: str, sig: int = 0):
        self.groups[idGroup].addNewDef(playerName, defName, rank, int(sig))

    def dump(self):
        for id, group in self.groups.items():
            print(f"Groupe numéro {id}\n{group}")

    def loadData(self, fileToOpen: str = "./data/data.txt"):
        with open(fileToOpen, encoding="utf-8") as f:
            data = [line.replace("\n", "") for line in f.readlines()]
        playerName = None
        group = None
        resetIdentifier = "//"
        playerIdentifier = ">"
        groupIdentifier = "Groupe "
        forceIdentifier = "!"
        commentaryIdentifier = "*"
        for line in data:
            if line == resetIdentifier:
                playerName = None
                group = None
            elif line.startswith(commentaryIdentifier):
                pass
            elif line.startswith(playerIdentifier):
                if playerName is not None:
                    raise Exception("Le joueur ne peux être saisi 2 fois")
                playerName = line.lstrip(playerIdentifier)
            elif line.startswith(groupIdentifier):
                if playerName is None:
                    raise Exception("Le joueur doit être saisi avant son groupe")
                elif group is not None:
                    raise Exception("Le groupe ne peux être saisi 2 fois")
                group = int(line.lstrip(groupIdentifier))
                self.addPlayerToAGroup(group, playerName)
            elif line.startswith(forceIdentifier):
                selectedGroup = self.groups[group]
                lineWhithoutIdentifier = line.lstrip(forceIdentifier)
                defName, strRank, strSig = lineWhithoutIdentifier.split(" ")
                checkDefName(playerName, defName.capitalize())
                selectedGroup.addDefInPlayer(playerName, defName.capitalize(),
                                             selectedGroup.convertRankStrToInt(strRank))
            else:
                rawData = line.split(" ")
                if len(rawData) != 3:
                    raise Exception(f"La ligne {rawData} du joueur {playerName} est mal écrite")
                defName, strRank, strSig = rawData
                checkDefName(playerName, defName.capitalize())
                self.addDefToOneGroup(group, playerName, defName.capitalize(), strRank, int(strSig))

    def executeAllGroups(self):
        for numGroup in range(1, 4):
            # todo print(debug)
            self.executeOneGroup(numGroup)


    def executeOneGroup(self, numGroup: int,load :bool= False):
        if load:
            # todo voir pour load un seul groupe
            self.loadData()
        group = self.groups[numGroup]
        print(f"____________________\nTraitement groupe {group.id}")
        group.checkdoublons()
        group.findTheBestDefs()

    def doEverything(self):
        self.loadData()
        self.executeAllGroups()
        # todo self.check()

# todo ajouter un check si il y a bien 10 membres par groupe
# todo ajouter un check si il y a bien 5 defenseurs par personne
# todo faire une méthode pour process tout les groupes
