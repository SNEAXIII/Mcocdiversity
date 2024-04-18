from src.group import Group
from src.player import Player
from src.utils import check_def_name, check_is_good_defs

LINE = "____________________"
RESET_IDENTIFIER = "//"
PLAYER_IDENTIFIER = ">"
GROUP_IDENTIFIER = "->Groupe "
FORCE_IDENTIFIER = "!"
COMMENTARY_IDENTIFIER = "*"


class Groups:
    def __init__(self):
        list_meta_defs = self.get_meta_def()
        self.groups = {id_group: Group(id_group, list_meta_defs) for id_group in range(1, 4)}

    def add_player_to_a_group(self, id_group: int, player_name: str):
        if len(self.groups[id_group].all_player) != 10:
            self.groups[id_group].add_player(Player(player_name))
            return
        raise IndexError(f"Il ne peux pas y avoir plus de 10 joueurs dans le groupe {id_group}!!!")

    def add_def_to_one_group(self,
                             id_group: int,
                             player_name: str,
                             def_name: str,
                             rank: str,
                             sig: int = 0
                             ):
        self.groups[id_group].add_new_def(player_name, def_name, rank, int(sig))

    def dump(self):
        for id, group in self.groups.items():
            print(f"{LINE}\nGroupe numéro {id}\n{group}")

    def get_player_group(self, player_name: str) -> int:
        for id in self.groups.keys():
            if player_name in self.groups[id].all_player:
                return id
        raise ValueError(f"Le joueur {player_name} ne fais partie d'aucun groupe!!!")

    def get_meta_def(self):
        with open("data/metadefs.txt", encoding="utf-8") as file:
            to_return = [line.strip('\n') for line in file.readlines()]
        check_is_good_defs(to_return)
        return to_return

    def add_all_player_to_groups(self):
        with open("data/groups.txt", encoding="utf-8") as file:
            lines = file.readlines()
        id_group = None
        for line in lines:
            if line.startswith(GROUP_IDENTIFIER):
                id_group = int(line.lstrip(GROUP_IDENTIFIER))
            else:
                self.add_player_to_a_group(id_group, line.strip('\n'))

    def load_data(self, file_to_open: str = "./data/data.txt"):
        with open(file_to_open, encoding="utf-8") as f:
            data = [line.replace("\n", "") for line in f.readlines()]
        self.add_all_player_to_groups()
        player_name = None
        group = None
        for index, line in enumerate(data):
            if line == RESET_IDENTIFIER:
                player_name = None
                group = None
            elif line.startswith(COMMENTARY_IDENTIFIER):
                pass
            elif line.startswith(PLAYER_IDENTIFIER):
                temp_name = line.lstrip(PLAYER_IDENTIFIER)
                if player_name is not None:
                    raise IndexError(f"Ligne {index + 1}: le nom de joueur {player_name} et {temp_name} ne peux être saisi 2 fois")
                player_name = temp_name
                group = self.get_player_group(player_name)
            elif line.startswith(FORCE_IDENTIFIER):
                selected_group = self.groups[group]
                line_whithout_identifier = line.lstrip(FORCE_IDENTIFIER)
                def_name, str_rank, str_sig = line_whithout_identifier.split(" ")
                check_def_name(player_name, def_name.capitalize())
                selected_group.add_def_in_player(player_name, def_name.capitalize(),
                                                 selected_group.convert_rank_str_to_int(str_rank))
            else:
                raw_data = line.split(" ")
                if len(raw_data) != 3:
                    raise ValueError(f"La ligne {index + 1} est mal écrite: {raw_data}")
                def_name, str_rank, str_sig = raw_data
                check_def_name(player_name, def_name.capitalize())
                self.add_def_to_one_group(group, player_name, def_name.capitalize(), str_rank, int(str_sig))
        print(LINE)
        for x in range(3):
            num_group = x + 1
            selected_group = self.groups[num_group].all_player
            nombre_membre = len(selected_group)
            string_group = ", ".join(selected_group)
            print(f"Le groupe {num_group} contient {nombre_membre} joueurs :\n{string_group}\n")

    def execute_all_groups(self):
        for num_group in range(1, 4):
            self.execute_one_group(num_group)

    def execute_one_group(self, num_group: int, loaded: bool = True):
        if not loaded:
            self.load_data()
        group = self.groups[num_group]
        print(f"{LINE}\nTraitement groupe {group.id}")
        group.check_doublons()
        group.find_the_best_defs()

    def do_everything(self):
        self.load_data()
        self.execute_all_groups()
