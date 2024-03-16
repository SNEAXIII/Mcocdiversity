from listCara import allCara


def check_def_name(playerName: str, defName: str):
    if defName not in allCara:
        raise Exception(f"{defName} du joueur {playerName} n'est pas un défenseur valide !!!")


def check_is_good_defs(listMetaDef):
    errorMessage = ""
    for defName in listMetaDef:
        if defName not in allCara:
            errorMessage += f"{defName} de la liste meta n'est pas un défenseur valide !!! "
    if errorMessage:
        raise Exception(errorMessage)
