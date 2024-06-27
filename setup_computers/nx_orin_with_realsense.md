# Setup XAVIER ORIN NX 

## 1. Load Jetpack 6.0 or superior in the board

You should use NVIDIA SDK Manager to upload the firmware.

For the Developer Board you may follow [Waveshare Instructions](https://www.waveshare.com/wiki/JETSON-ORIN-NX-16G-DEV-KIT)

## 2. Update board

```
sudo apt update && sudo apt upgrade -y 
```

## 3. Install ROS 2 Humble from Debian packages

Follow [Offical ROS 2 Humble setup Instructions](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debians.html)

## 4. Download Aerostack2 and platform

You can follow [Aerostack2 setup guide](https://aerostack2.github.io/_00_getting_started/source_install.html) for installing and setting up aerostack2.

### 4.1 Setup Platform (MavRos) 

In this example we will load mavros platform 

```
cd ~/aerostack2_ws/src/
git clone git@github.com:aerostack2/as2_platform_mavlink.git
cd ~/aerostack2_ws
rosdep install -y -r -q --from-paths src --ignore-src
```

We need to update the geometry lib database with 

```
cd ~/Downloads
wget https://raw.githubusercontent.com/mavlink/mavros/ros2/mavros/scripts/install_geographiclib_datasets.sh
chmod +x install_geographiclib_datasets.sh
sudo ./install_geographiclib_datasets.sh
```

Finally compile the platform

```
as2 build as2_platform_mavlink

```

Additionally we recommend to enable all the requirements for connecting to the autopilot and to mavproxy to visualize with QgroundControl.

Read more info in  [QgroundControl Setup](https://docs.qgroundcontrol.com/master/en/qgc-user-guide/getting_started/download_and_install.html), [Mavproxy install](https://ardupilot.org/mavproxy/docs/getting_started/download_and_installation.html)

> For telemetry forwarding see [Mavproxy Forwarding](https://ardupilot.org/mavproxy/docs/getting_started/forwarding.html)

```
# Enable dialout group
sudo usermod -a -G dialout $USER
sudo apt-get remove modemmanager -y

# Mavproxy 
sudo apt-get install python3-dev python3-opencv python3-wxgtk4.0 python3-pip python3-matplotlib python3-lxml python3-pygame
pip3 install PyYAML mavproxy --user
echo 'export PATH="$PATH:$HOME/.local/bin"' >> ~/.bashrc
```

> IMPORTANT: Restart the computer after this to take effect.

### 4.2 Setting up REALSENSE T265
> Intel realsense T265 has been discontinued so the latest versions of the ```librealsense2``` do not support it, that is why we shall make this steps

```
# First uninstall ros-humble-realsense package
sudo apt-get remove ros-humble-librealsense2 -y

# install an older version

sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE
sudo add-apt-repository "deb https://librealsense.intel.com/Debian/apt-repo bionic main" -u
sudo apt-get install librealsense2=2.53.1-0~realsense0.703  -y 
sudo apt-get install librealsense2-gl=2.53.1-0~realsense0.703  -y 
sudo apt-get install librealsense2-utils=2.53.1-0~realsense0.703  -y
sudo apt-get install librealsense2-dev=2.53.1-0~realsense0.703  -y
```

# Recompile as2_realsense_interface

```
as2 clean as2_realsense_interface
as2 build as2_realsense_interface
```

> IMPORTANT: Restart the computer after this to take effect.



### 4.3 Setting up CycloneDDS and Zenoh-ros2-bridge


We will follow [zenoh plugin ros2dds setup instuctions](https://github.com/eclipse-zenoh/zenoh-plugin-ros2dds?tab=readme-ov-file#linux-debian).

```
echo "deb [trusted=yes] https://download.eclipse.org/zenoh/debian-repo/ /" | sudo tee -a /etc/apt/sources.list > /dev/null
sudo apt update
sudo apt install ros-humble-rmw-cyclonedds-cpp zenoh-bridge-ros2dds -y

echo 'export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp' >> ~/.bashrc
echo 'export ROS_LOCALHOST_ONLY=1' >> ~/.bashrc
```

After this we sould enable multicast for Loopback in order to perform propperly. For enable it from start use:

```
sudo sh -c 'echo "#!/bin/sh \nip l set lo multicast on" > /etc/rc.local'

sudo chmod +x /etc/rc.local
```
> IMPORTANT: Restart the computer after this to take effect.

## 5 Additional programs

Some interesting improvements are

```
sudo apt install tmux tmuxinator python3 vctools -y
```

For easing the mavproxy launch you can add the following lines to the end of ```~/.bashrc``` file

```
alias get_connection_ip="echo $(echo $SSH_CONNECTION | awk '{print $1}')"                            
alias get_acm='ls /dev/ttyACM*'                                                                      
alias mavproxy_connect='mavproxy.py --master=$(get_acm) --baudrate 115200  --out $(get_connection_ip):14550'
```

with these you can only run 
```
# To broadcast the mavproxy to the computer that has stablished the ssh conenction
$ mavproxy_connect 
```

# Troubleshooting

1. Realsense not detected:  Un-plug the USB and plug it again (yes this should work) 

