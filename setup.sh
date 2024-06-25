pactl load-module module-null-sink \
   sink_name=mix-for-virtual-mic \
   sink_properties=device.description=Mix-for-Virtual-Microphone

pactl load-module module-pipe-source \
   source_name=virtmic \
   file=/home/pyle/dev/virtmic format=s16le rate=16000 channels=1

pactl load-module module-combine-sink \
   sink_name=virtual-microphone-and-speakers \
   slaves=mix-for-virtual-mic

pactl load-module module-remap-source \
   master=mix-for-virtual-mic.monitor \
   source_properties=device.description=mixed-mic

pactl load-module module-loopback \
    source=mix-for-virtual-mic.monitor.remapped \
    sink=@DEFAULT_SINK@