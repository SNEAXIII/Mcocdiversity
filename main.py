class Player:
    def __init__(self, name: str):
        self.name = name
        self.defs = []


class Group:
    def __init__(self):
        self.allDefs = {}
        self.selectDefs = []
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
        self.rangeRank = max(self.allRanks.values()), min(self.allRanks.values()) - 1, -1

    def __str__(self):
        stringReturn = ""
        for defName in self.allDefs:
            stringReturn += defName + "\n"
            for intRank in self.allDefs[defName]:
                stringReturn += f"{self.convertRankIntToStr(intRank)}-->{self.allDefs[defName][intRank]}" + "\n"
            stringReturn += "\n"
        return stringReturn

    def addPlayer(self, player: Player):
        self.allPlayer[player.name] = player

    def addNewDef(self, owner: str, defName: str, rank: str, strSig: str):
        sig = int(strSig)
        if defName not in self.allDefs:
            self.allDefs[defName] = {}
            for idRank in range(*self.rangeRank):
                self.allDefs[defName][idRank] = {}
        defNameDefRank = self.allDefs[defName][self.convertRankStrToInt(rank)]
        if not sig in defNameDefRank:
            defNameDefRank[sig] = set()
        defNameDefRank[sig].add(owner)

    def convertRankStrToInt(self, rank: str):
        if not rank in self.allRanks:
            raise Exception(f"Le rang est mal saisi : {rank}")
        return self.allRanks[rank]

    def convertRankIntToStr(self, value: int):
        for strRank, intRank in self.allRanks.items():
            if value == intRank:
                return strRank
        raise Exception(f"Aucun rang correspond trouvée pour la valeur : {value}")

    def countTheRankForDef(self, defName: str, rank: int):
        dictDefRank = self.allDefs[defName][rank]
        if len(dictDefRank):
            maxSig = max(dictDefRank.keys())
            dictPlayerForASig = dictDefRank[maxSig]
            if len(dictPlayerForASig) == 1:
                return next(iter(dictPlayerForASig))
            else:
                print(f"il y a plusieurs candidats pour {defName} au rang {rank}")
        return False

    def findThePlayerForRankForDef(self, defName: str, rank: int):
        print(len(self.allDefs[defName][rank]))

    @staticmethod
    def isDefRankEmpty(dictionary: dict):
        return all(not bool(s) for s in dictionary.values())

    def findTheBestDefs(self, force: bool = False):
        # implétementer le force
        for rank in self.allRanks.values():
            doublon = False
            # todo gerer les doublons
            # todo mettre une while tant qu'il y a des persos a supprimer
            for defName in self.allDefs:
                nameOrFalse = self.countTheRankForDef(defName, rank)
                if nameOrFalse:
                    self.addDefInPlayer(nameOrFalse,defName)
                    continue
                    # todo décrementer un indice si ya rien a suppr
                print(defName, rank)

            # todo addmultidelete here

    def addDefInPlayer(self,player:str,defName:str):
        self.allPlayer[player].defs.append(defName)
        if not defName in self.selectDefs:
            self.selectDefs.append(defName)
        else:
            raise Exception(f"Le défenseur {defName} à été enregistré 2 fois")
        # Si la personne a 5 defs on la retire des choix de defenseur
        if len(self.allPlayer[player].defs) == 5:
            selectedDef = None
        else:
            selectedDef = defName
        self.deleteAPlayerInDefsDict(player,selectedDef)

    def deleteADefsDict(self, defName: str):
        del self.allDefs[defName]

    def deleteMultiDefsDict(self, listDefName: list):
        # todo probablement useless
        for defName in listDefName:
            self.deleteADefsDict(defName)

    def deleteAPlayerInDefsDict(self, player: str,defToUpdate : str = None):
        for _def, ranks in list(self.allDefs.items()):
            if defToUpdate:
                if defToUpdate != _def:
                    continue
            for rank, allSig in list(ranks.items()):
                for sig, names in list(allSig.items()):
                    try:
                        # todo faire en sorte de supprimer soit le nom sur un seul persos soit sur tous
                        names.discard(player)
                        if not names:
                            del allSig[sig]
                        if self.isDefRankEmpty(allSig):
                            del self.allDefs[_def]
                    except KeyError:
                        pass

    # todo lors de la suppression d'un player dans les defenseurs, vérifier si il en reste un et l'ajouter a ses defs
    # todo verifier qu'il y a un seul et unique def par groupe


class Groups:
    def __init__(self):
        self.groups = {1: Group(), 2: Group(), 3: Group()}

    def addPlayerToAGroup(self, idGroup: int, playerName: str):
        if len(self.groups[idGroup].allPlayer) != 10:
            self.groups[idGroup].addPlayer(Player(playerName))
            return
        raise Exception(f"Il ne peux pas y avoir plus de 10 joueurs dans le groupe {idGroup}!!!")

    def addDefToAGroup(self, idGroup: int, playerName: str, defName: str, rank: str, sig: int):
        self.groups[idGroup].addNewDef(playerName, defName.capitalize(), rank, sig)

    def dump(self):
        for id, group in self.groups.items():
            print(f"Groupe numéro {id}\n{group}")


groups = Groups()

# groups.addPlayerToAGroup(1, "Mrbal'")
# groups.addPlayerToAGroup(1, "Legacy'")
# groups.addDefToAGroup(1,"Mrbal'","Shuri","7r3",0)
# groups.addDefToAGroup(1,"Mrbal'","Absman","6r6",200)
# groups.addDefToAGroup(1,"Legacy'","Shuri","7r3",0)

with open("data2", encoding="utf-8") as f:
    data = [line.replace("\n", "") for line in f.readlines()]
playerName = None
group = None
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
        groups.addPlayerToAGroup(group, playerName)
    else:
        # todo erreur potancielle ici
        # defName,rank,sig = line.split(" ")
        groups.addDefToAGroup(group, playerName, *line.split(" "))

# groups.groups[1].countTheRankForDef("Shuri", 8)
# groups.groups[1].deleteAPlayerInDefsDict("LEGACY LEGION")
# groups.groups[1].deleteAPlayerInDefsDict("Mrbal'")

# groups.groups[1].findTheBestDefs()

print(groups.groups[1].countTheRankForDef("Shuri", 8))
groups.groups[1].addDefInPlayer("Mrbal'","Shuri")
groups.groups[1].addDefInPlayer("Mrbal'","IDoom")
groups.dump()
a = "test"
