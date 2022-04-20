import json
import os

class Commit:
	def __init__(self, n: int):
		self.index = n
		f = open("commits.json", "r")
		self.commit = json.load(f)[n]
		f.close()
		self.files = self.commit["files"]
		self.name = self.commit["name"]
	def getNextCommits(self):
		return [Commit(i) for i in self.commit["next"]]
	def apply(self):
		os.system("rm test_dir/*")
		for i in self.commit["files"]:
			f = open("test_dir/" + i, "w")
			f.write(self.commit["files"][i])
			f.close()

def getCommits() -> "list[Commit]":
	f = open("commits.json", "r")
	commits = json.load(f)
	f.close()
	return [Commit(i) for i in range(len(commits))]