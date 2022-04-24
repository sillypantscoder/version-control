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
	def getPreviousCommits(self) -> "list[Commit]":
		f = open("commits.json", "r")
		c = json.load(f)["commits"]
		f.close()
		r = []
		for i in range(len(c)):
			if self.index in c[i]["next"]:
				r.append(Commit(i))
		return r
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
	def _getPosition(self):
		prev = self.getPreviousCommits()
		if prev == []: return (0, 0)
		prevpos = prev[0]._getPosition()
		p = 0
		for i in prev[0].getNextCommits():
			if i.index == self.index:
				return (prevpos[0] + p, prevpos[1] + 50)
			p += 50
	def getPosition(self, offset: "tuple[int, int]") -> "tuple[int, int]":
		b = self._getPosition()
		return (b[0] + offset[0], b[1] + offset[1])
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
	cur = commits["current"]
	com = commits["commits"][cur]
	if com["files"] != getFiles():
		if com["type"] == "working":
			com["files"] = getFiles()
			if Commit(cur).getPreviousCommits()[0].files == getFiles():
				commits["commits"].remove(com)
				commits["current"] = Commit(cur).getPreviousCommits()[0].index
				commits["commits"][Commit(cur).getPreviousCommits()[0].index]["next"].remove(cur)
		else:
			commits["commits"].append({"name": "Local Changes", "files": getFiles(), "next": [], "type": "working"})
			com["next"].append(len(commits["commits"]) - 1)
			commits["current"] = len(commits["commits"]) - 1
	f = open("commits.json", "w")
	f.write(json.dumps(commits, indent=4).replace("    ", "\t"))
	f.close()
