import configparser
import numpy as np
import pprint as pp
import pandas as pd
import pytz
import requests
import json
import urllib3
from datetime import datetime
import charts

#=============================================================

#Credentials for API conection.
api_key= "abf1b05dda202ff07f6d121233e1dd76"
token = "d19e8db59bc0c7150437dc8378de59cd05d5f49439e3a471448880266f0a0aa5"

#Configuration.
urllib3.disable_warnings()
pd.set_option('display.max_colwidth', None)

#=============================================================

#Function to facilitate calling the API.
def get(url, params):
    response = requests.get(url=url, params=params, verify=False)
    if response.status_code != 200 :
        return None
    data = response.json()
    return data

#Function to add the creation date to the card.
def get_creation_dt(dt_id):
    id_trim = int(dt_id[0:8], 16)
    creation_time = datetime.fromtimestamp (id_trim)
    utc_creation_time = pytz.utc.localize(creation_time)
    return creation_time

#=============================================================

#Creating the structure.
cols_to_select = ["id", "name", "shortUrl", "idMemberCreator", "creationMethod", "prefs_permissionLevel" , "prefs_backgroundImage", "labelNames_green", "labelNames_yellow", "labelNames_orange", "labelNames_red", "labelNames_purple", "labelNames_blue", "labelNames_sky", "labelNames_lime", "labelNames_pink", "labelNames_black"]
    
cols_to_rename = ["board_id", "board_name", "board_shortUrl", "board_idMemberCreator", "board_creationMethod", "prefs_permissionLevel", "prefs_backgroundImage", "labelNames_green", "labelNames_yellow", "labelNames_orange", "labelNames_red", "labelNames_purple", "labelNames_blue", "labelNames_sky", "labelNames_lime", "labelNames_pink", "labelNames_black"]

cols_to_rename = dict(zip(cols_to_select, cols_to_rename))

url_boards = "https://api.trello.com/1/members/me/boards"

params = dict(key=api_key, token=token)
response = get(url_boards, params)

boards = pd.json_normalize(response, sep='_')
boards = boards.reindex(columns = cols_to_select, fill_value=np.nan).rename(columns=cols_to_rename)

#=============================================================

#Selecting only boards from Report Control.
boards = boards[boards['board_id'].isin(['62e1ca7080d55f4986b31e7c',   #Tablero: Administración, Gastos, Legal, Compras internas	
                                         '5e56db9de73d2004ac1d74b5',   #Tablero: Afore
                                         '6307b7208f302300595be54c',   #Tablero: CES Externo
                                         '62feec19a8d3e73be9830ef5',   #Tablero: Clientes / CAT No Cobranza
                                         '62f430f47f327b3c2495d35d',   #Tablero: Finanzas, Contabilidad
                                         '62e5d4e0eb3b591d8a1bd21e',   #Tablero: GCIA CES Interno
                                         '62e94b4852127c67213d2d57',   #Tablero: GCIA Cadena de Suministro y CEDIS
                                         '627aa5d29784d24489e46e79',   #Tablero: GCIA Comercial Muebles (Ventas, Proveedores, eCommerce), Mkt, Exhibi.
                                         '6279aa38cec5e7061a55d793',   #Tablero: GCIA Operación Retail y Servicios Financieros, Inmobiliaria, Diseño y Construcción
                                         '62731c9116c8203cae887bd0',   #Tablero: GCIA Originación, Crédito al Consumo, Cobranzas
                                         '62e5d42fe27f6d71c819c7f0',   #Tablero: GCIA RRHH
                                         '62e097ed3b05c87167ea98c6',   #Tablero: GCIA Sistemas
                                         '62e9387108771006e53b6151',   #Tablero: GCIA Tablero de Control
                                         '62ebddc6189ad70bacffe1f8',   #Tablero: Seguros
                                         '62f5661895b2742ec058d64a'])] #Tablero: Servicios Financieros

boards.head()

#=============================================================

#Creating lists
cols_to_select = ["id", "name"]
cols_to_rename = ["list_id", "list_name"]

cols_to_rename = dict(zip(cols_to_select, cols_to_rename))

lists_df = []

for board_id in boards["board_id"]:
    #API conection.
    url_board_lists = f"https://api.trello.com/1/boards/{board_id}/lists"
    
    #Parameters.
    params = dict(fields="name", cards="none", key=api_key, token=token)
    
    #Extracting info.
    data = get(url_board_lists, params)
    
    list_df_i = pd.json_normalize(data, sep='_')
    list_df_i = list_df_i.rename(columns=cols_to_rename)
    list_df_i["board_id"] = board_id
    
    #Adding information from board to the total of boards.
    lists_df.append(list_df_i)

#Merging lists.
lists_df = pd.concat(lists_df)

#=============================================================

#Cards from the boards.
cards_df = []

for board_id in boards["board_id"]:
    #Conexión a la API
    url_board_card = f"https://api.trello.com/1/boards/{board_id}/cards"
    
    #Parametros
    params = dict(fields="id,name,desc,idList,idBoard,shortUrl", key = api_key, token=token)
    
    #Extracción de info
    data = get(url_board_card, params)
    
    #Convertir a dataframe
    card_df_i = pd.DataFrame(data)
    
    #Añadir información del tablero i al total de tableros
    cards_df.append(card_df_i)

#Concatenar la lista
cards_df = pd.concat(cards_df)

#Ordenar dataset por ID
cards_df = cards_df.sort_values(["idBoard","id"]).reset_index(drop=True)
    
#Agregar columna de fecha de creación de la tarjeta
cards_df["card_creation_dt"] = cards_df["id"].apply(get_creation_dt)
    
#Renombrar columnas
cards_df.rename(columns={"id": "card_id","name":"card_name","idBoard":"board_id","idList":"list_id"},inplace=True)

#Exclusiones
#Excluir tarjetas con nombre vacio (contadores)
cards_df = cards_df[~(cards_df["card_name"] == "")]

#Excluir fechas anteriores al 1 de agosto (a petición de Luis)
cards_df = cards_df[cards_df["card_creation_dt"] >= "2022-08-01"]

#Agregar nombres de listas a las tarjetas
cards_df = cards_df.merge(lists_df)

#Quitar las tarjetas que se encuentren en la lista de instrucciones
cards_df = cards_df[cards_df['list_name'] != "Instrucciones para Crear Tarjetas (No archivar ni borrar)"]

#=============================================================

#Restructuring columns.
cols_to_select = ["id", "data_card_id", "idMemberCreator",
                  "type", "date", "data_card_name",
                  "data_list_name", "data_listBefore_name",
                  "data_listAfter_name", "data_list_id",
                  "data_listBefore_id", "data_listAfter_id",
                  "data_board_id", "data_board_name"]

cols_to_rename = ["action_id", "card_id",
                  "MemberCreator_id", "action_type",
                  "action_date", "card_name",
                  "list_name", "listBefore_name",
                  "listAfter_name","list_id",
                  "listBefore_id", "listAfter_id",
                  "board_id", "board_name"]

cols_to_rename = dict(zip(cols_to_select, cols_to_rename))
list_actions = list()

#=============================================================

#Iterate over all cards to get the actions
for card in cards_df.card_id:
    url_card_actions = f"https://api.trello.com/1/cards/{card}/actions"

    params = dict(filter="updateCard,createCard,copyCard", key=api_key, token=token)
    response = get(url_card_actions, params)
    actions = pd.json_normalize(response, sep='_')
    actions = actions.reindex(columns = cols_to_select, fill_value=np.nan).rename(columns=cols_to_rename)
    list_actions.append(actions)

actions_df = pd.concat(list_actions)
actions_df["action_creation_dt"] = actions_df["action_id"].apply(get_creation_dt)

#Ordering data.
actions_df = actions_df.sort_values(["card_id","action_creation_dt"],ascending=True).reset_index(drop=True)

#=============================================================

#Board members.
members_df = []

for board_id in boards["board_id"]:
    
    url_board_members = f"https://api.trello.com/1/boards/{board_id}/members"
    
    cols_to_rename = ["member_id", "member_fullName", "member_username"]
    
    params = dict(key=api_key, token=token)
    
    response = get(url_board_members, params=params)

    members_df_i = pd.json_normalize(response, sep='_')
    members_df_i = members_df_i.rename(columns=dict(zip(members_df_i.columns, cols_to_rename)))
    #members_df_i["board_id"] = board_id

    #Adding information from board to board totals.
    members_df.append(members_df_i)

#Merging lists.
members_df = pd.concat(members_df).drop_duplicates()

#List of unique members.
#members_df_unique = members_df.merge(boards[["board_id","board_name"]])[["member_id","member_fullName","member_username","board_name"]].groupby('member_id').agg({'member_fullName':'first','board_name': ' | '.join, 'member_username':'first' }).reset_index()

#=============================================================

#Identifying card creators.
card_creators_df = actions_df[(actions_df["action_type"]=="createCard")|(actions_df["action_type"]=="copyCard")][["MemberCreator_id","card_id"]]

#Adding info to the table.
cards_df = cards_df.merge(card_creators_df, how="left")

#=============================================================

#Obtaining movements of cards to the 'Done' list.
done_cards_df = actions_df[actions_df["listAfter_name"]=="Done"][["card_id","action_creation_dt"]]

#Renaming columns.
done_cards_df.rename(columns={"action_creation_dt":"card_done_dt"}, inplace=True)

#First date the card was passed to 'Done'.
done_cards_df = done_cards_df.groupby("card_id").first().reset_index()

#Adding info to the table.
cards_df = cards_df.merge(done_cards_df, how="left")

#=============================================================

#Time in lists.
actions_sort = actions_df.copy().sort_values(by=["card_id", "action_date"])

actions_cards_processed = []
cards_unique = actions_sort["card_id"].unique()

for card_id in cards_unique:
    
    actions_card = actions_sort[actions_sort["card_id"] == card_id]
    
    #Eliminating needless card movements.
    actions_card = actions_card.drop(actions_card[actions_card["listBefore_name"].isna()][1:].index).reset_index(drop=True)
    
    #Creating a copy of the last movement.
    actual = actions_card.tail(1).copy()
    
    #Adding info to the copy of the last movement.
    actual["action_creation_dt"] = np.datetime64(datetime.now())
    actual["listBefore_id"] = actual["listAfter_id"]
    actual["listBefore_name"] = actual["listAfter_name"]
    
    #Adding to the copy of the last action.
    actions_card = pd.concat([actions_card, actual]).reset_index(drop=True)
    
    #Crear una columna con las fechas de la acción desfasadas 1 fila hacia abajo
    actions_card["action_creation_dt_shift"] = actions_card["action_creation_dt"].shift(1)
    
    #Actualizar los siguientes campos en la segunda acción
    actions_card.at[1, 'listBefore_name'] = actions_card["list_name"].iloc[0]
    actions_card.at[1, 'listBefore_id'] = actions_card["list_id"].iloc[0]
    
    #Quitar todas las filas que tengan valor nulo en el campo de lista anterior (primer fila)
    actions_card = actions_card.drop(actions_card[actions_card.listBefore_name.isna()].index).reset_index(drop=True)
    
    #Añadir filas al dataset
    actions_cards_processed.append(actions_card)    
    
#Concatenar todos los datasets
actions_cards_processed = pd.concat(actions_cards_processed).reset_index(drop=True)
    
#Crear campos
actions_cards_processed["segundos"] = (actions_cards_processed['action_creation_dt'] - actions_cards_processed['action_creation_dt_shift']).astype('timedelta64[s]')
actions_cards_processed["minutos"] = actions_cards_processed["segundos"]/60
actions_cards_processed["horas"] = actions_cards_processed["minutos"]/60
actions_cards_processed["dias"] = actions_cards_processed["horas"]/24

#Eliminar registros donde exista fecha nulas (tarjetas que venían precargadas al inicio del Trello)
actions_cards_processed = actions_cards_processed.drop(actions_cards_processed[actions_cards_processed["action_creation_dt_shift"].isna()].index).reset_index(drop=True)

#=============================================================

# Agregaete by card id and List
actions_agg = actions_cards_processed.groupby(['card_id', 'listBefore_id']).sum().reset_index()

actions_agg = actions_agg[['card_id', 'listBefore_id', 'minutos', 'horas', 'dias']].rename(columns={"listBefore_id": "list_id"})

actions_agg = actions_agg.merge(lists_df[["list_name","list_id"]], how="left").merge(cards_df[["card_id","card_name"]], how="left")

actions_agg = actions_agg[~actions_agg["list_name"].isna()]

actions_agg = actions_agg.pivot(index="card_id", columns="list_name", values="dias").reset_index()

#=============================================================

#Crear tabla final a través de uniones
final_df = cards_df.merge(members_df, how="left",left_on="MemberCreator_id",right_on="member_id").merge(boards[["board_id", "board_name"]],how="left").merge(actions_agg,how="left").merge(lists_df[["list_id","list_name"]]).drop(["card_id","member_id","list_id","board_id"],axis=1)

final_df.drop("Instrucciones para Crear Tarjetas (No archivar ni borrar)",axis=1,inplace=True)

#Crear columna de folio
final_df["folio"] = final_df.shortUrl.str.rsplit('/', 1,expand=True).drop(0,axis=1)

#Pasar dataframe final a CSV
final_df[(final_df.card_done_dt >= "2022-12-01") & (final_df.card_done_dt < "2023-01-31")].to_csv("TARJETAS TRELLO.csv",index=False)

'''
Data_TrelloBoard = pd.read_csv('TARJETAS TRELLO.csv')

Label = Data_TrelloBoard[]

charts.GenerateBarChart('Porcentajes',)
'''