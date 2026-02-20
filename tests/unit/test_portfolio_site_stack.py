import aws_cdk as core
import aws_cdk.assertions as assertions

from portfolio_site.portfolio_site_stack import PortfolioSiteStack

# example tests. To run these tests, uncomment this file along with the example
# resource in portfolio_site/portfolio_site_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = PortfolioSiteStack(app, "portfolio-site")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
