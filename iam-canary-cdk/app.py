from aws_cdk import aws_cloudwatch as cloudwatch
from aws_cdk import aws_cloudwatch_actions as actions
from aws_cdk import aws_events as events
from aws_cdk import aws_events_targets as targets
from aws_cdk import aws_iam as iam
from aws_cdk import aws_lambda as lambda_
from aws_cdk import aws_sns as sns
from aws_cdk import aws_sns_subscriptions as subscriptions
from aws_cdk import core as cdk

class IAMCanary(cdk.Stack):
    def __init__(self, app: cdk.App, id: str) -> None:
        super().__init__(app, id)

        with open("lambda-handler.py", encoding="utf8") as fp:
            handler_code = fp.read()

        principals_actions_json = cdk.CfnParameter(
            self, "PrincipalsActionsJSON",
            type = "String",
            default = "{}",
        )

        alert_notification_email = cdk.CfnParameter(
            self, "AlertNotificationEmail",
            type = "String",
            default = "name@domain.com",
        )

        role = iam.Role(
            self, "CheckPrincipalsActionsLambdaRole", 
            assumed_by = iam.ServicePrincipal("lambda.amazonaws.com"),
            managed_policies = [
                iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole")
            ]
        )
        role.add_to_policy(iam.PolicyStatement(
            effect = iam.Effect.ALLOW,
            actions = ["iam:SimulatePrincipalPolicy"],
            resources=["*"]
        )) 

        lambdaFn = lambda_.Function(
            self, "CheckPrincipalsActions",
            code = lambda_.InlineCode(handler_code),
            handler = "index.lambda_handler",
            memory_size = 128,
            timeout = cdk.Duration.seconds(10),
            runtime = lambda_.Runtime.PYTHON_3_8,
            environment = { "principals_actions_json": principals_actions_json.value_as_string },
            description = "Check actions assigned to an IAM users, roles, or groups",
            role = role,
        )

        rule = events.Rule(
            self, "CheckPrincipalsActionsEventScheduler",
            schedule = events.Schedule.rate(cdk.Duration.minutes(1)),
        )
        rule.add_target(targets.LambdaFunction(lambdaFn))

        topic = sns.Topic(self, "CheckPrincipalsActionsLambdaErrorTopic")
        topic.add_subscription(subscriptions.EmailSubscription(alert_notification_email.value_as_string))

        metric = lambdaFn.metric("Errors").with_(
            period = cdk.Duration.seconds(60),
            statistic = "Sum"
        )

        alarm = metric.create_alarm(
            self, "CheckPrincipalsActionsAlarm",
            threshold = 1,
            evaluation_periods = 1,
            datapoints_to_alarm = 1,
        )
        alarm.add_alarm_action(actions.SnsAction(topic))

app = cdk.App()
IAMCanary(app, "IAMCanary")
app.synth()
