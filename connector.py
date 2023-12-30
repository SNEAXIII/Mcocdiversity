from pygsheets import authorize
import groups
import pandas as pd


# wks.set_dataframe(df, (1, 1))

# print (wks.get_as_df())

class Connection:
    def __init__(self):
        sheets = self.getSheets()
        self.sheets = [sheets[0], sheets[1], sheets[2]]

    def getSheets(self):
        connection = authorize(service_file='private/client_secret.json')
        return connection.open('Gold Mcoc Diversity')

    def updateGroups(self, groups):
        for id, group in groups.groups.items():
            self.updateOneGroup(group, id)

    def updateOneGroup(self, group, id):
        worksheet = self.sheets[id-1]
        allplayer = list(group.allPlayer.values())
        offsety = 3
        offsetx = 2
        for x in range(5):
            try:
                player1 = f"{allplayer[x * 2]}".split("\n")
            except:
                player1 = ["vide"] * 7 + [""] * 2
            try:
                player2 = f"{allplayer[x * 2 + 1]}".split("\n")
            except:
                player2 = ["vide"] * 7 + [""] * 2
            toPrint = player1 + player2
            worksheet.update_col(offsetx + x,
                                 toPrint,
                                 offsety)

        cell_b2 = worksheet.cell("b2")
        cell_b2.value = f"Groupe {id} → puissance de groupe estimée : {group.getScore()}"
        cell_b2.update()

        cell_b21 = worksheet.cell("b21")
        cell_b21.value = f"Les défenseurs choisis sont : {group.strAllDefSelected()}"
        cell_b21.update()

        cell_b22 = worksheet.cell("b22")
        cell_b22.value = f"Les défenseurs non choisis sont : {group.strAllDefUnSelected()}"
        cell_b22.update()

        print(f"Groupe numéro {id} finis")
