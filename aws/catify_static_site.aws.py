import aws_cdk as cdk
from constructs import Construct
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_s3_deployment as s3_deployment
from aws_cdk import aws_cloudfront as cloudfront
from aws_cdk import aws_cloudfront_origins as origins
from aws_cdk import aws_certificatemanager as acm
from aws_cdk import aws_route53 as route53
from aws_cdk import aws_route53_targets as targets


class CatifyAppStack(cdk.Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        """Creates a private S3 bucket for the static site construct"""
        bucket = s3.Bucket(
            self,
            "CatifyStaticBucket",
            bucket_name="catifystatic",
            website_index_document="catify.html",
            removal_policy=cdk.RemovalPolicy.DESTROY,  # Destroy bucket when stack is deleted
            public_read_access=True,               # Allow public read access
            block_public_access=s3.BlockPublicAccess.BLOCK_ACLS  # Block only ACL-based access, not bucket policies
        )

        # Deploy the contents of the ../site directory to the S3 bucket
        s3_deployment.BucketDeployment(self, "DeployCatifyBucket",
            sources=[s3_deployment.Source.asset("../site")],
            destination_bucket=bucket,
        )

        # Define the custom domain
        domain_name = "catify.makurspace.com"

        # Fetch the hosted zone for the domain
        hosted_zone = route53.HostedZone.from_lookup(self, "CatifyHostedZone", domain_name="makurspace.com")

        # Create an ACM certificate for the domain (in the us-east-1 region, required for CloudFront)
        certificate = acm.Certificate(self, "CatifyCertificate",
            domain_name=domain_name,
            validation=acm.CertificateValidation.from_dns(hosted_zone)
        )

        # Create the CloudFront distribution
        distribution = cloudfront.Distribution(self, "CatifyCloudfront",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS  # Force HTTPS
            ),
            domain_names=[domain_name],
            certificate=certificate
        )

        # Create an A record in Route53 pointing the domain to CloudFront
        route53.ARecord(self, "CatifyAliasRecord",
            zone=hosted_zone,
            target=route53.RecordTarget.from_alias(targets.CloudFrontTarget(distribution)),
            record_name="catify"  # This creates the subdomain Catify.makurspace.com
        )

import os
app = cdk.App()
env = cdk.Environment(account=os.environ["AWS_ACCOUNT_ID"], region="us-east-1")
CatifyAppStack(app, "CatifyAppStack", env=env)

app.synth()
