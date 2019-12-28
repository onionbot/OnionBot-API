from thermal_camera import THERMAL_CAMERA as thermal_cam
from camera import CAMERA as normal_cam
import PIL.Image
import PIL.ImageEnhance
from cloud import CLOUD as cloud

import datetime 

cloud = cloud()

tc = thermal_cam(visualise_on=False)
nc = normal_cam()


time = datetime.datetime.now()

path1 = cloud.get_path("testsession", "nc", "jpg", time, "0")
n = nc.capture(path1)
#cloud.upload_from_filename(path1)


path2 = cloud.get_path("testsession", "tc", "jpg", time, "0")
tc.capture_frame()
t = tc.save_latest_jpg(path2)
#cloud.upload_from_filename(path2)

timg = PIL.Image.open(t).convert("RGBA")
nimg = PIL.Image.open(n).convert("RGBA")

# optional lightness of watermark from 0.0 to 1.0
#brightness = 0.5
#watermark = PIL.ImageEnhance.Brightness(watermark).enhance(brightness)

# apply the watermark
some_xy_offset = (0, 0) #10, 20
# the mask uses the transparency of the watermark (if it exists)
#nimg.paste(timg, some_xy_offset, mask=timg)

nimg = PIL.Image.blend(nimg, timg, 0.5)

nimg.show()
nimg.save('calibration_image.png')
