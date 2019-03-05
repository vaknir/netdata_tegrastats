# -*- coding: utf-8 -*-
# Description: tegrastat netdata python.d module
# Original Author: Nir Vaknin

import subprocess
import threading
import xml.etree.ElementTree as et

from bases.collection import find_binary
from bases.FrameworkServices.SimpleService import SimpleService

disabled_by_default = True

TEGRASTATS = '/home/nvidia/tegrastats'


GPU_LOAD_PERCENT = "gpu_load"
FAN_SPEED_RPM = "fan_speed"
GPU_GHZ_FREQ = "gpu_freq"

GPU_LOAD = '/sys/devices/gpu.0/load'
FAN_SPEED = '/sys/kernel/debug/tegra_fan/target_pwm'
GPU_FREQ = '/sys/devices/gpu.0/devfreq/17000000.gv11b/cur_freq'


ORDER = [
    GPU_LOAD_PERCENT,
  #  FAN_SPEED_RPM,
    GPU_GHZ_FREQ
]

CHARTS = {
    GPU_LOAD_PERCENT: {
        'options': [None, 'Gpu load','percentage','Tegra GPU Usage', 'gpu_load','stacked'],
        'lines':[
            ['gpu_load','load','absolute']
        ]
    },
    FAN_SPEED_RPM: {
        'options': [None, 'Fan speed', 'RPM', 'Tegra Fan Speed', 'gpu_fan_speed','stacked'],
        'lines': [
            ['gpu_fan_speed','rpm','absolute']
        ]
    },
    GPU_GHZ_FREQ: {
        'options': [None, 'GPU Mhz', 'Mhz', 'Tegra Gpu Freq', 'gpu_freq', 'stacked'],
        'lines': [
            ['gpu_freq','Mhz','absolute']
        ]
    }
}


class Service(SimpleService):
    def __init__(self, configuration=None, name=None):
        SimpleService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
        poll = int(configuration.get('poll_seconds', 1))

    def check(self):
        return True

    def _get_data(self):
        data = dict()
        data_1 = dict()
        data['gpu_load'] = self.get_gpu_load()
 #       data['gpu_fan_speed'] = self.get_gpu_fan()
        data['gpu_freq'] = self.get_gpu_freq()
        return data or None

    def get_gpu_load(self):
        proc = subprocess.Popen(['cat', GPU_LOAD], stdout=subprocess.PIPE)
        stdout, _ = proc.communicate()
        load = int(stdout) /  10
        return load

    def get_gpu_fan(self):
        proc = subprocess.Popen(['sudo', 'cat', FAN_SPEED], stdout=subprocess.PIPE)
        stdout, _ = proc.communicate()
        return stdout

    def get_gpu_freq(self):
        freq_cmd = subprocess.Popen(['cat', GPU_FREQ], stdout=subprocess.PIPE)
        stdout, _ = freq_cmd.communicate()
        freq = float(stdout)
        return (freq / 1000000 )

