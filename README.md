# OnionBot | An open source collaborative cooking robot 
An assistive stove-top cooking device with machine vision - for domestic automation research
[See it in action](https://youtu.be/poE4O6JZY0E)

<p float="left">
    <img src="https://www.raspberrypi.org/wp-content/uploads/2011/10/Raspi-PGB001.png" height="100"/>
    <img src="https://www.nasuni.com/wp-content/uploads/2019/10/googleCloudPartner.png" height="100"/>
    <img src="https://miro.medium.com/max/400/0*xNxZokzztcgpPueM.png" height="100"/>
</p>


### To start the API 
Script will run on boot. Otherwise SSH into Pi 
1. `ssh USER@YOUR_PI`
2. `cd onionbot`
3. `. runonion`

### To connect to the web portal
1. Start your local web server of choice (we use Apache)
2. Point the server to `onionbot/portal`
3. Start cooking! 

### Dependencies
1. `pip3 install pillow`
2. `pip3 install adafruit-circuitpython-mlx90640`
3. `pip install Adafruit-Blinka`
4. [Tensorflow install guide](https://www.tensorflow.org/lite/models/image_classification/overview)
5. [Servo driver install](http://parallax.com/product/900-00008)

### 3D Files
Visit [3d_files folder](https://github.com/bencobley/onionbot/tree/master/3d_files) to view 3D stls.

### System structure
![Screenshot 2020-06-09 at 21 40 54](https://user-images.githubusercontent.com/32883278/84198237-270c6d00-aa9b-11ea-9481-0a2cd971f2a7.png)

`API.py` Access the OnionBot portal over the local network

`camera.py` Control the camera using the Picamera module (threaded)

`classification.py` Classify images with TensorFlow and the Coral Edge TPU (threaded)

`cloud.py` Upload images to Google Cloud storage buckets (threaded)

`config.json` Configure settings, labels and models

`config.py` Interface with the `config.json` file 

`control.py` Wrapper for PID module, manage control data structures for `main.py`

`data.py` Manage data structures and metadata for API

`knob.py` Wrapper for servo module to control hob temperature setting (threaded)

`launcher.py` Launch OnionBot software from the big red button

`lib_para_360_servo.py` Parallax 360 [servo drivers](http://parallax.com/product/900-00008)

`main.py` Main script (threaded)

`pid.py` Proportional Integral Derivative hob temperature controller (threaded)

`runlauncher` Launch big red button listener script

`runonion` Launch OnionBot software

`thermal_camera.py` Wrapper for the Adafruit MLX90640 thermal camera module (threaded)


