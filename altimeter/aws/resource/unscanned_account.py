"""Resource representing an unscanned AWS Account"""
from typing import List, Type, TypeVar

from botocore.client import BaseClient

from altimeter.core.graph.link.links import SimpleLink
from altimeter.core.graph.link.base import Link
from altimeter.core.graph.schema import Schema
from altimeter.aws.resource.resource_spec import ScanGranularity, ListFromAWSResult, AWSResourceSpec
from altimeter.core.resource.resource import Resource
from altimeter.core.resource.resource_spec import ResourceScanResult
from altimeter.aws.scan.aws_accessor import AWSAccessor

T = TypeVar("T", bound="UnscannedAccountResourceSpec")


class UnscannedAccountResourceSpec(AWSResourceSpec):
    """Resource representing an unscanned AWS Account"""

    type_name = "unscanned-account"
    service_name = "null"
    scan_granularity = ScanGranularity.ACCOUNT
    schema = Schema()

    @classmethod
    def create_resource(cls: Type[T], account_id: str, errors: List[str]) -> Resource:
        links: List[Link] = []
        links.append(SimpleLink(pred="account_id", obj=account_id))
        for error in errors:
            link = SimpleLink(pred="error", obj=error)
            links.append(link)
        return Resource(
            resource_id=cls.generate_arn("", "", account_id),
            type_name=cls.get_full_type_name(),
            links=links,
        )

    @classmethod
    def get_full_type_name(cls: Type[T]) -> str:
        return f"{cls.provider_name}:{cls.type_name}"

    @classmethod
    def list_from_aws(
        cls: Type[T], client: BaseClient, account_id: str, region: str
    ) -> ListFromAWSResult:
        """List resources from AWS using client."""

    @classmethod
    def generate_arn(cls: Type[T], account_id: str, region: str, resource_id: str) -> str:
        """Generate an ARN for this resource"""
        return f"arn:aws::::account/{resource_id}"

    @classmethod
    def scan(cls: Type[T], scan_accessor: AWSAccessor) -> ResourceScanResult:
        raise NotImplementedError(f"{cls.__name__} is not a scannable ResourceSpec class.")
