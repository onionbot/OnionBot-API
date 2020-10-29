![Header](https://user-images.githubusercontent.com/32883278/97621285-a4208a80-1a1a-11eb-8b7f-90141d867982.png)

# OnionBot | Python API
*A collaborative computational cooking robot built with Raspberry Pi*

Python API integrating sensors, actuators and interfaces

[See it in action on YouTube](https://youtu.be/poE4O6JZY0E) | [Read the full project story on DesignSpark]https://www.rs-online.com/designspark/student-innovation-onionbot-building-a-robot-sous-chef


<p float="left">
    <img src="https://www.raspberrypi.org/wp-content/uploads/2011/10/Raspi-PGB001.png" height="100"/>
    <img src="https://www.nasuni.com/wp-content/uploads/2019/10/googleCloudPartner.png" height="100"/>
    <img src="https://miro.medium.com/max/400/0*xNxZokzztcgpPueM.png" height="100"/>
    <img src="https://user-images.githubusercontent.com/32883278/84203339-32fb2d80-aaa1-11ea-843e-f7f69da66e53.png" height="50"/>
</p>


### System
![Hardware](https://user-images.githubusercontent.com/32883278/97621266-9ec34000-1a1a-11eb-82a4-4ef906dfa522.png)


### Dependencies
1. `pip3 install pillow`
2. `pip3 install adafruit-circuitpython-mlx90640`
3. `pip install Adafruit-Blinka`
4. [Tensorflow install guide](https://www.tensorflow.org/lite/models/image_classification/overview)
5. [Servo driver install](http://parallax.com/product/900-00008)

Use `runonion` to start the API


### API structure
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


