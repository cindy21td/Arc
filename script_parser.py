import re
import Labels

class Movie_Script:
	scenes = {}
	chars = []
	total_scenes = 0

	def __init__(self, fname, chars):
		self.chars = chars
		s = self.parse_script(fname)
		self.total_scenes = len(s)
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
		all_char = []
		for l in lst:
			if l.strip() == "" or (l.isupper() and [x for x in Labels.SCENE_HEAD if x in l]):
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

def is_fluct(prev, curr, next):
	# different delta
	if (((curr - prev) > 0) != ((next - curr) > 0)):
		return True
	else:
		return False

def fluctuation(scores, total):
	fluct = {}
	for x in scores:
		fluct[x] = [0, 0, 0]
		if len(scores[x]) < 2:
			continue
		y = scores[x][0]
		s_prev = y[0]
		a_prev = y[1]["A"]
		p_prev = y[1]["P"]
		for i in range(1, len(scores[x]) - 1):
			y = scores[x][i]

			s_next = scores[x][i+1][0]
			a_next = scores[x][i+1][1]["A"]
			p_next = scores[x][i+1][1]["P"]

			if is_fluct(s_prev, y[0], s_next):
				fluct[x][0] += 1
			if is_fluct(a_prev, y[1]["A"], a_next):
				fluct[x][1] += 1
			if is_fluct(p_prev, y[1]["P"], p_next):
				fluct[x][2] += 1

			# update prev
			s_prev = y[0]
			a_prev = y[1]["A"]
			p_prev = y[1]["P"]

		# normalize the fluctuation score
		fluct[x][0] = float(fluct[x][0]) / total
		fluct[x][1] = float(fluct[x][1]) / total
		fluct[x][2] = float(fluct[x][2]) / total
			
	return fluct

def create_features(scores, fluct, total):
	features = {}
	for char in fluct:
		features[char] = []
		# append the fluctuation scores
		for x in fluct[char]:
			features[char].append(x)

		# number of occurrences
		occur = float(len(scores[char])) / total
		features[char].append(occur)

		# total length of dialogue
		d_len = 0
		c_d = 0
		for x in scores[char]:
			for s in x[2]:
				if s[0] == "d" and char in s[2]:
					d_len += len(s[1])
					c_d += 1

		if c_d == 0:
			features[char].append(0)
		else:
			features[char].append(float(d_len) / c_d)

	return features

def main():
	sen_dct = get_sentiment_dict()

	for m in Labels.MOVIES:
		fname = m[0]
		char_dct = m[1].keys()
		#(fname, char_dct) = ("frozen_script.txt", Labels.FROZEN.keys())
		#(fname, char_dct) = ("train_Toy Story.txt", TOYSTORY.keys())
		script = Movie_Script(fname, char_dct)

		# scene sentiment
		scores = {}
		for x in script.scenes:
			scores[x] = []
			for y in script.scenes[x]:
				score, rel = get_scene_sentiment(y[0], x, sen_dct, char_dct)
				scores[x].append((score, rel, y[0], y[1]))

		#print_scene_score(scores)

		fluct = fluctuation(scores, script.total_scenes)

		features = create_features(scores, fluct, script.total_scenes)

		print fname
		print features
		print

	return

if __name__ == "__main__":
    main()