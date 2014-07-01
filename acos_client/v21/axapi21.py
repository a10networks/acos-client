# Copyright 2013-2014,  Mike Thompson,  A10 Networks.
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

arg_templates = {
    'slb.server': {
        "server": {
            "name": "",
            "host": "",
            "gslb_external_address": "0.0.0.0",
            "weight": '',
            "health_monitor": "(default)",
            "status": 1,
            "conn_limit": '',
            "conn_limit_log": 1,
            "conn_resume": 0,
            "stats_data": 1,
            "extended_stats": 0,
            "slow_start": 0,
            "spoofing_cache": 0,
            "template": "default",
            "port_list": []
        }
    },
    'slb.server.port': {
        "port_num": '1-65535',
        "protocol": {'TCP': 2, 'UDP': 3},
        "status": 1,
        "weight": 1,
        "no_ssl": 0,
        "conn_limit": 8000000,
        "conn_limit_log": 1,
        "conn_resume": 0,
        "template": "default",
        "stats_data": 1,
        "health_monitor": "(default)",
        "extended_stats": 0
    },
    'slb.service_group': {
        "service_group": {
            "name": "",
            "protocol": '',
            "lb_method": {'RoundRobin': 0,
                          'WeightedRoundRobin': 1,
                          'LeastConnection': 2,
                          'WeightedLeastConnection': 3,
                          'LeastConnectionOnServicePort': 4,
                          'WeightedLeastConnectionOnServicePort': 5,
                          'FastResponseTime': 6,
                          'LeastRequest': 7,
                          'StrictRoundRobin': 8,
                          'StateLessSourceIPHash': 9,
                          'StateLessSourceIPHashOnly': 10,
                          'StateLessDestinationIPHash': 11,
                          'StateLessSourceDestinationIPHash': 12,
                          'StateLessPerPackageRoundRobin': 13},
            "health_monitor": "",
            "min_active_member": {
                "status": 0,
                "number": 0,
                "priority_set": 0
            },
            "backup_server_event_log_enable": 0,
            "client_reset": 0,
            "stats_data": 1,
            "extended_stats": 0,
            "member_list": []
        }

    },
    'slb.service_group.member': {
"name": "",
           "member": {"server": "", "port": "", "status": "1"}
    },
    'slb.virtual_server': {
"virtual_server": {
        "status": 1,
        "disable_vserver_on_condition": 0,
        "name": "foa",
        "vip_template": "default",
        "pbslb_template": "",
        "redistribution_flagged": 0,
        "extended_stats": 0,
        "ha_group": {
            "status": 0,
            "ha_group_id": 0,
            "dynamic_server_weight": 0
        },
        "arp_status": 1,
        "address": "192.168.212.121",
        "vport_list": [

        ],
        "stats_data": 1
    }
    },
    'slb.hm': {
       'retry': 3,
        'name': u'http_foo3',
        'consec_pass_reqd': 1,
        'interval': 5,
        'timeout': 5,
        'disable_after_down': 0,
        'type': 0, # icmp
 
         'retry': 3,
        'name': u'http_foo3',
        'consec_pass_reqd': 1,
        'interval': 5,
        'timeout': 5,
        'disable_after_down': 0,
        'type': 1, # tcp

        'retry': 3,
        'http': {
            'port': 80,
            'url': u'GET /foo',
            'expect_code': u'200'
        },
        'name': u'http_foo3',
        'consec_pass_reqd': 1,
        'interval': 5,
        'timeout': 5,
        'disable_after_down': 0,
        'type': 3, # http

        'retry': 3,
        'https': {
            'url': 'GET /foo',
            'port': 80,
            'expect_code': '200'
        },
        'name': 'http_foo3',
        'consec_pass_reqd': 1,
        'interval': 5,
        'timeout': 5,
        'disable_after_down': 0,
        'type': 4, # https

    },
    'slb.template.cookie_persistence': {
      "cookie_persistence_template": {
            "name": "",
            "expire_exist": 0,
            "expire": 3600,
            "cookie_name": "",
            "domain": "",
            "path": "",
            "match_type": 0,
            "match_all": 0,
            "insert_always": 0,
            "dont_honor_conn": 0
        }
  
    },
    'template.src_ip_persistence': {
    "src_ip_persistence_template": {
            "name": "src_ip",
            "match_type": 1,
            "match_all": 0,
            "timeout": 1800,
            "no_honor_conn": 0,
            "incl_sport": 0,
            "include_dstip": 0,
            "hash_persist": 0,
            "enforce_high_priority": 0,
            "netmask": "255.255.255.255",
            "netmask6": 96
        }
    
    },
    'partition': {
       'partition': {
            'max_aflex_file': 32,
            'network_partition': 0,
            'name': ""}

    }, 
    'slb.virtual_service': {
        "protocol": 11, # http
        "sync_cookie": {
            "sync_cookie": 0,
            "sack": 0
        },
        "snat_against_vip": 0,
        "received_hop": 0,
        "vport_template": "default",
        "send_reset": 0,
        "port": 80,
        "service_group": "",
        "vport_acl_id": 0,
        "auto_source_nat": 0,
        "extended_stats": 0,
        "server_ssl_template": "",
        "aflex_list": [],
        "status": 1,
        "default_selection": 1,
        "http_template": "",
        "source_nat": "",
        "cookie_persistence_template": "",
        "conn_reuse_template": "",
        "name": "",
        "tcp_proxy_template": "",
        "connection_limit": {
            "status": 0,
            "connection_limit_log": 0,
            "connection_limit": 8000000,
            "connection_limit_action": 0
        },
        "ram_cache_template": "",
        "pbslb_template": "",
        "stats_data": 1,
        "acl_natpool_binding_list": []


        "protocol": 12, # https
        "sync_cookie": {
            "sync_cookie": 0,
            "sack": 0
        },
        "snat_against_vip": 0,
        "received_hop": 0,
        "vport_template": "default",
        "send_reset": 0,
        "port": 443,
        "service_group": "",
        "auto_source_nat": 0,
        "vport_acl_id": 0,
        "extended_stats": 0,
        "server_ssl_template": "",
        "aflex_list": [],
        "status": 1,
        "client_ssl_template": "",
        "source_ip_persistence_template": "",
        "default_selection": 1,
        "http_template": "",
        "source_nat": "",
        "conn_reuse_template": "",
        "name": "",
        "tcp_proxy_template": "",
        "connection_limit": {
            "status": 0,
            "connection_limit_log": 0,
            "connection_limit": 8000000,
            "connection_limit_action": 0
        },
        "ram_cache_template": "",
        "pbslb_template": "",
        "stats_data": 1,
        "acl_natpool_binding_list": []


        "protocol": 2, # tcp
        "sync_cookie": {
            "sync_cookie": 0,
            "sack": 0
        },
        "snat_against_vip": 0,
        "received_hop": 0,
        "vport_template": "default",
        "tcp_template": "",
        "send_reset": 0,
        "port": '',
        "service_group": "",
        "vport_acl_id": 0,
        "extended_stats": 0,
        "aflex_list": [],
        "status": 1,
        "auto_source_nat": 0,
        "direct_server_return": 0,
        "source_ip_persistence_template": "",
        "default_selection": 1,
        "source_nat": "",
        "name": "",
        "ha_connection_mirror": 0,
        "connection_limit": {
            "status": 0,
            "connection_limit_log": 0,
            "connection_limit": 8000000,
            "connection_limit_action": 0
        },
        "pbslb_template": "",
        "stats_data": 1,
        "acl_natpool_binding_list": []

    },
}

def url(method, session_id):
    return ("/services/rest/v2.1/?format=json&method=%s&session_id=%s" %
            (method, session_id))

def arg_template(method):
    return copy.deepcopy(arg_templates[method])

