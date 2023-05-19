import unittest

import boto3
from moto import mock_ec2

from altimeter.aws.resource.ec2.elastic_ip import ElasticIPResourceSpec
from altimeter.aws.scan.aws_accessor import AWSAccessor
from altimeter.core.graph.links import LinkCollection, ResourceLink, SimpleLink
from altimeter.core.resource.resource import Resource


class TestElasticIPSchema(unittest.TestCase):
    @mock_ec2
    def test_scan_vpc_domain(self):
        self.maxDiff = None
        account_id = "123456789012"
        region_name = "us-east-1"

        session = boto3.Session()

        ec2_client = session.client("ec2", region_name=region_name)
        allocation = ec2_client.allocate_address(Domain="vpc")
        allocation_id = allocation["AllocationId"]
        public_ip = allocation["PublicIp"]
        arn = "arn:aws:ec2:us-east-1:123456789012:elastic-ip/" + public_ip.replace(".", "-")

        scan_accessor = AWSAccessor(
            session=session,
            account_id=account_id,
            region_name=region_name
        )
        resources = ElasticIPResourceSpec.scan(scan_accessor)

        expected_resources = [
            Resource(
                resource_id=arn,
                type="aws:ec2:elastic-ip",
                link_collection=LinkCollection(
                    simple_links=(
                        SimpleLink(pred="public_ip", obj=public_ip),
                        SimpleLink(pred="allocation_id", obj=allocation_id),
                        SimpleLink(pred="domain", obj="vpc"),
                        SimpleLink(pred="instance_id", obj=""),
                        SimpleLink(pred="network_interface_id", obj=""),
                    ),
                    resource_links=(
                        ResourceLink(pred="account", obj="arn:aws::::account/123456789012"),
                        ResourceLink(pred="region", obj="arn:aws:::123456789012:region/us-east-1"),
                    ),
                ),
            )
        ]
        self.assertEqual(resources, expected_resources)

    @mock_ec2
    def test_scan_non_vpc_domain(self):
        self.maxDiff = None
        account_id = "123456789012"
        region_name = "us-east-1"

        session = boto3.Session()

        ec2_client = session.client("ec2", region_name=region_name)
        allocation = ec2_client.allocate_address()
        public_ip = allocation["PublicIp"]
        arn = "arn:aws:ec2:us-east-1:123456789012:elastic-ip/" + public_ip.replace(".", "-")

        scan_accessor = AWSAccessor(
            session=session,
            account_id=account_id,
            region_name=region_name
        )
        resources = ElasticIPResourceSpec.scan(scan_accessor)

        expected_resources = [
            Resource(
                resource_id=arn,
                type="aws:ec2:elastic-ip",
                link_collection=LinkCollection(
                    simple_links=(
                        SimpleLink(pred="public_ip", obj=public_ip),
                        SimpleLink(pred="domain", obj="standard"),
                        SimpleLink(pred="instance_id", obj=""),
                        SimpleLink(pred="network_interface_id", obj=""),
                    ),
                    resource_links=(
                        ResourceLink(pred="account", obj="arn:aws::::account/123456789012"),
                        ResourceLink(pred="region", obj="arn:aws:::123456789012:region/us-east-1"),
                    ),
                ),
            )
        ]
        self.assertEqual(resources, expected_resources)
