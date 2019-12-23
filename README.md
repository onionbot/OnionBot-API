# onionbot
BEN COBLEY - DE4 SOLO PROJECT 

### Running camera plus thermal feed 
Update csv
1. `cd ~/onionbot/mlx90640-library/examples`
2. `./thermalcam`

Start visualisation
1. `cd ~/onionbot/mlx90640-library/python/`
2. `workon cv`
3. `LD_PRELOAD=/usr/lib/arm-linux-gnueabihf/libatomic.so.1.2.0 python thermalcam.py`
