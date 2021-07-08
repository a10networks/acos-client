# Copyright 2021,  Jeff Buttars,  A10 Networks.
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
from __future__ import absolute_import
from __future__ import unicode_literals


def acos_version_str2int(ver):
    if ver.isdigit():
        return int(ver)
    else:
        vnum = ""
        for index in range(len(ver)):
            if ver[index].isdigit():
                vnum = vnum + ver[index]
            else:
                break
        return int(vnum)


def acos_revision_parse(revision):
    rev = []
    revision_list = ['GR', 'P', 'SP']
    for tag in revision_list:
        tag_index = revision.find(tag)
        if tag_index >= 0:
            tag_len = len(tag)
            rev.append(acos_version_str2int(revision[(tag_index + tag_len):]))
        else:
            rev.append(0)

    return tuple(rev)


def acos_version(acos_version):
    major = acos_version_str2int(acos_version.split('.')[0])
    minor = acos_version_str2int(acos_version.split('.')[1])
    patch = acos_version_str2int(acos_version.split('.')[2])

    revision = ""
    prev = acos_version.find('-')
    if prev > 0:
        revision = acos_version[prev + 1:]
    gr, p, sp = acos_revision_parse(revision)

    return (major, minor, patch, gr, p, sp)


def acos_version_cmp(ver1, ver2):
    vtup1 = acos_version(ver1)
    vtup2 = acos_version(ver2)
    for index in range(len(vtup1)):
        if vtup1[index] != vtup2[index]:
            return vtup1[index] - vtup2[index]
    return 0
