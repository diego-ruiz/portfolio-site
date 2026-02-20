from aws_cdk import (
    Stack,
    RemovalPolicy,
    CfnOutput,
    Duration,
    aws_s3 as s3,
    aws_s3_deployment as s3deploy,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_cloudwatch as cloudwatch,
    aws_cloudwatch_actions as cw_actions,
    aws_sns as sns,
    aws_sns_subscriptions as subscriptions,
)
from constructs import Construct


class PortfolioSiteStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, env_name: str, alarm_email: str = None, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # S3 bucket — private, accessed only by CloudFront
        bucket = s3.Bucket(
            self, "PortfolioBucket",
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
        )

        # CloudFront distribution with Origin Access Control (OAC)
        distribution = cloudfront.Distribution(
            self, "PortfolioDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3BucketOrigin.with_origin_access_control(bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                cache_policy=cloudfront.CachePolicy.CACHING_OPTIMIZED,
            ),
            default_root_object="index.html",
            # Return index.html for 403/404 so SPAs handle routing client-side
            error_responses=[
                cloudfront.ErrorResponse(
                    http_status=403,
                    response_http_status=200,
                    response_page_path="/index.html",
                ),
                cloudfront.ErrorResponse(
                    http_status=404,
                    response_http_status=200,
                    response_page_path="/index.html",
                ),
            ],
        )

        # Deploy the Vite production build output to S3.
        # Run `npm run build` inside website/ before deploying.
        s3deploy.BucketDeployment(
            self, "DeployPortfolio",
            sources=[s3deploy.Source.asset("./website/dist")],
            destination_bucket=bucket,
            distribution=distribution,
            distribution_paths=["/*"],
        )

        # Output the site URL
        CfnOutput(
            self, "PortfolioURL",
            value=f"https://{distribution.distribution_domain_name}",
            description="Portfolio site CloudFront URL",
        )

        # ── Billing alarm ────────────────────────────────────────────────────
        # NOTE: AWS billing metrics are only emitted in us-east-1.
        # Prerequisite: enable "Receive Billing Alerts" in the AWS Billing
        # console (Billing Preferences) — this is a one-time manual step.
        alarm_topic = sns.Topic(
            self, "BillingAlarmTopic",
            display_name="Portfolio Site Billing Alarm",
        )

        if alarm_email:
            alarm_topic.add_subscription(
                subscriptions.EmailSubscription(alarm_email)
            )

        billing_metric = cloudwatch.Metric(
            namespace="AWS/Billing",
            metric_name="EstimatedCharges",
            dimensions_map={"Currency": "USD"},
            # Billing metrics are published once per day
            period=Duration.hours(24),
            statistic="Maximum",
        )

        billing_alarm = cloudwatch.Alarm(
            self, "MonthlyBillingAlarm",
            alarm_name=f"portfolio-monthly-cost-{env_name}",
            alarm_description="Alert when estimated AWS charges exceed $20",
            metric=billing_metric,
            threshold=20,
            comparison_operator=cloudwatch.ComparisonOperator.GREATER_THAN_OR_EQUAL_TO_THRESHOLD,
            evaluation_periods=1,
            treat_missing_data=cloudwatch.TreatMissingData.NOT_BREACHING,
        )
        billing_alarm.add_alarm_action(cw_actions.SnsAction(alarm_topic))

        CfnOutput(
            self, "BillingAlarmTopicArn",
            value=alarm_topic.topic_arn,
            description="SNS topic for billing alerts — subscribe your email if not set via alarm_email context",
        )
