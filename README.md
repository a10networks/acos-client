# ACOS Client

A10 github repos:

- [a10-openstack-lbaas](https://github.com/a10networks/a10-openstack-lbaas) - OpenStack LBaaS driver, 
identical to the files that are currently merged into Juno.  Also supports Icehouse.  Pypi package 
'a10-openstack-lbaas'.
- [a10-openstack-lbaas, havana branch](https://github.com/a10networks/a10-openstack-lbaas/tree/havana) - OpenStack 
LBaaS driver, for the Havana release.  Pypi package 'a10-openstack-lbaas-havana'.
- [a10-neutron-lbaas](https://github.com/a10networks/a10-neutron-lbaas) - Middleware sitting between the 
openstack driver and our API client, mapping openstack constructs to A10's AxAPI.
- [acos-client](https://github.com/a10networks/acos-client) - AxAPI client used by A10's OpenStack driver.
- [neutron-thirdparty-ci](https://github.com/a10networks/neutron-thirdparty-ci) - Scripts used by 
our Jenkins/Zuul/Devstack-Gate setup, used to test every openstack code review submission against 
A10 appliances and our drivers.
- [a10_lbaas_driver](https://github.com/a10networks/a10_lbaas_driver) - An older revision of A10's 
LBaaS driver; no longer supported.

## Installation

### Install using pip

```sh
$ pip install acos-client
```

### Install from source

```sh
$ git clone https://github.com/a10networks/acos-client.git
$ cd acos-client
$ python setup.py install
```

## Usage

```python
c = acos_client.Client('somehost.example.com', acos_client.AXAPI_21,
                       'admin', '123')
```

#### Example setting up an SLB:

```python
import acos_client as acos

c = acos.Client('1.2.3.4', acos.AXAPI_21, 'admin', '123')
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

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request

## Supported Versions

  * axapi 2.1, ACOS 2.7.2+ (2.7.1 works if you avoid partitions)

