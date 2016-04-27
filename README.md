# Slack File Cleaner
A simple python script to erase your slack team files when you reach the maximum space available.

##How to Use
Start by adding your domain and token in the script variables.

	token = ""
	domain = ""
	
make sure you have the module [requests](http://docs.python-requests.org/en/master/user/install/) installed and simply run
	
	python main.py
	
What this script does is delete the all the public files in that team for the user token provided and it does so by deleting 100 at each step.

##Possible Errors
It is possible that you will have some error messages, [here](https://api.slack.com/methods/files.delete) is a detailed list of them.
The most frequent are:

* **not_authed** - No token provided
* **invalid_auth** - Invalid token
* **cant\_delete\_file** - The provided token doesn't have the correct permissions to delete that file. [^permissions]

[^permissions]: In order to delete all the files I recommend you to give admin permissons to the token you provided or most of the files will return this error message.