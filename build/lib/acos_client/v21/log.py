#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import base


class Log(base.BaseV21):

        def set(self, sys_log, **kwargs):
            params = {"sys_log": sys_log}
            return self._post("system.log.set", params, **kwargs)

        def get(self, **kwargs):
            return self._get("system.log.get", **kwargs)

        def clear(self, sys_log, **kwargs):
            return self._post("system.log.clear", **kwargs)

        def download(self, **kwargs):
            return self._get('system.log.download', **kwargs)

        def backup(self, **kwargs):
            return self._post('system.log.backup', **kwargs)

        @property
        def level(self):
            return self.Level(self.client)

        @property
        def server(self):
            return self.Server(self.client)

        @property
        def buffer(self):
            return self.Buffer(self.client)

        @property
        def smtp(self):
            return self.Smtp(self.client)

        @property
        def audit(self):
            return self.Audit(self.client)

        class Level(base.BaseV21):
            def get(self, **kwargs):
                return self._get('system.log.level.get', **kwargs)

            def set(self, log_level, **kwargs):
                params = {"log_level": log_level}
                return self._post('system.log.level.set', params, **kwargs)

        class Server(base.BaseV21):
            def get(self, **kwargs):
                return self._get('system.log.server.get', **kwargs)

            def set(self, log_server, **kwargs):
                params = {"log_server": log_server}
                return self._post('system.log.server.set', params, **kwargs)

        class Buffer(base.BaseV21):
            def get(self, **kwargs):
                return self._get('system.log.buffer.get', **kwargs)

            def set(self, buff_size, **kwargs):
                params = {"buffer_size": buff_size}
                return self._post('system.log.buffer.set', params, **kwargs)

        class Smtp(base.BaseV21):
            def get(self, **kwargs):
                return self._get('system.log.smtp.get', **kwargs)

            def set(self, smtp, **kwargs):
                params = {"smtp": smtp}
                return self._post('system.log.smtp.set', params, **kwargs)

        class Audit(base.BaseV21):
            def get(self, **kwargs):
                return self._get('system.log.audit.get', **kwargs)

            def set(self, audit, **kwargs):
                params = {"audit": audit}
                return self._post('system.log.audit.set', params, **kwargs)
