This repository contains a watcher to be used to potentially automatically restart wifi on losing connection, and a script that connects to an onboard computer and sync the time on doing so. For now this scripts requires ssh keys inside de remote machine until I get the password piping working. 

### Remote conexion via wifi with QGC (EXECUTED IN REMOTE MACHINE)

```mavproxy.py --master=/dev/ttyACM0 --baudrate 115200  --out 192.168.0.130:14550```

### In order to get a file via SCP from remote machine (EXECUTED IN GROUND MACHINE)

```scp cvar@address.local:/path/file /home/user/destination/```

### In order to change fan control

https://docs.nvidia.com/jetson/archives/r34.1/DeveloperGuide/text/SD/PlatformPowerAndPerformance/JetsonOrinNxSeriesAndJetsonAgxOrinSeries.html#nvfancontrol
