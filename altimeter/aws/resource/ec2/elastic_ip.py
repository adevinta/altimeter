"""Resource for ElasticIPs"""
from typing import Type

from botocore.client import BaseClient

from altimeter.aws.resource.resource_spec import ListFromAWSResult
from altimeter.aws.resource.ec2 import EC2ResourceSpec
from altimeter.core.graph.field.scalar_field import ScalarField
from altimeter.core.graph.field.tags_field import TagsField
from altimeter.core.graph.schema import Schema


class ElasticIPResourceSpec(EC2ResourceSpec):
    """Resource for ElasticIPs"""

    type_name = "elastic-ip"
    schema = Schema(
        ScalarField("PublicIp"),
        ScalarField("AllocationId", optional=True),
        ScalarField("AssociationId", optional=True),
        ScalarField("Domain"),
        ScalarField("InstanceId", optional=True),
        ScalarField("NetworkInterfaceId", optional=True),
        ScalarField("NetworkInterfaceOwnerId", optional=True),
        ScalarField("PrivateIpAddress", optional=True),
        ScalarField("PublicIpv4Pool", optional=True),
        ScalarField("NetworkBorderGroup", optional=True),
        ScalarField("CustomerOwnedIp", optional=True),
        ScalarField("CustomerOwnedIpv4Pool", optional=True),
        ScalarField("CarrierIp", optional=True),
        TagsField(),
    )

    @classmethod
    def list_from_aws(
        cls: Type["ElasticIPResourceSpec"],
        client: BaseClient, account_id: str,
        region: str
    ) -> ListFromAWSResult:
        """Return a dict with the following format:

            {'elastic_ip_arn_1': {elastic_ip_1},
             'elastic_ip_arn2': {elastic_ip_2},
             ...}
        """
        elastic_ips = {}
        resp = client.describe_addresses()
        for elastic_ip in resp.get("Addresses", []):
            resource_id = elastic_ip["PublicIp"].replace(".", "-")
            resource_arn = cls.generate_arn(
                account_id=account_id, region=region, resource_id=resource_id
            )
            elastic_ips[resource_arn] = elastic_ip
        return ListFromAWSResult(resources=elastic_ips)
