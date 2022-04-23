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