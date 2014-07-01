
COOKIE_PER_TEMP_OBJ = wrapper(copy.deepcopy({
    "call": {"create": {"POST": "/services/rest/v2.1/?format=json&method=slb."
                                "template.cookie_persistence."
                                "create&session_id=%s"},
             "update": {"POST": "/services/rest/v2.1/?format=json&"
                                "method=slb.template.cookie_persistence."
                                "update&session_id=%s"},
             "delete": {"POST": "/services/rest/v2.1/?format=json&"
                                "method=slb.template.cookie_persistence."
                                "delete&session_id=%s"},
             "search": {"POST": "/services/rest/v2.1/?format=json&"
                                "method=slb.template.cookie_persistence."
                                "search&session_id=%s"}
             },
    "ds": {
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
    }
}))


