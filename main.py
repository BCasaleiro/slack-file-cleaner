import requests
import json
import calendar
from datetime import datetime, timedelta

token = ""

domain = ""
files_url = "https://slack.com/api/files.list"
delete_url = "https://" + domain + ".slack.com/api/files.delete"

data = {"token": token}

while 1:
    response = requests.post(files_url, data = data)
    files = response.json()["files"]
    paging = response.json()["paging"]

    if len(files) == 0:
        print "No files to delete"
        break
    else:

        print "Deleting " + str(paging["count"]) + " of " + str(paging["total"]) + "files..."

        for value in files:
            delete_data = {"token": token, "file": value["id"]}
            delete_response = requests.post(delete_url, delete_data)
            print "Deleted '" + value["title"] + "'"

print "Done"
