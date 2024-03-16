from listCara import allCara


def checkDefName(playerName: str, defName: str):
    if defName not in allCara:
        raise Exception(f"{defName} du joueur {playerName} n'est pas un défenseur valide !!!")


def checkIsGoodDefs(listMetaDef):
    errorMessage = ""
    for defName in listMetaDef:
        if defName not in allCara:
            errorMessage += f"{defName} de la liste meta n'est pas un défenseur valide !!! "
    if errorMessage:
        raise Exception(errorMessage)
