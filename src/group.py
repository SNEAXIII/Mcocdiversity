from random import choice
from itertools import product
from src.player import Player


class Group:
    def __init__(self, current_id: int, list_meta_defs: list):
        self.id = current_id
        self.list_meta_defs = list_meta_defs
        self.g_score = 0
        self.all_defs = {}
        self.selected_defs = set()
        self.unselected_defs = set()
        self.all_player: dict = {}
        self.all_ranks = \
            {
                "7r3": 326,
                "6r6": 265,
                "7r2": 264,
                "6r5": 217,
                "7r1": 210,
                "6r4": 188,
                "6r3": 164,
                "6r2": 138,
                "6r1": 100
            }

        self.range_rank = self.all_ranks.values()

    def get_score(self):
        return int(self.g_score / 30)

    def dump(self):
        string_return = ""
        for def_name in self.all_defs:
            string_return += f"{def_name}\n"
            for int_rank in self.all_defs[def_name]:
                string_return += f"{self.convert_rank_int_to_str(int_rank)}-->{self.all_defs[def_name][int_rank]}\n"
            string_return += "\n"
        return string_return

    def __str__(self):
        string_return = f"Puissance théorique du groupe : {self.get_score()}\n"
        for player in self.all_player.values():
            string_return += player.dump()
        return string_return + (f"Les défenseurs choisis sont : {self.str_all_def_selected()}\n"
                                f"Les défenseurs non choisis sont : {self.str_all_def_un_selected()}\n")

    def str_all_def_selected(self):
        sorted_selected_def = sorted(self.selected_defs, key=lambda x: (-x[1], x[0]))
        sorted_selected_def_format = [
            f"{_def[0]} {self.convert_rank_int_to_str(_def[1])}"
            for _def in sorted_selected_def
        ]

        return ", ".join(sorted_selected_def_format)

    def str_all_def_un_selected(self):
        return ", ".join(sorted(list(self.unselected_defs)))

    def add_player(self, player: Player):
        self.all_player[player.name] = player

    def add_new_def(self, owner: str, def_name: str, rank: str, sig: int):
        if def_name not in self.all_defs:
            if (
                    any(tuple_def[0] == def_name for tuple_def in self.selected_defs) or
                    len(self.all_player[owner].defs) == 5
            ):
                return
            self.all_defs[def_name] = {}
        id_rank = self.convert_rank_str_to_int(rank)
        one_def = self.all_defs[def_name]
        if id_rank not in one_def:
            one_def[id_rank] = {}
        def_name_def_rank = one_def[id_rank]
        if sig not in def_name_def_rank:
            def_name_def_rank[sig] = set()
        def_name_def_rank[sig].add(owner)

    def convert_rank_str_to_int(self, rank: str):
        lower_rank = rank.lower()
        if lower_rank not in self.all_ranks:
            raise ValueError(f"Le rang est mal saisi : {rank}")
        return self.all_ranks[lower_rank]

    def convert_rank_int_to_str(self, value: int):
        for str_rank, int_rank in self.all_ranks.items():
            if value == int_rank:
                return str_rank
        raise IndexError(f"Aucun rang correspond trouvée pour la valeur : {value}")

    def find_the_player_for_rank_for_def(self, def_name: str, rank: int):
        if def_name not in self.all_defs:
            return False
        dict_def_rank = self.all_defs[def_name].get(rank, None)
        if dict_def_rank:
            max_sig = max(dict_def_rank.keys())
            return choice(list(dict_def_rank[max_sig]))
        return False

    @staticmethod
    def is_def_rank_empty(dictionary: dict):
        return all(not bool(s) for s in dictionary.values())

    def find_the_best_defs(self):
        all_ranks = self.all_ranks.values()
        list_all_defs = tuple(product(self.list_meta_defs, all_ranks)) + tuple(product(list(self.all_defs), all_ranks))
        for def_name, rank in list_all_defs:
            if player_or_false := self.find_the_player_for_rank_for_def(def_name, rank):
                self.add_def_in_player(player_or_false, def_name, rank)

    # todo refactor cette bouse avec des bools
    def check_doublons(self):
        number_of_doublons = 0
        for tuple_def in self.all_defs.items():
            count = 0
            print_name = True
            string_to_print = ""
            for tuple_rank in sorted(tuple_def[1].items(), key=lambda x: x[0], reverse=True):
                count_for_rank = 0
                list_player_for_a_rank = []
                for tuple_sig in tuple_rank[1].items():
                    set_players = tuple_sig[1]
                    count_for_sig = len(set_players)
                    if count_for_sig:
                        count_for_rank += count_for_sig
                        list_player_for_a_rank += [f"{player} [{tuple_sig[0]}]" for player in set_players]
                count += count_for_rank
                if count_for_rank > 0:
                    line_to_print = ", ".join(list_player_for_a_rank)
                    string_to_print += f"  --> {self.convert_rank_int_to_str(tuple_rank[0])} --> {line_to_print}\n"
            if count > 1:
                if print_name:
                    print(tuple_def[0])
                    print_name = False
                number_of_doublons +=1
                print(string_to_print)
        if number_of_doublons:
            print(f"Il y a {number_of_doublons} doublons non déterminés !!!")

    def add_def_in_player(self, player: str, def_name: str, rank: int):
        if not any(tuple_def[0] == def_name for tuple_def in self.selected_defs):
            self.selected_defs.add((def_name, rank))
        else:
            raise IndexError(f"Le défenseur {def_name} à été enregistré 2 fois")

        if len(self.all_player[player].defs) == 4:
            selected_def = None
        else:
            selected_def = def_name
        self.all_player[player].defs.append(f"{def_name} {self.convert_rank_int_to_str(rank)}")
        self.g_score += rank
        self.all_player[player].p_score += rank
        self.delete_one_def_dict(def_name)
        self.delete_one_player_in_defs_dict(player, selected_def)

    def delete_one_def_dict(self, def_name: str):
        if def_name in self.all_defs:
            del self.all_defs[def_name]

    def delete_one_player_in_defs_dict(self, player: str, def_to_update: str = None):
        for def_name, ranks in list(self.all_defs.items()):

            if def_to_update and def_to_update != def_name: continue

            for rank, all_sig in list(ranks.items()):

                for sig, names in list(all_sig.items()):

                    if player in names:
                        names.discard(player)
                        if not names:
                            del all_sig[sig]
                        if not all_sig:
                            del ranks[rank]

            if not ranks:
                self.unselected_defs.add(def_name)
                self.delete_one_def_dict(def_name)

    def is_empty_def(self):
        return not bool(self.all_defs)

    def is_full_of_def(self):
        return len(self.selected_defs) == 50
