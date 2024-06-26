# tts-through-mic
Attempt to make a quick utility software which allows me to pipe TTS into a virtual microphone

# Requirements
- Using pulseaudio on your device
- Dependencies (see nix-shell file for easy usage)

# Usage
```
python run.py
```
will run the minimal GUI

Clicking the Initialise button should do all the pulseaudio work to set up virtual microphones as new devices (This will create new audio devices in your audio settings!)
You may need to restart every app that should recognise these new audio devices.

The default usage of this app is to create these virtual devices once and then leave them be.
If you really hate them: To get rid of these devices you can use "Remove Virtual Devices".


# Modifying the script
You will want to probably modify ``main.py``:
- ``process_text`` if you want to change the text you actually write into something else by the TTS voice
- ``MainWindow.speak_text`` handles TTS, you can change the voice here

