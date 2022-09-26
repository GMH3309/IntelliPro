#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 27 21:40:33 2022

@author: JeremyLZX
"""

import requests
import time
import json
import pickle
import pandas as pd
from tqdm import tqdm
import warnings
import subprocess
from pymongo import MongoClient, InsertOne, UpdateOne, DeleteOne




def main(i):
    while True:
        t1 = time.time()

        
        insert_id = []
        person_profiles = []
        
        # id_list = []
        # for item in db.aminer_scholar.aggregate([{"$match": {"scholar_profile": {"$exists": False}}}, {"$sample": { "size": 200}} ]):
        #     id_ = item['_id']
        #     id_list.append(id_)
        
        
        while True:
            try:
                size = 1000
                while True:
                    id_list = []
                    for item in db.aminer_scholar.aggregate([{"$sample": { "size": size}} ]):
                        if "scholar_profile" not in item.keys():
                            id_ = item['_id']
                            id_list.append(id_)
                    if len(id_list) == 0: 
                        size += 1000
                        time.sleep(30)
                    else: 
                        break
                break
            except:
                print('reconnect')
                
                subprocess.Popen("ssh -N -L 27117:10.0.0.70:27018 xinmeng.x@54.188.117.117 -i fortress_xinmeng.pem", shell=True)
                subprocess.Popen("ssh xinmeng.x@54.188.117.117 -i fortress_xinmeng.pem", shell = True)
                
                uri = "mongodb://xinmeng:Ipg%21%403X%21nm@127.0.0.1:27117/?authSource=shop_info&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"
                client = MongoClient(uri)
                db = client['shop_info']
                db.list_collection_names()
            

        print(i*200)
        i += 1
    
        for id_ in tqdm(id_list):
            
            
            while True:
                try:
                    res_1 = requests.post("https://apiv2.aminer.cn/magic", 
                                          json = [{"action":"personapi.get","parameters":{"ids":[id_]},"schema":{"person":["id","name","name_zh","avatar","num_view","is_follow","work","hide","nation","language","bind","acm_citations","links","educations","tags","tags_score","tags_zh","num_view","num_follow","is_upvoted","num_upvoted","is_downvoted","is_lock",{"indices":["hindex","gindex","pubs","citations","newStar","risingStar","activity","diversity","sociability"], "geo_addresses":["city_id","geo","alias","country_id","formatted_address","org_name","org_type","province_id"]},{"profile":["position","position_zh","affiliation","affiliation_zh","work","work_zh","gender","lang","homepage","phone","email","fax","bio","bio_zh","edu","edu_zh","address","note","homepage","titles"]}]}}], 
                                          headers = {'Authorization':'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFtaW5lcnZpcEBnbWFpbC5jb20iLCJleHAiOjE3NjY1NjgwMTQsImlhdCI6MTYwODg4ODAxNCwibmJmIjoxNDQ0NDc4NDAwLCJyb2xlcyI6WyJ0dXAiLCJhZG1pbiIsInZpZXdFbWFpbCJdLCJzcmMiOiJ0dXAiLCJ1aWQiOiI1YzkxZjlmNzUzMGM3MGI5MmY4NmFmY2QifQ.oZKkZhjxcBfRaBVUYyFE5q1kiGekAl9kjalw6iv13O8'}, verify=False, timeout=10)
                    # time.sleep(0.25)
                    break
                except:
                    print('timeout')
                    time.sleep(1)
            if not res_1.status_code == 200 or res_1.status_code == 404: 
                assert False
        
            person_info = json.loads(res_1.text)
            
            
            while True:
                try:
                    res_4 =  requests.post('https://apiv2.aminer.cn/magic?a=search.search+getGeoLocations', json = [{"action":"search.search","parameters":{"query":"","offset":0,"size":100,"searchType":"all","advquery":{"texts":[{"source":"fromYear","text":"1900"},{"source":"toYear","text":"2022"}]},"ids":[id_]},"primarySchema":"person","schema":{"person":["id","name","name_zh","avatar","tags",{"profile":["position","affiliation","org"]},{"indices":["hindex","gindex","pubs","citations","newStar","risingStar","activity","diversity","sociability"]}],"geo_addresses":["city_id","geo","alias","country_id","formatted_address","org_name","org_type","province_id"]}}], verify=False, timeout=10)
                    break
                except:
                    print('timeout')
            location_info = json.loads(res_4.text)
            # time.sleep(0.25)
           
            try:
                person_info['data'][0]['data'][0].update({"geo": location_info['data'][0]['items'][0]['geo']})
            except:
                continue
            
            # try:
            #     print(person_info['data'][0]['data'][0]['profile']['email'])
            # except:
            #     pass
            person_profiles.append(UpdateOne({'_id': id_}, {'$set': {'scholar_profile': person_info['data'][0]['data'][0]}}))
            
            while True:
                try:
                    res = requests.get("https://innovaapi.aminer.cn/predictor/api/v1/valhalla/highlight/get_first_author_papers/", json = {"pid":id_,"this_year":2022,"recent_n":10,"top_n":5}, verify=False, timeout=10)
                    break
                except:
                    print('timeout')
                    time.sleep(1)
            
            # try:
            #    json.loads(res.text)['data']
            # except:
            #    print('error')
            #    print(res.status_code)
            #    print(res.text)
            #    print(json.loads(res.text).keys())
			
            try:
                citation = json.loads(res.text)
                for _ in citation['data']:
                   for __ in _['authors']:
                       if 'id' in __.keys():
                           person_id = __['id']
                           insert_id.append({'_id': person_id})
            except:
                pass
            # time.sleep(0.25)
            
            while True:
                try:
                    res_2 = requests.get('https://api.top3-talent.com/expert/v1/{}/geo'.format(id_), verify=False, timeout=10)
                    break
                except:
                    print('timeout')
                    time.sleep(1)
            network = json.loads(res_2.text)
            try:
                for _ in network['data'][0]['data']:
                    person_id = _['id']
                    insert_id.append({'_id': person_id})
            except:
                pass
            
        # db.aminer_scholar.bulk_write(person_profiles)
        # try: db.aminer_scholar.insert_many(insert_id, ordered=False)
        # except: pass
    
    
        while True:
            try:
                
                db.aminer_scholar.bulk_write(person_profiles)
                
                try: db.aminer_scholar.insert_many(insert_id, ordered=False)
                except: pass
            
                break
            except:
                print('reconnect')
                
                subprocess.Popen("ssh -N -L 27117:10.0.0.70:27018 xinmeng.x@54.188.117.117 -i fortress_xinmeng.pem", shell=True)
                subprocess.Popen("ssh xinmeng.x@54.188.117.117 -i fortress_xinmeng.pem", shell = True)
                
                
                uri = "mongodb://xinmeng:Ipg%21%403X%21nm@127.0.0.1:27117/?authSource=shop_info&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"
                client = MongoClient(uri)
                db = client['shop_info']
                db.list_collection_names()
                
        t2 = time.time()
        print('time consuming ', t2 - t1)



if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    
    # connect to database
    subprocess.Popen("ssh -N -L 27117:10.0.0.70:27018 xinmeng.x@54.188.117.117 -i fortress_xinmeng.pem", shell=True)
    subprocess.Popen("ssh xinmeng.x@54.188.117.117 -i fortress_xinmeng.pem", shell = True)
    
    uri = "mongodb://xinmeng:Ipg%21%403X%21nm@127.0.0.1:27117/?authSource=shop_info&readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false"
    client = MongoClient(uri)
    db = client['shop_info']
    db.list_collection_names()
    
    
    # run main
    i = 0
    main(i)
    
    # while True:
    #     try:
    #         main(i)
    #     except Exception as e: 
    #         print(e)
    #         print("rerun main")
    #         time.sleep(150)
        
