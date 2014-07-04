
Title and intro boilerplate

Install steps:

pip install acos_client

or

git clone blah
python setup.py

Current support:

axapi 2.1.  ACOS 4.0 support coming soon.

Usage:

```
c = acos_client.Client('somehost.example.com', 'admin', '123')
```

... example setting up slb:

```
c = acos_client.Client('1.2.3.4', 'admin', '123')
c.slb.server.create('s1', '1.1.1.1')
c.slb.server.create('s2', '1.1.1.2')
c.slb.service_group.create('pool1', c.slb.service_group.TCP,
                       c.slb.service_group.ROUND_ROBIN)
c.slb.virtual_server.create("vip1", '1.1.1.3',
                            c.slb.virtual_service.HTTP,
                            '80', 'pool1')
c.slb.hm.create(c.slb.hm.HTTP, "hm1", 5, 5, 5, 'GET', '/', '200', 80)
c.slb.service_group.update('pool1', health_monitor='hm1')
c.slb.service_group.member.create("pool1", "s1", 80)
c.slb.service_group.member.create("pool1", "s2", 80)
```

Not yet complete, initial entry points for openstack driver.  Refer to TODO.md.

Blurb about contributing

Anything else useful.


