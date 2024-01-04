from listCara import allCara


def checkDefName(playerName: str, defName: str):
    if defName not in allCara:
        raise Exception(f"{defName} du joueur {playerName} n'est pas un défenseur valide !!!")
