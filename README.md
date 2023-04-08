# GTA-V Live Data Collection

This is used to collect images and keys pressed sample by playing GTA-V.<br />
The countdown will be 10 seconds before the game start being recorded.<br />
The data will saved in dataset directory.<br />
Inside dataset directory, images directory contain the images and labels directory contains a keys.csv file which contains the key mapping.<br />
<br />
While recording the game, "T" key is used to pause/unpause the recording and "Q" key is used to stop the recording.<br />
The dataset comprises of four labels:
- *Throttle Value* is the value of the acceleration the car is in. Throttle value 1.0 means forward acceleration, 0.0 means backward acceleration and 0.5 means no acceleration.
- *Throttle Flag* is a boolean value which states whether there is an acceleration.
- *Steering Value* is the value of the steering of the car. Steering value 1.0 means left steering, 0.0 means right steering and 0.5 means no steering.
- *Steering Flag* is a boolean value which states whether there is an steering.
