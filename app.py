from threading import Thread
from flask import Flask, render_template, request
from flask_pymongo import pymongo
import pandas as pd
# from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
from pymongo import MongoClient
import json
import os
from bson.objectid import ObjectId
# import dnspython
# import dataiku
import dataikuapi
import dataiku


# print(dataiku.Dataset("data_select_by_well").get_dataFrame().head())




# client is now a DSSClient and can perform all authorized actions.
# For example, list the project keys for which the API key has access
# client.list_project_keys()

from bokeh.embed import server_document

from py_viz.bkapp.vsh import eval_vsh
from py_viz.bkapp.phie import eval_phie
from py_viz.bkapp.sw import eval_sw
from py_viz.bkapp.perm import eval_perm
from py_viz.bkapp.facies import eval_facies
from py_viz.bkapp.hc import eval_hc
from py_viz.bkapp.histplot import plot_histogram, get_form

from math import cos, asin, sqrt

app = Flask(__name__)

num_data = 1500

@app.route("/getDataset")
def getDataset():
    dataiku.set_remote_dss("https://ai-delfi-ing-hackathon.datascience.delfi.slb.com/", "KQzhMgvVpsIF3ojSjeg12L9rdp9zdFAP")

    # host = "https://ai-delfi-ing-hackathon.datascience.delfi.slb.com/"
    # apiKey = "KQzhMgvVpsIF3ojSjeg12L9rdp9zdFAP"
    # client = dataikuapi.DSSClient(host, apiKey)

    project = client.get_project('DEMO_HACKUNAMATATA')
    # data = project.get_dataset("data_select_by_well")

    list_data
    for row in data.iter_rows():
        return json.dumps(row)

@app.route("/")
def viewForm():
    client = pymongo.MongoClient("mongodb+srv://johndoe:johndoe@cluster0.jyb2o.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.test
    database_name='hackuna_matata123'
    student_db=client[database_name]
    collection_name='user'
    collection=student_db[collection_name]
    user_data_list = []
    for document in collection.find():
        user_data_list.append(document)
        # print(document)
    #print(user_data_list[0]["data"])

    return render_template("form.html", user_data=user_data_list)

@app.route("/page-2")
def analyze_page():
    return render_template("analyze.html")

@app.route("/circles")
def circle_page():
    return render_template("circle.html")

@app.route("/postform", methods = ["POST"])
def upload_form():

    host = "https://ai-delfi-ing-hackathon.datascience.delfi.slb.com/"
    apiKey = "KQzhMgvVpsIF3ojSjeg12L9rdp9zdFAP"
    projectKey = "DEMO_HACKUNAMATATA"

    dataiku.set_remote_dss(host, apiKey, no_check_certificate=True)
    
    well_name = request.form.get("well_name")
    field_name = request.form.get("field_name")
    lat = request.form.get("form_lat")
    lon = request.form.get("form_lon")
    f = request.files['form_file']

    client = pymongo.MongoClient("mongodb+srv://johndoe:johndoe@cluster0.jyb2o.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.test

    # return db
    target_path = '/%s' % f.filename
    mf = dataiku.Folder('lYYI4uPp', project_key=projectKey)

    mf.upload_stream(target_path, f)

    # open('tmp/' + f.filename, 'wb').write(f.read())
    
    database_name='hackuna_matata123'
    student_db=client[database_name]


# @app.route("/postform")
# def upload_form():

#     client = pymongo.MongoClient("mongodb+srv://johndoe:johndoe@cluster0.jyb2o.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
#     db = client.test

#     database_name='hackuna_matata123'
#     student_db=client[database_name]

    collection_name='user'
    collection=student_db[collection_name]
    # f = request.files.get('file')
    # # mf = dataiku.Folder('O2B4wCQL') # name of the folder in the flow
    # # target_path = '/%s' % f.filename
    # # mf.upload_stream(target_path, f)

    # well = request.form.get('well')
    # lat = request.form.get('lat')
    # lon = request.form.get('lon')


    # df = pd.read_csv("tmp/"+f.filename)
    df = pd.read_csv(mf.get_download_stream(f.filename))
    
    source = {
        "filename":f.filename,
          "coordinate ": {"BAND":None, "EASTING":None,
                          "LATITUDE": lat, "LONGITUDE": lon,
                          "NORTHING": None, "WELL":well_name,
                          "ZONE": None},
          "data":[]
        # "wellName": well_name,
        # "latitude": lat,
        # "longitude": lon
    }
    
          
    
    for i in range(len(df)):
        dict_df = {}
        
        for col in df.columns:
            dict_df['WELL']=well_name
            dict_df[col]=df[col].iloc[i]
            
        source['data'].append(dict_df)
    
    # print(source)
    
    collection.insert_one(source)
    
    # return json.dumps("Data berhasil di input")
    return render_template("redirect_form.html")
#     # df = pd.read_csv(mf.get_download_stream(f.filename))

#     source = {
#         # "filename":f.filename,
#         #   "coordinate ": {"BAND":None, "EASTING":None,
#         #                   "LATITUDE": lat, "LONGITUDE": lon,
#         #                   "NORTHING": None, "WELL":well,
#         #                   "ZONE": None},
#         #   "data":[]
#         "wellName": well,
#         "latitude": lat,
#         "longitude": lon
#     }


#     # for i in range(len(df)):
#     #     dict_df = {}

#     #     for col in df.columns:
#     #         dict_df['WELL']=well
#     #         dict_df[col]=df[col].iloc[i]

#     #     source['data'].append(dict_df)

#     print(source)

#     collection.insert_one(source)

#     return json.dumps({1})

def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    hav = 0.5 - cos((lat2-lat1)*p)/2 + cos(lat1*p)*cos(lat2*p) * (1-cos((lon2-lon1)*p)) / 2

    return 12742 * asin(sqrt(hav))

def closest(data, v):
    for dd in data:
      dd['dist'] = distance(v['lat'],v['lon'],dd['lat'],dd['lon'])
      print(dd)
        #wow.jarak = distance(v['lat'],v['lon'],wow.get('lat'),wow.get('lon'))
    
    return min(data, key=lambda p: distance(v['lat'],v['lon'],p['lat'],p['lon']))

@app.route('/table/<id_well>/', methods=['GET'])
def well_table(id_well):
    

    # for line in df1:
    #     row = line.split(",")
    #     well = row[0]
    #     easting = row [1]
    #     northing = row[2]
    #     zone = row[3]
    #     band = row[4]
    #     latitude = row[5]
    #     longitude = row[6]
    # arr = df.to_dict()


    df = pd.read_csv("tmp/volve_coordinate.csv")
    
    list_coord = list()
    

    for i in range(len(df)):
        dict_coord = dict()
        dict_coord['lat'] = df['LATITUDE'][i]
        dict_coord['lon'] = df['LONGITUDE'][i]
        dict_coord['label'] = df['WELL'][i]
        dict_coord['dist'] = None
        list_coord.append(dict_coord)
        print(i)

    print(list_coord)

    v = {'lat': 56, 'lon': 10}
    nearest = closest(list_coord, v)

    # print(nearest)

    # return nearest

    client = pymongo.MongoClient("mongodb+srv://johndoe:johndoe@cluster0.jyb2o.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    db = client.test
    database_name='hackuna_matata123'
    student_db=client[database_name]
    collection_name='user'
    collection=student_db[collection_name]

    user_data_dict = collection.find_one({"_id": ObjectId(id_well)},{ "_id": 0, "data": 0 })

    # for document in collection.find({},{ "_id": 0, "data": 0 }):
    #     user_data_list.append(document)
    #     print(document)

    print(user_data_dict['coordinate ']['LATITUDE'])

    print(list_coord[0]['label'])

    return render_template("table_well.html", data=list_coord, user_data=user_data_dict)
    # return("ok")
    # return render_template('table_well.html', data = dataaa)

@app.route('/well-log')
def log():
    return render_template("wellLog.html")


@app.route('/hist', methods = ["get"])
def hist():
    
    data, list_formation = get_form(nameWell='15/9-F-5')
    # target = request.form.get[formation_form]
    print(list_formation)
    formation = list_formation[0]
    script, div, cdn_js = plot_histogram(data=data, nameWell='15/9-F-5', nameForm=formation)
    return render_template("hist.html",
                            list_formation = list_formation,
                            script=script,
                            div=div,
                            cdn_js=cdn_js)

@app.route('/hist_select', methods=['GET', 'POST'])
def hist_select():
    data, list_formation = get_form(nameWell='15/9-F-5')
    option_form = request.form.get('formation_form')
    script, div, cdn_js = plot_histogram(data=data, nameWell='15/9-F-5', nameForm=option_form)
    print(option_form)
    return render_template("hist_select.html",
                            list_formation = list_formation,
                            script=script,
                            div=div,
                            cdn_js=cdn_js)

@app.route('/hc', methods=['GET'])
def hc_page():
    script, div, cdn_js = eval_hc(num_data=num_data)
    return render_template("evalLog/hc.html",
                           script=script,
                           div=div,
                           cdn_js=cdn_js)


@app.route('/facies', methods=['GET'])
def facies_page():
    script, div, cdn_js = eval_facies(num_data=num_data)
    return render_template("evalLog/facies.html",
                           script=script,
                           div=div,
                           cdn_js=cdn_js)


@app.route('/perm', methods=['GET'])
def perm_page():
    script, div, cdn_js = eval_perm(num_data=num_data)
    return render_template("evalLog/perm.html",
                           script=script,
                           div=div,
                           cdn_js=cdn_js)


@app.route('/sw', methods=['GET'])
def sw_page():
    script, div, cdn_js = eval_sw(num_data=num_data)
    return render_template("evalLog/sw.html",
                           script=script,
                           div=div,
                           cdn_js=cdn_js)


@app.route('/phie', methods=['GET'])
def phie_page():
    script, div, cdn_js = eval_phie(num_data=num_data)
    return render_template("evalLog/phie.html",
                           script=script,
                           div=div,
                           cdn_js=cdn_js)


@app.route('/vsh', methods=['GET'])
def vsh_page():
    script, div, cdn_js = eval_vsh(num_data=num_data)
    return render_template("evalLog/vsh.html",
                           script=script,
                           div=div,
                           cdn_js=cdn_js)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
