from .i2c_bus import bus
from .ads1015 import ads1015 as _ads1015
from .bmp280 import bmp280 as _bmp280
from .leds import leds as _leds
from .lsm303d import lsm303d as _lsm303d
from .tcs3472 import tcs3472 as _tcs3472


__version__ = '0.0.6'


_is_setup = False


class Default(object):
    """Default class to catch calls and ensure one-time setup.
    """

    def __init__(self, parent_name=None, **kwargs):
        object.__init__(self)
        self._parent_name = parent_name

    def _ensure_setup(self):
        if not _is_setup:
            setup()
        self._ensure_setup = lambda: globals()[self._parent_name]
        return globals()[self._parent_name]

    def __getattribute__(self, name):
        if name in ["_ensure_setup", "_parent_name"]:
             return object.__getattribute__(self, name)

        return self._ensure_setup().__getattribute__(name)

    def __repr__(self):
        return self._ensure_setup().__repr__()

    def __getitem__(self, item):
        return self._ensure_setup()[item]


leds = Default('leds')
light = Default('light')
weather = Default('weather')
analog = Default('analog')
motion = Default('motion')


def setup():
    global _is_setup, leds, light, weather, analog, motion

    if _is_setup:
        raise RuntimeError("")

    leds = _leds()
    light = _tcs3472(bus)
    weather = _bmp280(bus)
    analog = _ads1015(bus)
    motion = _lsm303d(bus)

    _is_setup = True

