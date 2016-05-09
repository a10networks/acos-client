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

import collections
import copy

CLEAN_FIELDS = ["username", "password"]

REPLACEMENT = "*" * 8
PRIMITIVES = [int, float, str]


def clean(data, field=None):
    if field in CLEAN_FIELDS:
        return REPLACEMENT

    if type(data) is dict:
        return dict(
            (x, clean(y, field=x))
            for x, y in data.iteritems()
            )
    elif issubclass(type(data), str):
        return data
    elif issubclass(type(data), collections.Iterable):
        return type(data)(clean(x) for x in data)
    elif hasattr(data, "__dict__"):
        data = copy.copy(data)
        for x, y in data.__dict__.iteritems():
            setattr(data, x, clean(y, field=x))
        return data

    return data
