#!/usr/bin/env python3
import os

import aws_cdk as cdk

from portfolio_site.portfolio_site_stack import PortfolioSiteStack

# ---------------------------------------------------------------------------
# Environment configuration
# Account IDs are intentionally placeholder values — replace them with yours.
# ---------------------------------------------------------------------------
ENV_CONFIG = {
    "nonprod": {
        "account": os.getenv("NONPROD_ACCOUNT_ID"),
        "region":  os.getenv("NONPROD_REGION"),
    },
    "prod": {
        "account": os.getenv("PROD_ACCOUNT_ID"),
        "region":  os.getenv("PROD_REGION"),
    },
}

app = cdk.App()

# Select environment with: cdk deploy -c env=prod   (default: nonprod)
env_name = app.node.try_get_context("env") or "nonprod"
if env_name not in ENV_CONFIG:
    raise ValueError(f"Unknown environment '{env_name}'. Valid values: {list(ENV_CONFIG)}")

config = ENV_CONFIG[env_name]

# Optional: pass alarm email via context to subscribe automatically.
# Usage: cdk deploy -c env=prod -c alarm_email=you@example.com
alarm_email = app.node.try_get_context("alarm_email")

stack = PortfolioSiteStack(
    app,
    f"PortfolioSiteStack-{env_name}",
    env_name=env_name,
    alarm_email=alarm_email,
    env=cdk.Environment(
        account=config["account"],
        region=config["region"],
    ),
)

# Default tags applied to every resource in the stack
cdk.Tags.of(stack).add("project",     "portfoliosite")
cdk.Tags.of(stack).add("managed-by",  "cdk")
cdk.Tags.of(stack).add("environment", env_name)

app.synth()
