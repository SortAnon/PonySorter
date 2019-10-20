import csv
import os
import datetime
import hashes
import hashlib
import json
from jsonschema import validate

with open(os.path.dirname(os.path.realpath(__file__)) + "/pony_schema.json") as f:
	schema = json.load(f)
try:
	with open(os.path.dirname(os.path.realpath(__file__)) + "/settings.json") as f:
		config = json.load(f)
except:
	config = {"audio_paths":[],"audio_hashes":{},}

def write_config():
	path = os.path.dirname(os.path.realpath(__file__)) + "/settings.json"
	with open(path, 'w') as f:
		json.dump(config, f, indent=4)
	return path

def import_from_labels(filename):
	episode_data = {}
	episode_data["label_name"] = os.path.splitext(os.path.basename(filename))[0].replace(" ", "_")
	if episode_data["label_name"] not in hashes.friendly_names:
		return None
	episode_data["friendly_name"] = hashes.friendly_names[episode_data["label_name"]]
	episode_data["last_modified"] = datetime.datetime.utcnow().isoformat()
	labels = []
	with open(filename) as f:
		for i in csv.reader(f, delimiter="\t"):
			label = {}
			label["start"] = float(i[0])
			label["end"] = float(i[1])
			label["character"] = i[2].split("_")[3]
			label["mood"] = i[2].split("_")[4].lower().split(" ")
			label["transcript"] = i[2].split("_")[6]
			label["noise_level"] = i[2].split("_")[5].replace(" ","").lower()
			if label["noise_level"] == "":
				label["noise_level"] = "clean"
			label["reviewed"] = False
			labels.append(label)
	episode_data["labels"] = labels
	return episode_data

def import_from_json(filename):
	with open(filename) as f:
		episode_data = json.load(f)
	return episode_data

def check_progress(filename):
	episode_data = import_from_json(filename)
	a = 0
	b = len(episode_data["labels"])
	for l in episode_data["labels"]:
		if l["reviewed"] == True:
			a += 1
	if a == b:
		return 100
	else:
		return int((a/b)*99)

#Unfinished
def export_to_labels(episode_data):
	dirpath = os.path.dirname(os.path.realpath(__file__)) + "/exported_labels/"
	try:
		os.makedirs(dirpath)
	except: pass
	fullpath = dirpath + episode_data["label_name"] + "_export.txt"
	with open(fullpath, 'w') as f:
		for l in episode_data["labels"]:
			if l["noise_level"] == "noisy":
				noise = "Noisy"
			elif l["noise_level"] == "verynoisy":
				noise = "Very Noisy"
			else:
				noise = ""
			f.write(
				"{:.6f}".format(l["start"]) + "\t" + "{:.6f}".format(l["end"]) + "\t" + "xx_xx_xx_" 
				+ l["character"] + "_" + " ".join(l["mood"]).capitalize() + "_" + noise 
				+ "_" + l["transcript"] + "\n"
			)
	return fullpath

def export_to_json(episode_data):
	dirpath = os.path.dirname(os.path.realpath(__file__)) + "/saved_changes/"
	try:
		os.makedirs(dirpath)
	except: pass
	fullpath = dirpath + episode_data["label_name"] + ".json"
	with open(fullpath, 'w') as f:
		json.dump(episode_data, f, indent=4)
	return fullpath

def hash_audio_files(queue):
	new_audio = 0
	queue.put("Hashing audio files...")
	for p in config["audio_paths"]:
		for r, _, f in os.walk(p):
			for file in f:
				if '.flac' in file:
					if os.path.join(r, file) in config["audio_hashes"]:
						continue
					hasher = hashlib.sha1()
					with open(os.path.join(r, file), "rb") as openfile:
						readfile = openfile.read()
						hasher.update(readfile)
						hash = hasher.hexdigest()
						config["audio_hashes"][os.path.join(r, file)] = hash
						queue.put("Hashed " + file)
						new_audio += 1
	queue.put("Done! Found " + str(new_audio) + " new audio file(s)")
	write_config()
	queue.put("msgdone")
