![Header](https://user-images.githubusercontent.com/32883278/97621285-a4208a80-1a1a-11eb-8b7f-90141d867982.png)

# OnionBot | Python API

<p float="left">
    <img src="https://www.raspberrypi.org/wp-content/uploads/2011/10/Raspi-PGB001.png" height="100"/>
    <img src="https://www.nasuni.com/wp-content/uploads/2019/10/googleCloudPartner.png" height="100"/>
    <img src="https://miro.medium.com/max/400/0*xNxZokzztcgpPueM.png" height="100"/>
    <img src="https://user-images.githubusercontent.com/32883278/84203339-32fb2d80-aaa1-11ea-843e-f7f69da66e53.png" height="50"/>
</p>

*A collaborative computational cooking robot using computer vision built with Raspberry Pi*

Python API integrating sensors, actuators and interfaces

[See it in action on YouTube](https://youtu.be/W4utRCyo5C4) | 
[Read more about the project on DesignSpark](https://www.rs-online.com/designspark/student-innovation-onionbot-building-a-robot-sous-chef)

### About 
*How can we apply robotics to home cooking?*

Automation tech in the food industry is well known to reduce physical and cognitive demands on production-line operators. Perhaps the same technology could also reduce errors and help decision-making for home cooking? For example, how might robots augment the cooking skills of busy parents and professionals?

The problem: kitchens pose very different design engineering challenges to production lines, because home cooking requires multi-purpose tools, not specialised machines. Robot arms can mimic human-kitchen interaction, but these are currently far too large and expensive to be feasible for the home. For multi-purpose sensing, cameras can detect a wide variety of cooking information, but there are currently no datasets for training cooking image classification algorithms.

![Hardware](https://user-images.githubusercontent.com/32883278/97621266-9ec34000-1a1a-11eb-82a4-4ef906dfa522.png)

*Prototyping integration of industry automation techniques and machine vision into a simple robot that fits on a countertop.*

### System structure
![system2](https://user-images.githubusercontent.com/32883278/97644851-4d7b7680-1a43-11eb-94a6-876e7f35183a.png)

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

### Dependencies

1. `pip3 install pillow`
2. `pip3 install adafruit-circuitpython-mlx90640`
3. `pip install Adafruit-Blinka`
4. [Tensorflow install guide](https://www.tensorflow.org/lite/models/image_classification/overview)
5. [Servo driver install](http://parallax.com/product/900-00008)


### The OnionBot idea was developed through a research project at Imperial College London

Check out the paper for technical details in much more depth!

[OnionBot: A System for Collaborative Computational Cooking - ArXiv](https://arxiv.org/pdf/2011.05039.pdf)

![arxiv](https://user-images.githubusercontent.com/32883278/98860117-18b3ea00-245b-11eb-976e-163721560a50.png)


### Interested in building a cooking automation robot?

Get in touch! 
