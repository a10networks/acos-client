
# ACOS Client

## Installation

### Install using pip

```
$ pip install acos_client
```

### Install the latest version

```
$ git clone blah
```

```
$ python setup.py
```

## Usage

```python
c = acos_client.Client('somehost.example.com', 'admin', '123')
```

#### Example setting up an SLB:

```python
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

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request

## Supported Versions

  * axapi 2.1.

## Future Features and Additions

Initial entry points for openstack driver. ACOS 4.0 support coming soon.

Please refer to [TODO.md](TODO.md).
