# AWS HOWTO

## Using Custom AWS IAM Users, Roles, Policies

### Custom AWS IAM Users and Policies for Deployment

You can specify which *local* profile to use for deploying your Zappa application
by defining the `profile_name` setting, which will correspond to a profile in
your AWS credentials file (check the
[official documentation](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html)
for more details on how to configure multiple AWS profiles).

Thus you have to create an IAM User with the name `serverless` first (see the
[configuration file](../zappa_settings.json) for Zappa).

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
8. Find the `serverless` user.
9. Click the `Add permissions` button.
10. Select the `Attach existing policies directly` tab.
11. Search for the `ZappaLambdaDeploymentPolicy` policy.
12. Click the `Next: Review` button and then the `Add permissions` button.

Though the described setup has to be done manually, the good thing is that it
has to be done only once per each particular `serverless` user (the steps 1-6
can be skipped if the `ZappaLambdaDeploymentPolicy` policy already exist).

### Custom AWS IAM Roles and Policies for Execution

TBD...
