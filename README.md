[![license](https://img.shields.io/badge/license-apache_2.0-red.svg?style=flat)](https://raw.githubusercontent.com/square/metrics/master/LICENSE)

# listEC2Instances.py

List EC2 instances in a region given specified credentials

Tool which uses AWS API access to list all EC2 instances in any
single region.  The script works for any number of instances.

# Requirements

listEC2Instances.py uses Python2.7+ and requires boto3 http://boto3.readthedocs.io/ and PyYAML http://pyyaml.org/

# Commandline Syntax
```
usage: listEC2Instances.py [-h] --accessKeyID ACCESSKEYID --secretAccessKey
                           SECRETACCESSKEY --regionID REGIONID
                           [--attrs [ATTRS [ATTRS ...]]]
                           [--tags [TAGS [TAGS ...]]]

optional arguments:
  -h, --help            show this help message and exit
  --accessKeyID ACCESSKEYID
                        AWS Access key ID
  --secretAccessKey SECRETACCESSKEY
                        AWS Secret access key
  --regionID REGIONID   AWS Region ID
  --attrs [ATTRS [ATTRS ...]]
                        List of instance attributes to display
  --tags [TAGS [TAGS ...]]
                        List of instance tags to display
```

## Examples

# Standard output.  Displays instance id, owner, instance type and launch time.  Sorted by 'Owner' tag ("unknown" if not defined).
```
$ ./listEC2Instances.py --accessKeyID "ACCESSKEYID" --secretAccessKey "SECRETACCESSKEY" --regionID="us-west-2"
- id: i-00000000000000003
  instance_type: t2.nano
  launch_time: 2016-06-22 01:02:28+00:00
  tag:Owner: Jdog
- id: i-00000000000000001
  instance_type: t2.nano
  launch_time: 2016-06-22 01:02:28+00:00
  tag:Owner: Ohai
- id: i-00000000000000004
  instance_type: t2.nano
  launch_time: 2016-06-22 01:02:28+00:00
  tag:Owner: unknown
- id: i-00000000000000002
  instance_type: t2.nano
  launch_time: 2016-06-22 01:02:28+00:00
  tag:Owner: unknown
```

# Specify one or more fields to sort by (use "tag:<tagName>" to specify a tag for sorting).
```
$ ./listEC2Instances.py --accessKeyID "ACCESSKEYID" --secretAccessKey "SECRETACCESSKEY" --regionID="us-west-2" --sortBy "tag:Owner" id
- id: i-00000000000000003
  instance_type: t2.nano
  launch_time: 2016-06-22 01:02:28+00:00
  tag:Owner: Jdog
- id: i-00000000000000001
  instance_type: t2.nano
  launch_time: 2016-06-22 01:02:28+00:00
  tag:Owner: Ohai
- id: i-00000000000000002
  instance_type: t2.nano
  launch_time: 2016-06-22 01:02:28+00:00
  tag:Owner: unknown
- id: i-00000000000000004
  instance_type: t2.nano
  launch_time: 2016-06-22 01:02:28+00:00
  tag:Owner: unknown

$ ./listEC2Instances.py --accessKeyID "ACCESSKEYID" --secretAccessKey "SECRETACCESSKEY" --regionID="us-west-2" --sortBy id
- id: i-00000000000000001
  instance_type: t2.nano
  launch_time: 2016-06-22 01:02:28+00:00
  tag:Owner: Ohai
- id: i-00000000000000002
  instance_type: t2.nano
  launch_time: 2016-06-22 01:02:28+00:00
  tag:Owner: unknown
- id: i-00000000000000003
  instance_type: t2.nano
  launch_time: 2016-06-22 01:02:28+00:00
  tag:Owner: Jdog
- id: i-00000000000000004
  instance_type: t2.nano
  launch_time: 2016-06-22 01:02:28+00:00
  tag:Owner: unknown
```

# Displaying a specific list of tags or attributes.
Empty list of attrs and tags (NOTE: fields specified for sorting will be displayed even if not specified)  Not sure why, but you can lol.
```
$ ./listEC2Instances.py --accessKeyID "ACCESSKEYID" --secretAccessKey "SECRETACCESSKEY" --regionID="us-west-2" --attrs --tags --sortBy
- {}
- {}
- {}
- {}

$ ./listEC2Instances.py --accessKeyID "ACCESSKEYID" --secretAccessKey "SECRETACCESSKEY" --regionID="us-west-2" --attrs --tags --sortBy id tag:Owner
- id: i-00000000000000001
  tag:Owner: Ohai
- id: i-00000000000000002
  tag:Owner: unknown
- id: i-00000000000000003
  tag:Owner: Jdog
- id: i-00000000000000004
  tag:Owner: unknown

```

# Displaying all tags and attribtutes with "all" keyword
```
$ ./listEC2Instances.py --accessKeyID "ACCESSKEYID" --secretAccessKey "SECRETACCESSKEY" --regionID="us-west-2" --attrs all --tags all --sortBy id
- ami_launch_index: 0
  architecture: x86_64
  block_device_mappings:
  - !!python/unicode 'DeviceName': /dev/sda1
    !!python/unicode 'Ebs':
      !!python/unicode 'AttachTime': 2016-06-10 22:14:52+00:00
      !!python/unicode 'DeleteOnTermination': true
      !!python/unicode 'Status': attached
  id: i-00000000000000001
  instance_type: t2.nano
  tag:Owner: Ohai
  [... you get the idea]

```

