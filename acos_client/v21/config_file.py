
import base

class ConfigFile(base.BaseV21):

    def upload(self, cfg_backup, **kwargs):
        return self._post("system.config_file.upload", cfg_backup, **kwargs)

    def restore(self, **kwargs):
        return self._post("system.config_file.restore", **kwargs)

    def write(self, from_file, to_file, **kwargs):
        return self._post("system.config_file.write", {"from": from_file, "to": to_file}, **kwargs)
