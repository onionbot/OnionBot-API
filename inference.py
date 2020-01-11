# python3
#
# Copyright 2019 The TensorFlow Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Example using TF Lite to classify objects with the Raspberry Pi camera."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import time
import numpy as np

from PIL import Image
from tflite_runtime.interpreter import Interpreter



class Classify(object):


    def __init__(self, labels, model):

        self.labels = self.load_labels(labels)

        interpreter = Interpreter(model)
        interpreter.allocate_tensors()
        self.interpreter = interpreter

        _, self.height, self.width, _ = interpreter.get_input_details()[0]['shape']

    
    def load_labels(self, path):
        with open(path, 'r') as f:
            return {i: line.strip() for i, line in enumerate(f.readlines())}


    def set_input_tensor(self, interpreter, image):
        tensor_index = interpreter.get_input_details()[0]['index']
        input_tensor = interpreter.tensor(tensor_index)()[0]
        input_tensor[:, :] = image


    def classify_image(self, imagefilepath, top_k=1):
        """Returns a sorted array of classification results."""
        image = Image.open(imagefilepath).convert('RGB').resize((self.width, self.height),Image.ANTIALIAS)

        interpreter = self.interpreter

        self.set_input_tensor(interpreter, image)
        interpreter.invoke()
        output_details = interpreter.get_output_details()[0]
        output = np.squeeze(interpreter.get_tensor(output_details['index']))

        # If the model is quantized (uint8 data), then dequantize the results
        if output_details['dtype'] == np.uint8:
            scale, zero_point = output_details['quantization']
            output = scale * (output - zero_point)

        ordered = np.argpartition(-output, top_k)
        
        result = [(self.labels[i], output[i]) for i in ordered[:top_k]][0] # Only returns single result, assumes top_k = 1
        
        
        return F"{result[0]}_{"{:.2f}".format(result[1])}" 









