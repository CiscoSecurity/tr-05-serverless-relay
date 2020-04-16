# AWS HOWTO

## Using Custom AWS IAM Users, Roles, Policies

### Custom AWS IAM Users and Policies for Deployment

You can specify which *local* profile to use for deploying your Zappa application
by defining the `profile_name` setting, which will correspond to a profile in
your AWS credentials file (check the
[official documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html)
for more details on how to configure multiple AWS profiles).

Thus in order to get started, you have to create an IAM User with the name
`serverless` (see the Zappa
[configuration file](../zappa_settings.json)).

By default, Zappa just assumes that the user already has all the necessary
permissions before deploying or running any other command. On the other hand,
it is not always possible (and is not a good idea either according to the
[PoLP](https://en.wikipedia.org/wiki/Principle_of_least_privilege))
to simply work on behalf of a user with administrator access to any resource.

So a better solution is to grant your user a more granular (ideally minimum)
set of permissions. We have already compiled the
[policy file](ZappaLambdaDeploymentPolicy.json) to simplify things. You just
have to attach this policy to your user by going through the following steps:

1. Go to the `Identity and Access Management (IAM)` console.
2. Select the `Policies` tab under the `Access management` drop-down list.
3. Click the `Create policy` button.
4. Select the `JSON` tab. Copy and paste the JSON contents of the policy file.
Make sure to replace `<ACCOUNT_ID>` by the actual ID of your AWS account.
5. Click the `Review policy` button.
6. Give your policy the name `ZappaLambdaDeploymentPolicy` and click
the `Create policy` button.
7. Select the `Users` tab under the `Access management` drop-down list.
8. Find the `serverless` user and go to the corresponding configuration page.
9. Click the `Add permissions` button.
10. Select the `Attach existing policies directly` tab.
11. Search for the `ZappaLambdaDeploymentPolicy` policy and enable it via the
corresponding check-box.
12. Click the `Next: Review` button and then the `Add permissions` button.

Though the described setup has to be done manually, the good thing is that it
has to be done only once per each particular `serverless` user (the steps 1-6
can be skipped if the `ZappaLambdaDeploymentPolicy` policy already exist).

### Custom AWS IAM Roles and Policies for Execution

The default IAM policy created by Zappa for executing the Lambda is very
permissive. It grants access to all actions for all resources for types
CloudWatch, S3, Kinesis, SNS, SQS, DynamoDB, and Route53; lambda:InvokeFunction
for all Lambda resources; Put to all X-Ray resources; and all Network Interface
operations to all EC2 resources. While this allows most Lambdas to work
correctly with no extra permissions, it is generally not an acceptable set of
permissions for most continuous integration pipelines or production
deployments. Instead, you will probably want to manually manage your IAM
policies.

That is why the `manage_roles` setting is set to `false` in the Zappa
[configuration file](../zappa_settings.json). Also, notice the `role_name`
setting, it makes Zappa look for an IAM role with the following name:
`tr-serverless-relay-ZappaLambdaExecutionRole`.
The role will be automatically attached to your Lambda by Zappa.

**Note.** After having properly configured your `serverless` user, Zappa must
be able to attach such roles to any of your Lambdas on behalf of `serverless`.

We have already compiled the
[policy file](ZappaLambdaExecutionPolicy.json) with a much smaller set of
permissions intended exactly for our particular use case (i.e. implementation
of Threat Response Serverless Relay APIs). You just have to create an AIM role
and attach this policy to the role by going through the following steps:

1. Go to the `Identity and Access Management (IAM)` console.
2. Select the `Policies` tab under the `Access management` drop-down list.
3. Click the `Create policy` button.
4. Select the `JSON` tab. Copy and paste the JSON contents of the policy file.
5. Click the `Review policy` button.
6. Give your policy the name `ZappaLambdaExecutionPolicy` and click
the `Create policy` button.
7. Select the `Roles` tab under the `Access management` drop-down list.
8. Click the `Create role` button.
9. Select the `AWS service` tab and choose the `Lambda` service.
10. Click the `Next: Permissions` button.
11. Search for the `ZappaLambdaExecutionPolicy` policy and enable it via the
corresponding check-box.
12. Click the `Next: Tags` button and then the `Next: Review` button.
13. Give your role the name `tr-serverless-relay-ZappaLambdaExecutionRole`
and click the `Create role` button.
14. Find the newly created role and go to the corresponding configuration page.
15. Select the `Trust relationships` tab.
16. Click the `Edit trust relationship` button.
17. The `Service` field must be equal to `lambda.amazonaws.com` for now.
Convert the value to a list and add `apigateway.amazonaws.com` to it.

Before:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

After:
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "apigateway.amazonaws.com",
          "lambda.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Though the described setup has to be done manually, the good thing is that it
has to be done only once (all the steps can be skipped if both the
`ZappaLambdaExecutionPolicy` policy and the
`tr-serverless-relay-ZappaLambdaExecutionRole` role already exist).

## Setting Environment Variables

Unfortunately, Zappa does not have a good way to pass environment variables to
your Lambdas. Of course, the `aws_environment_variables` setting allows us to
use native AWS Lambda environment variables. These are useful as you can easily
change them via the AWS Lambda console at run-time. They are also useful for
storing sensitive credentials and to take advantage of KMS encryption of
environment variables.

The main problem with `aws_environment_variables` is that environment variables
have to be hard-coded into the configuration file, and this is not acceptable.

Example:
```json
{
    "dev": {
        "aws_environment_variables": {
            "key": "value"
        }
    }
}
```

So a better solution is to set environment variables via the AWS Lambda console
directly. The process itself is quite easy and can be done by going through the
following steps:

1. Go to the `AWS Lambda` console.
2. Select the `Functions` tab.
3. Find your Lambda and go to the corresponding configuration page.
4. Set your key-value pairs in the `Environment variables` section.
5. Click the `Save` button.

Though the described setup has to be done manually, the good thing is that it
has to be done only once per each particular deployment, and the values can be
dynamically changed at run-time without having to re-deploy anything.
