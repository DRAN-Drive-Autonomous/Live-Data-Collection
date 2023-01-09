# GTA-V Live Data Collection

This is used to collect images and keys pressed sample by playing GTA-V.<br />
The countdown will be 10 seconds before the game start being recorded.<br />
The data will saved in dataset directory.<br />
Inside dataset directory, images directory contain the images and labels directory contains a keys.csv file which contains the key mapping.<br />
<br />
While recording the game, "T" key is used to pause/unpause the recording and "Q" key is used to stop the recording.
The game will record a total of 10 key-press behaviours which contain:

Key Behaviour Label  | Description
------------- | -------------
W |when W key is pressed.
A |when A key is pressed.
S |when S key is pressed.
D |when D key is pressed.
WA |when both W and A keys are pressed.
WD |when both W and D keys are pressed.
SA |when both S and A keys are pressed.
SD |when both S and D keys are pressed.
Space |when SPACE key is pressed.
No Key |when no key is pressed.
