# Pony Sorter
A faster way to review the existing labels and select the cleanest audio source.

## Getting started
* Clone the repo. Optionally, Windows users can download the binary release.
* Copy the label files from Clipper's MEGA resource to /labels.
* Run ```pip3 install -r requirements.txt```, followed by ```python3 ponysorter_gui.py```. (Or run ponysorter_gui.exe on Windows)
* Download the original audio files. You can find seasons 1-8 in the Google Docs document.
* Download the iZotope filtered audio from Clipper's MEGA.
* Download the Open-Unmix filtered audio from my MEGA.
* Go to Edit -> Add audio path(s). Paste the path or paths where the audio files are stored.
* Wait ~5 minutes for the files to get hashed. The hashes are loaded from settings.json the next time you run the program.
* Go to Edit -> Load episode. You should see a list of all episodes from seasons 1-6, episode 22-26 of season 9, and four Equestria Girls movies.
* Load an episode. It will take ~30 seconds to load the audio, during which the UI will be frozen.
* If everything worked correctly, the three Listen buttons at the top should play audio when clicked.

## How to use
* Load an episode. You can either click the buttons at the top, or use the numeric keys as indicated.
* Listen to all three versions of the line.
* Adjust the metadata as necessary.
* Select the audio source that strikes the best balance between quality and noise reduction.
* If you made a mistake, use the leftmost button to go back a line.
* When all lines have been reviewed, go to Edit -> Save changes (or press Ctrl+S) to save your changes. 
* You can also save your progress in the middle of an episode, and return to it later.
* The files are stored in /saved_changes. Upload completed episodes and post them to the thread.
