import json
import os

class Commit:
	def __init__(self, n: int):
		self.index = n
		f = open("commits.json", "r")
		self.commit: dict = json.load(f)["commits"][n]
		f.close()
		self.files: dict[str, str] = self.commit["files"]
		self.name: str = self.commit["name"]
		self.type: str = self.commit["type"]
	def getNextCommits(self) -> "list[Commit]":
		return [Commit(i) for i in self.commit["next"]]
	def apply(self):
		os.system("rm test_dir/*")
		for i in self.commit["files"]:
			f = open("test_dir/" + i, "w")
			f.write(self.commit["files"][i])
			f.close()
		f = open("commits.json", "r")
		commits = json.load(f)
		f.close()
		commits["current"] = self.index
		f = open("commits.json", "w")
		f.write(json.dumps(commits, indent=4).replace("    ", "\t"))
		f.close()
	def __repr__(self):
		return f"<Commit \"{self.name}\">"

def getCommits() -> "list[Commit]":
	f = open("commits.json", "r")
	commits = json.load(f)
	f.close()
	return [Commit(i) for i in range(len(commits["commits"]))]

def getCurrentCommit() -> Commit:
	f = open("commits.json", "r")
	commits = json.load(f)
	f.close()
	return Commit(commits["current"])

def getFiles() -> "dict[str, str]":
	f = os.listdir("test_dir")
	return {i: open("test_dir/" + i, "r").read() for i in f}

def updateFiles() -> None:
	f = open("commits.json", "r")
	commits = json.load(f)
	f.close()
	if commits["commits"][commits["current"]]["files"] != getFiles(): 												# if the files have changed:
		if commits["commits"][commits["current"]]["type"] == "working": 												# if the current commit is a working commit:
			commits["commits"][commits["current"]]["files"] = getFiles() 													# update the files
		else: 																											# otherwise:
			commits["commits"].append({"name": "Local Changes", "files": getFiles(), "next": [], "type": "working"}) 		# add a new working commit
			commits["commits"][commits["current"]]["next"].append(len(commits["commits"]) - 1) 								# add the new commit to the current commit's next commits
			commits["current"] = len(commits["commits"]) - 1 																# and switch to the new commit
	f = open("commits.json", "w")
	f.write(json.dumps(commits, indent=4).replace("    ", "\t"))
	f.close()
