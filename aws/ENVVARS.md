# AWS Environment Variables

**Note.** Feel free to skip this document until you have deployed your Lambda
(check the [AWS HOWTO](HOWTO.md) document for more details on how to properly
set up your AWS environment first). But once your Lambda has been successfully
deployed, make sure to return back to this document for some extra configuration
tweaks.

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

Thus, you can securely store your environment variables and dynamically change
them at run-time without having to re-deploy anything.
