# Copyright 2016, All Rights Reserved,  A10 Networks.
#
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

import copy

CLEAN_FIELDS = ["username", "password"]

REPLACEMENT = "*" * 8
PRIMITIVES = [int, float, str]


def clean(data):
    data = copy.copy(data)

    if type(data) is dict:
        for x, y in data.iteritems():
            if type(y) is dict:
                data[x] = clean(y)
            else:
                if x in CLEAN_FIELDS:
                    data[x] = REPLACEMENT
    elif hasattr(data, "__dict__"):
        for x, y in data.__dict__.iteritems():
            if type(y) is dict or hasattr(y, "__dict__"):
                setattr(data, x, clean(y))
            else:
                if x in CLEAN_FIELDS:
                    setattr(data, x, REPLACEMENT)
    return data
