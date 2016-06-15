import re

SCENE_HEAD = ["EXT.", 
				"INT.", 
				"CUT TO", 
				"DISSOLVE TO", 
				"FADE IN", 
				"PAN TO", 
				"WHITE OUT TO", 
				"FADE OUT", 
				"MOMENTS LATER", 
				"PLAY MONTAGE",
				"OPEN ON",
				"THE END",
				"ANGLE",
				"SFX"]

# MAIN CHARACTERS
FROZEN = ["ANNA", "ELSA", "KRISTOFF", "HANS", "OLAF", "DUKE"]
TOYSTORY = ["WOODY", "BUZZ", "ANDY", "POTATO HEAD", "REX", "SARGENT", "DAVIS", "SLINKY", "SID", "HANNAH"]


class Movie_Script:
	scenes = {}
	chars = []

	def __init__(self, fname, chars):
		self.chars = chars
		s = self.parse_script(fname)
		self.group_scene(s)

	def group_scene(self, s):
		for i in range(0, len(s)):
			x = s[i]
			for y in x[0]:
				if y not in self.scenes:
					self.scenes[y] = []
				self.scenes[y].append((x[1], i))
		

	def get_category(self, parag):
		if parag[0].isupper() and len(parag) > 1:
			return "d"
		return "s"

	def get_chars(self, scene):
		c = []
		for x in self.chars:
			for y in scene:
				if y[0] == "d" and x in y[2] and x not in c:
					c.append(x)
				elif x in y[1] and x not in c:
					c.append(x)
		return sorted(c)

	def clean_scenes(self, lst):
		clean = []
		for l in lst:
			if l.strip() == "" or (l.isupper() and [x for x in SCENE_HEAD if x in l]):
				continue

			# before split, find all char that occur on that scene
			parag = l.split('\n')
			parag = [x for x in parag if x.strip() != ""]
			cat = self.get_category(parag)

			if cat == "d":
				char = parag[0].strip()
				content = " ".join([x.strip() for x in parag[1:]])
				clean.append((cat, content, char))
			else:
				content = " ".join([x.strip() for x in parag])
				clean.append((cat, content))

			all_char = self.get_chars(clean)
		return clean, all_char

	def parse_script(self, fname):
		with open(fname, "r") as t_file:
			data = t_file.read()
		t_file.close()

		pattern_parag = re.compile("\n( *)\n")
		parag = pattern_parag.split(data)

		scenes = []
		idx = 0
		for i in range(0, len(parag)):
			p = parag[i]
			if "INT." in p or "EXT." in p:
				clean, chars = self.clean_scenes(parag[idx:i])
				if len(chars) == 0:
					continue
				scenes.append((chars, clean))
				idx = i
		clean, chars = self.clean_scenes(parag[idx:])
		if len(chars) != 0:
			scenes.append((chars, clean))

		return scenes


def get_sentiment_dict():
	with open("AFINN/AFINN-111.txt", "r") as t_file:
		data = t_file.readlines()
	t_file.close()

	dct = {}
	for d in data:
		token = d.split('\t')
		word = token[0].strip()
		val = int(token[1])
		dct[word] = val

	return dct

def get_speaker(name, chars):
	#print chars
	character = None
	for c in chars:
		#print name, c
		if c.lower() in name.lower():
			character = c
	return character

def get_listener(scene, i, chars):
	# check next line
	if i < len(scene) - 1 and scene[i+1][0] == "d":
		c = get_speaker(scene[i+1][2], chars)
		if c != None:
			return c

	# check prev line
	if i > 0 and scene[i-1][0] == "d":
		c = get_speaker(scene[i-1][2], chars)
		if c != None:
			return c

	# check the dialogue
	diag = scene[i][1]
	c = get_speaker(diag, chars)
	if c != None:
		return c

	return None


def get_dialogue_sentiment(scene, main_char, sen_dct, chars):
	rel = {}
	rel["A"] = 0
	rel["P"] = 0

	for i in range(0, len(scene)):
		line = scene[i]
		if line[0] != "d":
			continue
		speaker = get_speaker(line[2], chars)
		if speaker == None:
			# minor character
			continue
		diag = line[1]
		listener = get_listener(scene, i, chars)
		if listener == None or listener == speaker:
			# invalid
			continue

		score = get_sentiment_value(diag, sen_dct)

		# active
		if speaker == main_char:
			rel["A"] += score
		# passive
		elif listener == main_char:
			rel["P"] += score

	return rel


def get_sentiment_value(txt, sen_dct):
	val = 0
	cnt = 0
	token = txt.lower().split()
	for t in token:
		if t in sen_dct:
			val += sen_dct[t]
			cnt += 1

	#if cnt == 0:
	#	return 0
	#return float(val) / cnt
	return val

def get_scene_sentiment(scene, main_char, sen_dct, chars):
	val = 0
	# sentiment for naration
	for x in scene:
		if x[0] == "d":
			continue
		else:
			txt = x[1]
			val += get_sentiment_value(txt, sen_dct)

	# sentiment for dialogue
	rel = get_dialogue_sentiment(scene, main_char, sen_dct, chars)
	return val, rel

def print_scene_score(scores):
	for x in scores:
		print x
		for y in scores[x]:
			#print "\tIdx: ", y[3]
			#print "\tScene: ", y[0]
			#print "\tActive: ", y[1]["A"]
			#print "\tPassive: ", y[1]["P"]
			#print

			print y[3], "\t", y[0], "\t", y[1]["A"], "\t", y[1]["P"]
		print
		print


def main():
	sen_dct = get_sentiment_dict()
	script = Movie_Script("frozen_script.txt", FROZEN)
	#script = Movie_Script("train_Toy Story.txt")

	# scene sentiment
	scores = {}
	for x in script.scenes:
		scores[x] = []
		for y in script.scenes[x]:
			score, rel = get_scene_sentiment(y[0], x, sen_dct, FROZEN)
			scores[x].append((score, rel, y[0], y[1]))

	print_scene_score(scores)

	# dialogue sentiment
	#diag_sen = get_dialogue_sentiment(script, FROZEN, sen_dct)
	#diag_summ = get_diag_sen_summ(diag_sen)

	#for k in diag_summ:
	#	print k
	#	for x in diag_summ[k]:
	#		print "\t", x[0], "\t", x[1]
	#	print

	return

if __name__ == "__main__":
    main()