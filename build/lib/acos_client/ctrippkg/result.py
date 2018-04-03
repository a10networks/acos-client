# coding=utf-8


class Result(object):
    code_message_map = {
        0: 'ok',
        # --------------COM Error-------------------------
        150: 'get url [%s] redis config error!',
        151: 'redis does not contain Servers key',
        152: 'canread should be boolean',
        153: 'redis server is empty, can not init redis connection!',
        154: 'connection redis server  error! [%s]',
        155: 'key is none while write data to redis',
        156: 'data is none while write data to redis, ignore write action!',
        160: 'clusterid [ %s ] not found in db!',
        199: '[%s]'
    }

    def __init__(self, code, msg=None):
        self.message = self.code_message_map[code] if code in self.code_message_map.keys() \
            else 'Invalid error number'
        if code in self.code_message_map.keys():
            self.code = code
            self.message = self.code_message_map[code]
        elif msg:
            self.code = code
            self.message = msg
        else:
            self.code = code
            self.message = 'Invalid error number'
        self.response = True if code in [0, ] else False

    def __str__(self):
        return repr(self.message)

    def get_result(self, param=None):
        if '%s' in self.message and param and (isinstance(param, str) or isinstance(param, unicode)):
            self.message = self.message % param
        return {
            'code': self.code,
            'status': self.response,
            'message': self.message
        }


class ResponseResult(object):
    def __init__(self):
        self.data = []
        self.status = True
        self.total = 0
        self.message = 'ok'

    def __str__(self):
        return repr(self.message)

    def get_response(self, resultobj):
        if resultobj["code"] != 0:
            self.status = False
            self.message = str(resultobj["message"])
        elif resultobj["code"] == 0:
            data = resultobj["message"]
            self.data = data if isinstance(data, list) else [data]
            self.data = [{i[0]: i[1]} for i in data.items()] if isinstance(data, dict) else self.data
            self.total = len(self.data)
        return {
            'data': self.data,
            'status': self.status,
            'total': self.total,
            'message': self.message
        }

    def get_new_response(self, resultobj):
        if resultobj["code"] != 0:
            self.status = False
            self.message = str(resultobj["message"])
        elif resultobj["code"] == 0:
            data = resultobj["message"]
            self.data = data if isinstance(data, list) else [data]
            self.data = [data] if isinstance(data, dict) else self.data
            self.total = len(self.data)
        return {
            'data': self.data,
            'status': self.status,
            'total': self.total,
            'message': self.message
        }

    def get_dict_response(self, resultobj):
        if resultobj["code"] != 0:
            self.status = False
            self.message = str(resultobj["message"])
            self.data = {}
        elif resultobj["code"] == 0:
            data = resultobj["message"]
            self.data = data if isinstance(data, dict) else {"message": data}
            # self.data = [{i[0]: i[1]} for i in data.items()] if isinstance(data, dict) else self.data
            self.total = len(self.data.keys())
        return {
            'data': self.data,
            'status': self.status,
            'total': self.total,
            'message': self.message
        }

    def get_data_response(self, resultobj):

        if resultobj["code"] != 0:
            self.status = False
            self.message = str(resultobj["message"])
        elif resultobj["code"] == 0:
            self.data = resultobj["data"]
            self.total = len(self.data.keys())

        return {
            'data': self.data,
            'status': self.status,
            'total': self.total,
            'message': self.message
        }