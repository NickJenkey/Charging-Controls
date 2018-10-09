# Charging-Controls
Python script config file and notes for control of Victron Energy Storage System over a network from connected linux NAS
This is a small project that has been written to control a Victron inverter based on time of day and season of the year to maximise use of solar PV energy and cheap ovenight energy
the project may develop to include the ability to interact with the potential variable tarrifs becoming available in the UK
It is also hoped to run the project on the "Color Control" unit which is the main control unit in the Victron ESS system but at present it runs on a NAS unit connected to the same LAN with a python module, the intention was to ensure that if the code is FUBAR then it wont break a functioning system as supplied by the hardware manufacturer
The Inveretr charges a lithium ion battery from surplus solar and when energy is cheap to use later
Huge thanks to AB for his input in making this code work and helping me on first baby steps in this area!
