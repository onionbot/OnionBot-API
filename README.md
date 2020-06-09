![alt text](https://github.com/bencobley/onionbot/blob/master/img/portal.png)

# onionbot | DE4 SOLO and SIOT projects
A streamlined data collection, labelling and training platform for cooking data. Built with Raspberry Pi. 
[See it in action](https://youtu.be/l-FsY-qU2Vw)

<p float="left">
    <img src="https://www.raspberrypi.org/wp-content/uploads/2011/10/Raspi-PGB001.png" height="100"/>
    <img src="https://www.nasuni.com/wp-content/uploads/2019/10/googleCloudPartner.png" height="100"/>
    <img src="https://miro.medium.com/max/400/0*xNxZokzztcgpPueM.png" height="100"/>
</p>


### To start the API 
Script will run on boot. Otherwise SSH into Pi 
1. `ssh pi@onionpi`
2. `cd onionbot`
3. `python3 API.py`

### To use the web portal
1. Start a MAMP <mamp.info> local server environment
2. In your browser, navigate to `0.0.0.0:5000/portal`
3. Start collecting data! 

### Dependencies
1. `pip3 install pillow`
2. `pip3 install adafruit-circuitpython-mlx90640`
3. `pip install Adafruit-Blinka`
4. [Tensorflow install guide](https://www.tensorflow.org/lite/models/image_classification/overview)
5. [Servo driver install](http://parallax.com/product/900-00008)

### Implementation
![alt text](https://github.com/bencobley/onionbot/blob/master/img/hardware.jpg)
