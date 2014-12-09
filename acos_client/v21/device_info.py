
import base

class DeviceInfo(base.BaseV21):

        def get(self, **kwargs):
            return self._get('system.device_info.get', **kwargs)

        def cpu_current_usage(self, **kwargs):
            return self._get('system.device_info.cpu.current_usage.get',**kwargs)

        def cpu_historical_usage(self, **kwargs):
            return self._get('system.device_info.cpu.historical_usage.get',**kwargs)

