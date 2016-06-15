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
	scenes = []

	def __init__(self, fname):
		self.scenes = self.parse_script(fname)

	def get_category(self, parag):
		if parag[0].isupper() and len(parag) > 1:
			return "d"
		return "s"

	def clean_scenes(self, lst):
		clean = []
		for l in lst:
			if l.strip() == "" or (l.isupper() and [x for x in SCENE_HEAD if x in l]):
				continue
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
		return clean

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
				scenes.append(self.clean_scenes(parag[idx:i]))
				idx = i
		scenes.append(self.clean_scenes(parag[idx:]))
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

def get_scene_sentiment(scene, sen_dct):
	val = 0
	for x in scene:
		if x[0] != "s":
			continue
		txt = x[1]
		val += get_sentiment_value(txt, sen_dct)
	return val

def print_scene_score(script, score):
	# print result
	#for x in sen_score:
	#	print x


	for i in range(0, len(script.scenes)):
		txt = ""
		#if i != 64:
		#	continue
		for x in script.scenes[i]:
			if x[0] == "d":
				continue
			txt += x[1] + '\n'

		print sen_score[i]
		print txt
		print
		print

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


def get_dialogue_sentiment(script, chars, sen_dct):
	rel = {}
	for j in range(0, len(script.scenes)):
		scene = script.scenes[j]
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

			cc = (speaker, listener)
			if cc not in rel:
				rel[cc] = {}
			if j not in rel[cc]:
				rel[cc][j] = []
			score = get_sentiment_value(diag, sen_dct)
			
			rel[cc][j].append((score, diag))
	return rel

def get_diag_sen_summ(diag_sen):
	summ = {}
	for c in diag_sen:
		summ[c] = []
		scenes = diag_sen[c]
		for i in sorted(scenes):
			s = scenes[i]
			lines = []
			total = 0

			for x in s:
				total += x[0]
				lines.append(x[1])
			summ[c].append((i, total, lines))

	return summ

def main():
	sen_dct = get_sentiment_dict()
	#script = Movie_Script("frozen_script.txt")
	script = Movie_Script("train_Toy Story.txt")

	# scene sentiment
	sen_score = []
	for x in script.scenes:
		score = get_scene_sentiment(x, sen_dct)
		sen_score.append(score)

	# dialogue sentiment
	diag_sen = get_dialogue_sentiment(script, TOYSTORY, sen_dct)
	diag_summ = get_diag_sen_summ(diag_sen)

	for k in diag_summ:
		print k
		for x in diag_summ[k]:
			print "\t", x[0], "\t", x[1]
		print

	return

if __name__ == "__main__":
    main()