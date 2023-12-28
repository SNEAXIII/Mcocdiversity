from pygsheets import authorize
import groups
import pandas as pd


# wks.set_dataframe(df, (1, 1))

# print (wks.get_as_df())
def getSheets():
    connection = authorize(service_file='private/client_secret.json')
    return connection.open('Test Mcoc Diversity')


def updateGroups(groups):
    for id, group in groups.groups.items():
        updateOneGroup(group, id)


def updateOneGroup(group, id):
    getSheets()[id-1].update_col(1, f"{group}".split("\n"))

