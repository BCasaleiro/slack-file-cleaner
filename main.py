#!/usr/bin/env python 

# from https://github.com/BCasaleiro/slack-file-cleaner

import requests
import json
import calendar
import time
import pprint
from datetime import datetime, timedelta

tokens = [  # make a list of ("domain", "token") here...
        ("YourDomainGoesHere", "YourApiTokenGoesHere"),
    ]

daysToKeep = 30
totalDeletedBytes = 0
dryRun = False

if __name__ == '__main__':
    for t in tokens:
        domain = t[0]
        token  = t[1]
        print "Starting work for " + domain + ".slack.com with token " + token
        while 1:
            files_list_url = 'https://slack.com/api/files.list'
            ts_to = datetime.now() + timedelta(-daysToKeep)
            print "Looking for files created prior to " + ts_to.strftime('%Y-%m-%d')
            date  = str(calendar.timegm(ts_to.utctimetuple()))
            data = {"token": token, "ts_to": date}
            response = requests.post(files_list_url, data = data)
            if response.status_code != 200:
                print("Slack API files.list response status code = %d" % (response.status_code))
                break

            decodedResult = response.json()
            if not "files" in decodedResult or len(decodedResult["files"]) <= 0:
                break   # no files left in this list

            #print("length of resulting files array = %d" % (len(response.json()["files"])))
            for f in decodedResult["files"]:
                if dryRun:
                    print("Found file %s %5dKB %s" % (datetime.fromtimestamp(f["created"]).strftime('%Y-%m-%d'),  f["size"]/1024, f["name"]))
                else:
                    print("Deleting file %s %5dKB %s" % (datetime.fromtimestamp(f["created"]).strftime('%Y-%m-%d'),  f["size"]/1024, f["name"]))
                    timestamp = str(calendar.timegm(datetime.now().utctimetuple()))
                    delete_url = "https://" + domain + ".slack.com/api/files.delete?t=" + timestamp
                    response2 = requests.post(delete_url, data = {
                        "token": token,
                        "file": f["id"], 
                        "set_active": "true", 
                        "_attempts": "1"})
                    #print response2.json()
                    totalDeletedBytes += f["size"]
            if dryRun:
                break   # only run once, otherwise we loop forever in a dry run
            time.sleep(1)
    print("Done! %dMB total deleted" % (totalDeletedBytes/(1024*1024)))
