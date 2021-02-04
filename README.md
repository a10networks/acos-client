# ACOS Client

## Table of Contents
1. [Supported Versions](#Supported-Versions)

2. [Installation for ACOSv4.1.4](#Installation-ACOSv4.1.4)

3. [Installation for ACOSv4.1.1](#Installation-ACOSv4.1.1)

4. [Example usage information](#Usage)

5. [Contributing & Testing](#Contributing)

6. [Issues and Inquiries](#Issues-and-Inquiries)

7. [Helpful Links](#Helpful-links)


## Supported Versions

```
| ACOS Version   | AXAPI Version | ACOS Client Version | Status      |
| 2.7.1†         | 2             | >=0.1.0,<0.3.0      | end-of-life |
| 2.7.2          | 2             | >=0.1.0,<0.3.0      | end-of-life |
| 4.0.0          | 3             | >=1.4.6,<1.5.0      | Maintenance |
| 4.1.1          | 3             | >=1.5.0,<2.0.0      | Maintenance |
| 4.1.4 GR1-P2   | 3             | >=2.0.0,<2.4.0      | Maintenance |
| 4.1.4          | 3             | >=2.4.0             | Maintenance |
| 4.1.4 GR1-P5   | 3             | >=2.6.0             | Maintenance |
| 5.2.1          | 3             | >=2.6.0             | Maintenance |
```

†Works only when not using partitioning

## Installation

### Install using pip

```sh
$ pip install acos-client>=2.6.0
```

### Install from source

```sh
$ git clone https://github.com/a10networks/acos-client.git
$ cd acos-client
$ git checkout stable/stein
$ pip install -e . 
```

## Usage

```python
c = acos_client.Client('somehost.example.com', acos_client.AXAPI_30, 'admin', 'password')
```

#### Example setting up an SLB:

```python
import acos_client as acos

c = acos.Client('1.2.3.4', acos.AXAPI_30, 'admin', 'password')
c.slb.server.create('s1', '1.1.1.1')
c.slb.server.create('s2', '1.1.1.2')
c.slb.service_group.create('pool1', c.slb.service_group.TCP, c.slb.service_group.ROUND_ROBIN)
c.slb.virtual_server.create('vip1', '1.1.1.3')
c.slb.hm.create('hm1', c.slb.hm.HTTP, 5, 5, 5, 'GET', '/', '200', 80)
c.slb.service_group.update('pool1', health_monitor='hm1')
c.slb.service_group.member.create('pool1', 's1', 80)
c.slb.service_group.member.create('pool1', 's2', 80)
```

## Contributing

1. Fork it
2. Create your feature branch (`git checkout -b my-new-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin my-new-feature`)
5. Create new Pull Request

### Testing

This project uses [tox](https://pypi.python.org/pypi/tox) for testing. To run
the test suite simply:

```sh
$ sudo pip install tox  # use pip2 if using Arch Linux
$ cd /path/to/acos_client
$ tox
```

## Issues and Inquiries
For all issues, please send an email to support@a10networks.com 

For general inquiries, please send an email to opensource@a10networks.com


## Helpful links

### Improved speed
pypy: [http://pypy.org/index.html](http://pypy.org/index.html)

### Old python versions
Deadsnakes github: [https://github.com/deadsnakes](https://github.com/deadsnakes)  
Deadsnakes ppa: [https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa](https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa)
