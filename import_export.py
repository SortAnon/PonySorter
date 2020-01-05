import csv
import os
import datetime
import hashes
import hashlib
import json
import math
import string
import ffmpeg
from jsonschema import validate

with open(os.path.dirname(os.path.realpath(__file__)) + "/pony_schema.json") as f:
    schema = json.load(f)
try:
    with open(os.path.dirname(os.path.realpath(__file__)) + "/settings.json") as f:
        config = json.load(f)
except:
    config = {
        "audio_paths": [],
        "audio_hashes": {},
    }


def write_config():
    path = os.path.dirname(os.path.realpath(__file__)) + "/settings.json"
    with open(path, "w") as f:
        json.dump(config, f, indent=4)
    return path


def import_from_labels(filename):
    episode_data = {}
    episode_data["label_name"] = os.path.splitext(os.path.basename(filename))[
        0
    ].replace(" ", "_")
    if episode_data["label_name"] not in hashes.friendly_names:
        return None
    episode_data["friendly_name"] = hashes.friendly_names[episode_data["label_name"]]
    episode_data["last_modified"] = datetime.datetime.utcnow().isoformat()
    labels = []
    with open(filename, encoding="utf-8") as f:
        for i in csv.reader(f, delimiter="\t"):
            label = {}
            label["start"] = float(i[0])
            label["end"] = float(i[1])
            label["character"] = i[2].split("_")[3]
            label["mood"] = i[2].split("_")[4].lower().split(" ")
            label["transcript"] = i[2].split("_")[6]
            label["noise_level"] = i[2].split("_")[5].replace(" ", "").lower()
            if label["noise_level"] == "":
                label["noise_level"] = "clean"
            label["reviewed"] = False
            labels.append(label)
    episode_data["labels"] = labels
    return episode_data


def import_from_json(filename):
    with open(filename, encoding="utf-8") as f:
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
        return int((a / b) * 99)


def generate_label_filename(l):
    if l["noise_level"] == "noisy":
        noise = "Noisy"
    elif l["noise_level"] == "verynoisy":
        noise = "Very Noisy"
    else:
        noise = ""
    hour = int(math.floor(round(l["start"]) / 3600))
    minute = int(math.floor(round(l["start"]) / 60 % 60))
    second = int(math.floor(round(l["start"]) % 60))
    name = (
        "{0:02d}".format(hour)
        + "_"
        + "{0:02d}".format(minute)
        + "_"
        + "{0:02d}".format(second)
        + "_"
        + l["character"]
        + "_"
        + string.capwords(" ".join(l["mood"]))
        + "_"
        + noise
        + "_"
        + l["transcript"]
        + "\n"
    )
    return name


def generate_clean_filename(l, label_name):
    name = generate_label_filename(l)
    split = name.split(sep="_")
    for i, s in enumerate(split):
        split[i] = "".join(x for x in s if x.isalnum())
        split[i] = split[i][:32]
    name = "".join(x for x in label_name if x.isalnum()) + "_" + "_".join(split).lower()
    return name


def export_to_labels(episode_data, character_filter=None, source_filter=None):
    dirpath = os.path.dirname(os.path.realpath(__file__)) + "/exported_labels/"
    try:
        os.makedirs(dirpath)
    except:
        pass
    if source_filter != None:
        fullpath = dirpath + episode_data["label_name"] + "_" + source_filter + ".txt"
    else:
        fullpath = dirpath + episode_data["label_name"] + ".txt"
    with open(fullpath, "w", encoding="utf-8") as f:
        missing_warning = False
        for l in episode_data["labels"]:
            if character_filter != None and l["character"] != character_filter:
                continue
            if source_filter != None and "ideal_source" not in l:
                if not missing_warning:
                    print("Warning: missing source(s) in " + episode_data["label_name"])
                    missing_warning = True
                continue
            if source_filter != None and l["ideal_source"] != source_filter:
                continue
            f.write(
                "{:.6f}".format(l["start"])
                + "\t"
                + "{:.6f}".format(l["end"])
                + "\t"
                + generate_label_filename(l)
            )
    return fullpath


def find_audio_path(episode_name):
    original_path = ""
    izo_path = ""
    unmix_path = ""
    original_hash = hashes.original_hashes[episode_name]
    izo_hash = hashes.izo_hashes[episode_name]
    unmix_hash = hashes.unmix_hashes[episode_name]
    for k, v in config["audio_hashes"].items():
        if v == original_hash:
            original_path = k
        if v == izo_hash:
            izo_path = k
        if v == unmix_hash:
            unmix_path = k
    return (original_path, izo_path, unmix_path)


def split_by_pony(
    episode_data,
    character_filter=None,
    mood_filter=[],
    allow_questions=True,
    default_source="izo",
):
    metadata = []
    dirpath = os.path.dirname(os.path.realpath(__file__)) + "/exported_clips/wavs/"
    try:
        os.makedirs(dirpath)
    except:
        pass
    original_path, izo_path, unmix_path = find_audio_path(episode_data["label_name"])
    for l in episode_data["labels"]:
        if character_filter != None and l["character"] != character_filter:
            continue
        if l["mood"][0] not in mood_filter:
            continue
        if not allow_questions and "?" in l["transcript"]:
            continue
        if "ideal_source" in l:
            source = l["ideal_source"]
        else:
            source = default_source
        if source == "original":
            inputfile = original_path
        elif source == "izo":
            inputfile = izo_path
        elif source == "unmix":
            inputfile = unmix_path
        filename = generate_clean_filename(l, episode_data["label_name"])
        ffmpeg.input(inputfile, ss=l["start"], t=l["end"] - l["start"]).output(
            dirpath + filename + ".wav", ar="22050"
        ).overwrite_output().run()
        metadata.append(filename + "|" + l["transcript"] + "|" + l["transcript"])
    return metadata


def export_to_json(episode_data):
    dirpath = os.path.dirname(os.path.realpath(__file__)) + "/saved_changes/"
    try:
        os.makedirs(dirpath)
    except:
        pass
    fullpath = dirpath + episode_data["label_name"] + ".json"
    with open(fullpath, "w", encoding="utf-8") as f:
        json.dump(episode_data, f, indent=4, ensure_ascii=False)
    return fullpath


def hash_audio_files(queue):
    new_audio = 0
    queue.put("Hashing audio files...")
    for p in config["audio_paths"]:
        for r, _, f in os.walk(p):
            for file in f:
                if ".flac" in file:
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


def get_chars_and_moods(filename):
    chars = set()
    moods = set()
    episode_data = import_from_json(filename)
    for l in episode_data["labels"]:
        chars.add(l["character"])
        for m in l["mood"]:
            moods.add(m)
    return chars, moods


def episode_format(name):
    if name.startswith("fim_s"):
        return "s" + str(int(name[5:7])) + "e" + str(int(name[8:10]))
    else:
        return name.replace("_", "")


def format_name(
    name_format,
    episode,
    number,
    seconds,
    character,
    moods,
    transcript,
    noise_level,
    audio_source,
    extension,
    filter_reserved,
    filter_space,
):
    # Prepare metadata
    if noise_level == "noisy":
        noise = "Noisy"
    elif noise_level == "verynoisy":
        noise = "Very Noisy"
    else:
        noise = ""
    hour = int(math.floor(round(seconds) / 3600))
    minute = int(math.floor(round(seconds) / 60 % 60))
    second = int(math.floor(round(seconds) % 60))

    # Format output string
    output = name_format
    output = output.replace("{h}", "{0:02d}".format(hour))
    output = output.replace("{m}", "{0:02d}".format(minute))
    output = output.replace("{s}", "{0:02d}".format(second))
    output = output.replace("{xs}", "{0:.3f}".format(seconds))
    output = output.replace("{num}", str(number))
    output = output.replace("{ep}", episode_format(episode))
    output = output.replace("{c}", character)
    output = output.replace("{md}", string.capwords(" ".join(moods)))
    output = output.replace("{md0}", string.capwords(moods[0]))
    output = output.replace("{t}", transcript)
    output = output.replace("{nl}", noise)
    output = output.replace("{src}", audio_source)
    if filter_reserved:
        reserved = ["<", ">", ":", '"', "/", "\\", "|", "?", "*", "\0"]
        for r in reserved:
            output = output.replace(r, "")
    if filter_space:
        output = output.replace(" ", "")
    return output.replace("/", "") + "." + extension.lower()

