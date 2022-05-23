from ast import Lambda
from aws_cdk import (
    # Duration,
    Stack,
    # aws_sqs as sqs,
    aws_lambda,
    aws_iam,
    aws_apigateway,
    aws_guardduty
)
from constructs import Construct

class CdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        api_gateway = aws_apigateway.RestApi(self, 'API_Gateway_main', rest_api_name='pbAPI')
        api_root = api_gateway.root.add_resource('API')

        '''
        EC2 rememediation integration lambda function integrations
        '''
        ec2_remediation = api_root.add_resource('ec2')

        shutdown_ec2 = aws_lambda.Function(self, 'shutdown_ec2'
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler='lambda-handler.main',
            code=aws_lambda.Code.from_asset("Lambda_scripts/ec2/shutdown.py")
        )
        shutdown_ec2.role.add_managed_policy(aws_iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))
        shutdown_lambda_integration = aws_apigateway.LambdaIntegration(
            shutdown_ec2,
            proxy=False
        )
        ec2_shutdown = ec2_remediation.add_resource('shutdown')
        ec2_shutdown.add_method('POST', shutdown_lambda_integration)

        '''
        S3 rememediation integration lambda function integrations
        '''
        s3_remediation = api_root.add_resource('s3')

        # The code that defines your stack goes here

        # example resource
        # queue = sqs.Queue(
        #     self, "CdkQueue",
        #     visibility_timeout=Duration.seconds(300),
        # )
