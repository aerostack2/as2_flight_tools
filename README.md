This repository contains a watcher to be used to potentially automatically restart wifi on losing connection, and a script that connects to an onboard computer and sync the time on doing so.

In order for this script to work, please install expect package with ```sudo apt install expect```

### Remote conexion via wifi with QGC (EXECUTED IN REMOTE MACHINE)

```mavproxy.py --master=/dev/ttyACM0 --baudrate 115200  --out 192.168.0.130:14550```

### In order to get a file via SCP from remote machine (EXECUTED IN GROUND MACHINE)

```scp cvar@address.local:/path/file /home/user/destination/```

### In order to change fan control

https://docs.nvidia.com/jetson/archives/r34.1/DeveloperGuide/text/SD/PlatformPowerAndPerformance/JetsonOrinNxSeriesAndJetsonAgxOrinSeries.html#nvfancontrol
