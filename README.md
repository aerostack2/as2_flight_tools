This repository contains a watcher to be used to potentially automatically restart wifi on losing connection, and a script that connects to an onboard computer and sync the time on doing so. For now this scripts requires ssh keys inside de remote machine until I get the password piping working. 

### Remote conexion via wifi with QGC (EXECUTED IN REMOTE MACHINE)

```mavproxy.py --master=/dev/ttyACM0 --baudrate 115200  --out 192.168.0.130:14550```

### In order to get a file via SCP from remote machine (EXECUTED IN GROUND MACHINE)

```scp cvar@address.local:/path/file /home/user/destination/```

### In order to change fan control

[Link to docs](https://docs.nvidia.com/jetson/archives/r34.1/DeveloperGuide/text/SD/PlatformPowerAndPerformance/JetsonOrinNxSeriesAndJetsonAgxOrinSeries.html#nvfancontrol)

Fan Profile Control
-----------------

Jetson Orin supports two profiles of fan operation named â€œquietâ€ and
â€œcool.â€

Userspace Fan speed control daemon `nvfancontrol <#nvfancontrol>`__ manages fan speed
based on the trip point temperatures configured for the selected profile.

Fan Profile Configuration
-----------------

Every fan speed step is associated with the trip point temperature and
corresponding hysteresis. 

The framework implements hysteresis to prevent frequent changes in fan
speed. For Jetson Orin, as an example, when fan
profile is set to â€œquietâ€ with the default settings shown above, the
framework performs these actions:

- Turns on the fan when the temperature rises to 50\ |degC|
- Turns off the fan when the temperature falls to 32\ |degC|
- Turns on the fan again when the temperature rises to 50\ |degC|, and so on

nvfancontrol
-----------------

nvfancontrol is a userspace fan speed control daemon.
This manages Fan speed based on Temperature to Fan speed mapping table in nvfancontrol configuration file.

nvfancontrol.conf
-----------------

- Location::

    /etc/nvfancontrol.conf

- Please find below the example nvfancontrol.conf file for the Jetson Orin::
    ```
    POLLING_INTERVAL 2
    <FAN 1>
        TMARGIN ENABLED
        FAN_GOVERNOR pid {
                STEP_SIZE 10
        }
        FAN_PROFILE cool {
                #TEMP   HYST    PWM     RPM
                0       0       255     2900
                18      9       255     2900
                30      11      202     2300
                45      11      149     1700
                60      14      88      1000
                105     0       0       0
        }
        FAN_PROFILE quiet {
                #TEMP   HYST    PWM     RPM
                0       0       202     2300
                18      9       202     2300
                30      11      158     1800
                45      11      114     1300
                60      14      62      700
                105     0       0       0
        }
        THERMAL_GROUP 0 {
                GROUP_MAX_TEMP 105
                #Thermal-Zone Coeffs Max-Temp
                CPU-therm 20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 0
                GPU-therm 20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 0
                SOC0-therm 20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 0
                SOC1-therm 20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 0
                SOC2-therm 20,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0 0
        }
        FAN_DEFAULT_CONTROL open_loop
        FAN_DEFAULT_PROFILE cool
        FAN_DEFAULT_GOVERNOR pid
        

Default Fan Profile
-----------------

For Jetson Orin the fan profile is set to â€œcoolâ€ by default. It is defined as ``FAN_DEFAULT_PROFILE`` in the configuration file ``/etc/nvfancontrol.conf``.

To change the default fan profile
-----------------

Please follow the below steps to change the Fan profile:

- Stop the ``nvfancontrol`` systemd service::

    sudo systemctl stop nvfancontrol

- Set the default fan profile by putting the following property in ``/etc/nvfancontrol.conf``::

    FAN_DEFAULT_PROFILE <fan_profile>

Where ``<fan_profile>`` is ``quiet`` or ``cool``.

- Remove the status file::

    sudo rm /var/lib/nvfancontrol/status

- Start the ``nvfancontrol`` systemd service::

    sudo systemctl start nvfancontrol

To identify the current fan profile
-----------------

- Enter the command::

    $ sudo nvfancontrol -q

- Example::

    $ sudo nvfancontrol -q
    FAN1:FAN_PROFILE:cool
    ...
    ...

Once you set a fan profile, the module stays in that profile until you change
it. The profile persists across power cycles.

Fan Profile Table
-----------------

Fan profile table contains the mapping between temperature and PWM value. It also
contains the hysteresis value for each step and the fan RPM value.

- Syntax::

        FAN_PROFILE <fan_profile_name> {
                <temp>  <hyst>  <pwm>   <rpm>
        }

        Where:
        <fan_profile_name>: Fan Profile Name
        <temp>: Temperation step in degree celcius
        <hyst>: Hysteresis step
        <pwm>:  Fan PWM value
        <rpm>:  Fan RPM value

- Example::

        FAN_PROFILE cool {
                #TEMP   HYST    PWM     RPM
                0       0       255     2900
                18      9       255     2900
                30      11      202     2300
                45      11      149     1700
                60      14      88      1000
                105     0       0       0
        }

Polling Interval
-----------------

nvfancontrol daemon polls the thermal zone temperatures at the time interval specified by POLLING_INTERVAL
and sets the Fan PWM value specified as per FAN PWM mapping table.

- Syntax::

    POLLING_INTERVAL <time_in_seconds>
