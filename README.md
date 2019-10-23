# Pony Sorter
A faster way to review the existing labels and select the cleanest audio source.

## Getting started
* Clone this repo. Optionally, Windows users can download the binary release.
* Download all audio sources for the episodes you plan to work with. You can find a link to the uncleaned seasons 1-8 on Google Docs. The iZotope filtered audio is in Clipper's MEGA in the OP. The Open-Unmix filtered audio is in another MEGA, linked to in post 34429137 (thread 11).
* Download the label files from Clipper's MEGA, and copy them to /labels.
* Run ```pip3 install -r requirements.txt```, followed by ```python3 ponysorter_gui.py```. (Or run ponysorter_gui.exe on Windows)
* Go to Edit -> Add audio path(s). Paste the path or paths where the audio files are stored.
* Wait ~5 minutes for the files to get hashed. This is only done once for new files, and ensures that everyone is working with the same audio sources.
* Go to Edit -> Load episode. You should see a list of all episodes from seasons 1-6.

## How to use
* Load an episode. Check the thread to see who's working on what.
* Listen to all three versions of the line. You can either click the buttons at the top, or use the numeric keys as indicated.
* Adjust the label data if it's wrong.
* Select the audio source that strikes the best balance between quality and noise reduction.
* If you made a mistake, use the leftmost button to go back a line.
* When all lines have been reviewed, go to Edit -> Save changes (or press Ctrl+S) to save your changes. 
* You can also save your progress in the middle of an episode, and return to it later.
* The files are stored in /saved_changes. Upload the JSON files for completed episodes, and post them to the thread.

## Export options
### Split by pony
Automatically splits audio samples from all episodes for a selected pony, and generates metadata in LJ Speech format. This takes about 5 minutes.
Options are hardcoded for now: Twilight only, defaulting to iZotope for unreviewed lines.

### Generate combined source
Not yet implemented. Will create a single Frankenstein file for each episode with the cleanest audio source for each line.
Potentially useful for existing splitting scripts.

### Generate Audacity labels (current episode)
Exports the episode data loaded into memory to /exported_labels. 
Four files are created. Files suffixed "original", "izo" and "unmix" contain only the lines chosen for each source. The file without a suffix contains all lines.

### Generate Audacity labels (all episodes)
Same as above, but exports labels for all episodes. Save your changes before running this.
