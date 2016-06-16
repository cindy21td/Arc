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

GENRES = [ "Action",
		   "Adventure",
		   "Animation",
		   "Biography",
		   "Comedy",
		   "Crime",
		   "Documentary",
		   "Drama",
		   "Family",
		   "Fantasy",
		   "Film-Noir",
		   "History",
		   "Horror",
		   "Music",
		   "Musical",
		   "Mystery",
		   "Romance",
		   "Sci-Fi",
		   "Sport",
		   "Thriller",
		   "War",
		   "Western"
		]

FROZEN = {"ANNA" : ("F", 1),
			"ELSA":	("F", 1),
			"KRISTOFF":	("M", 1),
			"HANS":	("M", 1),
			"OLAF":	("M", 0),
			"DUKE":	("M", 0)
		}

TOYSTORY = {"WOODY": ("M", 1),
			"BUZZ":	("M", 1),
			"ANDY":	("M", 1),
			"POTATO HEAD": ("M", 0),
			"REX": ("M", 0),
			"SARGENT": ("M", 0),
			"DAVIS": ("M", 0),
			"SLINKY": ("M", 0),
			"SID": ("M", 0),
			"HANNAH": ("F", 0),
			"HAMM":	("M", 0),
			"BO PEEP": ("F", 0)
		}

WALLE = {"WALL-E": ("M", 1),
		"EVE": ("F", 1),
		"CAPTAIN": ("M", 1),
		"AUTO":	("M", 0)
		}	

NINE = {"DICTATOR": ("M", 0),
		"SCIENTIST": ("M", 0),
		"RADIO": ("M", 0),
		"1": ("M", 1),
		"2": ("M", 0),
		"5": ("M", 1),
		"6": ("M", 1),
		"7": ("F", 1),
		"8": ("M", 0),
		"9": ("M", 1)
		}	

KUNGFUPANDA = {"NARRATOR": ("M", 0),
				"GATOR": ("M", 0),
				"BUNNY": ("M", 0),
				"MONKEY": ("M", 0),
				"PO": ("M", 1),
				"TIGRESS": ("F", 1),
				"SHIFU": ("M", 1),
				"OOGWAY": ("M", 0),
				"PATRON": ("M", 0),
				"ZENG": ("M", 0),
				"CRANE": ("M", 0),
				"TAI LUNG": ("M", 0),
				"VIPER": ("F", 0),
				"DAD": ("M", 0),
				"MANTIS": ("M", 0)
			}

SHREKTHETHIRD = {"SHREK": ("M", 1),
				"DONKEY": ("M", 1),
				"FIONA": ("F", 1),
				"PUSS IN BOOTS": ("M", 1),
				"QUEEN": ("F", 0),
				"KING": ("M", 0),
				"PRINCE": ("M", 0),
				"MERLIN": ("M", 0),
				"ARTIE": ("M", 1),
				"PINOCCHIO": ("M", 0),
				"PIGS": ("M", 0),
				"DORIS": ("M", 0),
				"MICE": ("M", 0),
				"LANCELOT": ("M", 0),
				"HOOK": ("M", 0),
				"EVIL": ("F", 1)
			}

MOVIES = [("frozen_script.txt", FROZEN, ["Animation", "Adventure", "Comedy"]),
			("train_Toy Story.txt", TOYSTORY, ["Animation", "Adventure", "Comedy"]),
			("train_9 (2009 animated film).txt", NINE, ["Animation", "Adventure", "Action"]),
			("train_Kung Fu Panda.txt", KUNGFUPANDA, ["Animation", "Adventure", "Action"]),
			("train_Shrek the Third.txt", SHREKTHETHIRD, ["Animation", "Adventure", "Comedy"]),
			("train_WALL-E.txt", WALLE, ["Animation", "Adventure", "Family"])
		]