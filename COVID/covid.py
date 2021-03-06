import pandas as pd
import numpy as np
import json
import os.path

data_file = "COVID_MX_2020_tst.xlsx"
catalog_file = "Catalogos.xlsx"
desc_file = "descriptor.json"

catalogs = {}
mappings = {}
covid_df = None


def load_files():
    global covid_df
    global mappings
    # Read the descriptor from the json file
    j_file = open(desc_file, "r")
    desc = json.loads(j_file.read())
    mappings = desc["fields"]
    load_catalogs(desc)
    j_file.close()
    if not os.path.exists("export_dataframe.xlsx"):
        print("Loading data source...")
        # Load the main data source
        xl = pd.ExcelFile(data_file)
        covid_df = xl.parse('Hoja1')
        # Describe our main data set
        # print(covid_df.index)       # Gives me the range of the indices (Number of rows)
        # Gives me rows and columns
        print("The data set contains " + str(covid_df.shape[0]) + " rows by " + str(covid_df.shape[1]) + " columns.")
        # print(covid_df.dtypes)      # Describes my data source by telling me how did pandas identify each column
        # print(covid_df.head(5))     # Prints the top n values of my data source
        print("Done.")
        print("Cleaning data...")
        merge_clean_data()
        print("Done.")
        # print(covid_df.head(5))  # Prints the top n values of my data source
        # Save clean data
        covid_df.to_excel(r'export_dataframe.xlsx', index=False, header=True)
    else:
        xl = pd.ExcelFile('export_dataframe.xlsx')
        covid_df = xl.parse('Sheet1')

def load_catalogs(desc):
    print("Loading catalogs...")
    cat_xl = pd.ExcelFile(catalog_file)
    for i in desc["catalogs"]:
        # print("Catalogo: " + i)
        catalogs[i] = cat_xl.parse(i)
        # Clean NaN values
        catalogs[i].dropna(inplace=True)
        # Validate all the numeric columns to be integers
        dtypes = catalogs[i].dtypes.to_dict()
        if 'float64' in dtypes.values():
            for col_nam, typ in dtypes.items():
                if typ == 'float64':
                    catalogs[i][col_nam] = catalogs[i][col_nam].astype(int)
        # print(catalogs[i].dtypes)
        # print(catalogs[i].head())
    cat_mun = catalogs["MUNICIPIOS"]
    cat_mun["CODIGO"] = cat_mun["CLAVE_ENTIDAD"].astype(str) + "-" + cat_mun["CLAVE_MUNICIPIO"].astype(str)
    print("Done.")


def merge_clean_data():
    for fields in mappings:
        field = fields["name"]
        # print(field)
        if fields["format"] == "ID":
            covid_df.set_index(field)
        elif fields["format"] == "DATE":
            # Clean data of empty fields
            covid_df[field] = pd.to_datetime(covid_df[field], errors='coerce').fillna('')
            # spread values in different fields
            covid_df[field + "_YR"] = covid_df[field].apply(lambda x: x.year if x != '' else x)
            covid_df[field + "_MT"] = covid_df[field].apply(lambda x: x.month if x != '' else x)
            covid_df[field + "_DY"] = covid_df[field].apply(lambda x: x.day if x != '' else x)
            covid_df[field + "_WK"] = covid_df[field].apply(lambda x: x.week if x != '' else x)
        elif fields["format"] == "MUNICIPIOS":
            catalog = catalogs[fields["format"]]
            relation = fields["relation"]
            covid_df[field] = covid_df[relation].astype(str) + "-" + covid_df[field].astype(str)
            covid_df[field].replace(catalog["CODIGO"].values, catalog["MUNICIPIO"].values, inplace=True)
        elif fields["format"] == "ENTIDADES":
            catalog = catalogs[fields["format"]]
            covid_df[field].replace(catalog["CLAVE_ENTIDAD"].values, catalog["ABREVIATURA"].values, inplace=True)
        elif field == "PAIS_NACIONALIDAD":
            wrong_syntax = ["M????xico", "Espa????a", "Estados Unidos de Am????rica", "Hait????"]
            proper_syntax = ["Mexico", "Spain", "USA", "Haiti"]
            covid_df[field].replace(wrong_syntax, proper_syntax, inplace=True)
        elif fields["format"] in catalogs.keys():
            catalog = catalogs[fields["format"]]
            covid_df[field].replace(catalog["CLAVE"].values, catalog["DESCRIPCI??N"].values, inplace=True)

def searchIntoJSON(atr1, atr2, fileName):
  consulta = covid_df.groupby([atr1, atr2], as_index = False)["id_registro"].count()
  x,y = consulta.shape
  info = []
  for i in range(0,x):
    for j in range(0,y):
      if j==0:
        info.append({
        atr1 : consulta.values[i][j],
        atr2 : consulta.values[i][j+1],
        'count': str(consulta.values[i][j+2])
        })

  with open("json_files/" + fileName + ".json", 'w') as outfile:
      json.dump(info, outfile)


def searchIntoJSON2(atr1, fileName):
  labels = covid_df[atr1].value_counts().index
  values = covid_df[atr1].value_counts().values
  x = len(labels)
  info = []
  for i in range(0,x):
    info.append({
        atr1 : labels[i],
        'count' : str(values[i])
    })
  with open("json_files/"+fileName + ".json", 'w') as outfile:
      json.dump(info, outfile)

def clear_graph2():
    data = []
    with open('json_files\\graph-2.json') as file:
        data = json.load(file)

    #declare maps for age range
    map_contH=dict()
    map_contF=dict()
    #initialize in 0 counters
    for i in range(0,100,10):
        map_contH[str(0+i)+"-"+str(9+i)]=0
        map_contF[str(0+i)+"-"+str(9+i)]=0
    #add count
    for ele in data:
       for i in range(0,100,10):
            if (0+i)<=ele["edad"]<=(9+i) and ele["sexo"] == "HOMBRE":
                map_contH[str(0+i)+"-"+str(9+i)]+=int(ele["count"])
            elif (0+i)<=ele["edad"]<=(9+i) and ele["sexo"] == "MUJER":
                map_contF[str(0+i)+"-"+str(9+i)]+=int(ele["count"])
    info = []
    for key in map_contF:
        info.append({
        'rango' : key,
        'sexo' : 'MUJER',
        'count': str(map_contF[key])
        })
        info.append({
        'rango' : key,
        'sexo' : 'HOMBRE',
        'count': str(map_contH[key])
        })

    with open("json_files/graph-2.json", 'w') as outfile:
        json.dump(info, outfile)

load_files()

# print(covid_df.isnull().sum())
# covid_df.dropna(inplace=True)
# dup1 = covid_df
# dup2 = covid_df

# dup1[dup1.duplicated()]
# dup2.drop_duplicates(keep='first',inplace=True)

# print(covid_df["ENTIDAD_RES"].value_counts())

'''
sex_by_state_df = covid_df[['sexo', 'entidad_res']]
print("The data set contains " + str(sex_by_state_df.shape[0]) + " rows by " + str(sex_by_state_df.shape[1]) + " columns.")
print(sex_by_state_df.head())
'''


# TODO: Make sure you have virtualenv, django and djantorestframework

#grafica 1 intubados/enfermedades 
searchIntoJSON(atr1="tipo_paciente", atr2="intubado", fileName="graph-1")
#grafica 2 muertes/sexo/edad
searchIntoJSON(atr1="edad", atr2="sexo", fileName="graph-2")
#grafica 3 laboratorio/por estado
searchIntoJSON2(atr1="toma_muestra_lab", fileName="graph-3")
#grafica 4 sector/por estado
searchIntoJSON2(atr1="sector", fileName="graph-4")
clear_graph2()
