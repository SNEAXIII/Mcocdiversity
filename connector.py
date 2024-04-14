from pygsheets import authorize, HorizontalAlignment

from src.group import Group

class Connection:
    def __init__(self, sheet_to_open:str):
        sheets = self.get_sheets(sheet_to_open)
        self.url = sheets.url
        self.sheets = [sheets[0], sheets[1], sheets[2]]

    def get_sheets(self, sheet_to_open:str):
        connection = authorize(service_file='private/client_secret.json')
        return connection.open(sheet_to_open)

    def print_sheets_url(self):
        print(f"Lien vers les sheets:\n{self.url}")

    def print_one_sheet_url(self, worksheet):
        print(f"Lien vers le sheet:\n{worksheet.spreadsheet.url}")

    def update_groups(self, groups):
        for id, group in groups.groups.items():
            self.update_one_group(group, id, False)
        self.print_sheets_url()

    def update_one_group(self, group:Group, id, print_url=True):
        worksheet = self.sheets[id - 1]
        allplayer = list(group.all_player.values())
        offsety = 3
        offsetx = 2
        eol = "\n"
        for x in range(5):
            try:
                def_p1 = allplayer[x * 2]
                player1 = f"{def_p1}{(5 - len(def_p1.defs)) * eol}".split(eol)
            except:
                player1 = ["vide"] * 7 + [""] * 2
            try:
                def_p2 = allplayer[x * 2 + 1]
                player2 = f"{def_p2}{(5 - len(def_p2.defs)) * eol}".split(eol)
            except:
                player2 = ["vide"] * 7 + [""] * 2
            to_print = player1 + player2
            worksheet.update_col(offsetx + x,
                                 to_print,
                                 offsety)

        cell_b2 = worksheet.cell("b2")
        cell_b2.value = f"Groupe {id} → puissance de groupe estimée : {group.get_score()}"
        cell_b2.set_horizontal_alignment(HorizontalAlignment.CENTER)
        cell_b2.update()

        cell_b21 = worksheet.cell("b21")
        cell_b21.value = f"Les défenseurs choisis sont : {group.str_all_def_selected()}"
        cell_b21.wrap_strategy = "WRAP"
        cell_b21.update()

        cell_b22 = worksheet.cell("b22")
        cell_b22.value = f"Les défenseurs non choisis sont : {group.str_all_def_un_selected()}"
        cell_b22.wrap_strategy = "WRAP"
        cell_b22.update()

        print(f"____________________\nGroupe numéro {id} finis")
        if print_url:
            self.print_one_sheet_url(worksheet)
