from src.group import Group
from src.player import Player
from src.utils import checkDefName,checkIsGoodDefs

LINE = "____________________"
resetIdentifier = "//"
playerIdentifier = ">"
groupIdentifier = "->Groupe "
forceIdentifier = "!"
commentaryIdentifier = "*"


class Groups:
    def __init__(self):
        listMetaDefs = self.getMetaDef()
        self.groups = {id:Group(id,listMetaDefs) for id in range(1,4)}


    def addPlayerToAGroup(self, idGroup: int, playerName: str):
        if len(self.groups[idGroup].allPlayer) != 10:
            self.groups[idGroup].addPlayer(Player(playerName))
            return
        raise Exception(f"Il ne peux pas y avoir plus de 10 joueurs dans le groupe {idGroup}!!!")

    def addDefToOneGroup(self,
                         idGroup: int,
                         playerName: str,
                         defName: str,
                         rank: str,
                         sig: int = 0
                         ):
        self.groups[idGroup].addNewDef(playerName, defName, rank, int(sig))

    def dump(self):
        for id, group in self.groups.items():
            print(f"Groupe numéro {id}\n{group}")

    def getPlayerGroup(self, player_name: str) -> int:
        for id in self.groups.keys():
            if player_name in self.groups[id].allPlayer:
                return id
        raise ValueError(f"Le joueur {player_name} ne fais partie d'aucun groupe!!!")
    def getMetaDef(self):
        with open("data/metadefs.txt") as file:
            toReturn = [line.strip('\n') for line in file.readlines()]
        checkIsGoodDefs(toReturn)
        return toReturn

    def addAllPlayerToGroups(self):
        with open("data/groups.txt") as file:
            lines = file.readlines()
        idGroup = None
        for line in lines:
            if line.startswith(groupIdentifier):
                idGroup = int(line.lstrip(groupIdentifier))
            else:
                self.addPlayerToAGroup(idGroup, line.strip('\n'))

    def loadData(self, fileToOpen: str = "./data/data.txt"):
        with open(fileToOpen, encoding="utf-8") as f:
            data = [line.replace("\n", "") for line in f.readlines()]
        self.addAllPlayerToGroups()
        playerName = None
        group = None
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
                group = self.getPlayerGroup(playerName)
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
        print(LINE)
        for x in range(3):
            numGroup = x + 1
            selectedGroup = self.groups[numGroup].allPlayer
            nombreMembre = len(selectedGroup)
            stringGroup = ", ".join(selectedGroup)
            print(f"Le groupe {numGroup} contient {nombreMembre} joueurs :\n{stringGroup}\n")

    def executeAllGroups(self):
        for numGroup in range(1, 4):
            # todo print(debug)
            self.executeOneGroup(numGroup)

    def executeOneGroup(self, numGroup: int, loaded: bool = True, ignoreError: bool = True):
        if not loaded:
            self.loadData()
        group = self.groups[numGroup]
        print(f"{LINE}\nTraitement groupe {group.id}")
        group.checkdoublons()
        group.findTheBestDefs()

    def doEverything(self):
        self.loadData()
        self.executeAllGroups()
        # todo self.check()
