import json
import os

def applyCommit(n: int):
	f = open("commits.json", "r")
	commit = json.load(f)[n]
	f.close()
	os.system("rm test_dir/*")
	for i in commit["files"]:
		f = open("test_dir/" + i, "w")
		f.write(commit["files"][i])
		f.close()