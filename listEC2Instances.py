#!/usr/bin/env python
# python 2!

######################################################################
#  Copyright (c)2017, David L. Armstrong.
#
#  See LICENSE file included for usage and distribution rights.
#
######################################################################

#NAME / DESCRIPTION
'''
listEC2Instances.py

Tool which uses AWS API access to list all EC2 instances in any
single region, sorted by the value of a tag each instance has
called 'Owner'.  The script displays the results in an easy
to read format which includes the instance id, owner, instance
type and launch time.  The script works for any number of
instances, and displays any instances without an Owner tag
as owner 'unknown' with the instance id, type and launch time.
'''


def retrieveEc2InstanceData(accessKeyID=None, secretAccessKey=None, regionID=None):

# TODO Client is interesting since we can flatten it for our own design, but
# seems like a better iden to stick with higher level resource objects
# Client also returns 'ResponseMetadata', very handy for debugging
#
#    ec2client = boto3.client(
#        'ec2',
#        aws_access_key_id=accessKeyID,
#        aws_secret_access_key=secretAccessKey,
#        region_name=regionID,
#    )
#    print(ec2client.describe_instances())

    ec2resource = boto3.resource(
        'ec2',
        aws_access_key_id=accessKeyID,
        aws_secret_access_key=secretAccessKey,
        region_name=regionID,
    )

    instanceMetaData = []
    for instance in ec2resource.instances.all():
        # tags are stored as key/value pairs, we'll flatten that a bit into a standard dict
        instanceMetaData.append({'obj': instance,
                                 'tags': dict([[tag['Key'], tag['Value']] for tag in instance.tags]),
                                })

    return instanceMetaData


def printEc2InstanceData(instanceMetaData, attrList=None, tagList=None, sortBy=None):

    # Set up default output
    if attrList is None:
        attrList = ['id', 'instance_type', 'launch_time']
    elif 'all' in attrList:
        attrList = ['ami_launch_index', 'architecture', 'block_device_mappings', 'client_token', 'ebs_optimized', 'ena_support', 'hypervisor', 'iam_instance_profile', 'image_id', 'id', 'instance_lifecycle', 'instance_type', 'kernel_id', 'key_name', 'launch_time', 'monitoring', 'network_interfaces_attribute', 'placement', 'platform', 'private_dns_name', 'private_ip_address', 'product_codes', 'public_dns_name', 'public_ip_address', 'ramdisk_id', 'root_device_name', 'root_device_type', 'security_groups', 'source_dest_check', 'spot_instance_request_id', 'sriov_net_support', 'state', 'state_reason', 'state_transition_reason', 'subnet_id', 'virtualization_type', 'vpc_id',]

    if tagList is None:
        tagList = ['Owner']

    if sortBy is None:
        sortBy = ['tag:Owner',]

    instanceList = []
    for instance in instanceMetaData:

        # Copy over interesting attributes
        instanceDict = dict([[attr, getattr(instance['obj'], attr)] for attr in attrList])

        # Copy over interesting tags
        for tagName in tagList:
            if tagName == "all":
                for tagName in instance['tags']:
                    instanceDict["tag:%s" % (tagName,)] = instance['tags'].get(tagName)
            else:
                instanceDict["tag:%s" % (tagName,)] = instance['tags'].get(tagName, "unknown")

        # Make sure any/all tags and attrs specified in sort are defined in every instance object
        for field in sortBy:
            matchObj = re.search("^tag:(?P<tagName>.*)$", field)
            if matchObj:
                tagName = matchObj.group('tagName')
                instanceDict["tag:%s" % (tagName,)] = instance['tags'].get(tagName, "unknown")
            else:
                instanceDict[field] = getattr(instance['obj'], field)

        instanceList.append(instanceDict)

    # Feed sort the dict values for the sortBy keys
    instanceList.sort(key=lambda item: [item[key] for key in sortBy])

    # YAML gives us a handy format that is reliably parseable
    import yaml
    print(yaml.dump(instanceList, default_flow_style=False))
#    for instance in instanceList:
#        for attr in attrList:
#            print("%s: %s" % (attr, instance[attr],))
#        for tag in tagList:
#            print("%s: %s" % (tag, instance["tag:%s" % (tag,)],))
#
#        print


if __name__ == "__main__":
    # Interactive mode
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--accessKeyID', help='AWS Access key ID', required=True)
    parser.add_argument('--secretAccessKey', help='AWS Secret access key', required=True)
    parser.add_argument('--regionID', help='AWS Region ID', required=True)
    parser.add_argument('--sortBy', nargs='*', help='List of fields to sort by', required=False)
    parser.add_argument('--attrs', nargs='*', help='List of instance attributes to display', required=False)
    parser.add_argument('--tags', nargs='*', help='List of instance tags to display', required=False)

    args = parser.parse_args()

    # Global imports, only after successful syntax check
    import boto3, re

    ec2InstanceData = retrieveEc2InstanceData(accessKeyID=args.accessKeyID, secretAccessKey=args.secretAccessKey, regionID=args.regionID)
    printEc2InstanceData(ec2InstanceData, sortBy=args.sortBy, attrList=args.attrs, tagList=args.tags)

