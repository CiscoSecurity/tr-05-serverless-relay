[![Travis CI Build Status](https://travis-ci.com/CiscoSecurity/tr-05-serverless-relay.svg?branch=develop)](https://travis-ci.com/CiscoSecurity/tr-05-serverless-relay)

# Relay Template

Generic Relay template not bound to any real third-party Threat Intelligence
service provider.

**NOTE.** The template aims to show the general structure for future
implementations. It also provides a couple of utility functions that might be
handy. Keep in mind that the main idea here is to just give you a hint of a
possible approach rather than enforcing you to do everything exactly the same
way.

The Relay itself is just a simple application written in Python that can be
easily packaged and deployed as an AWS Lambda Function using
[Zappa](https://github.com/Miserlou/Zappa).

## Rationale

1. We need an application that will translate API requests from Threat Response
to the third-party integration, and vice versa. This application is provided
here in the GitHub repository, and we are going to install it in AWS Lambda
using Zappa.

2. AWS Lambda allows us to deploy our application without deploying a dedicated
server or paying for so called "idle" cycles. AWS handles instantiation and
resource provisioning; all we need to do is define the access rights and upload
our application.

3. Zappa is a helper tool that will package our application and publish it to
AWS as a Lambda function. It abstracts a large amount of manual configuration
and requires only a very simple configuration file, which we have provided and
will explain how to customize it during this process.

## Preparation

To get started, you have to configure your AWS environment and encode your
third-party credentials into a JWT using a generated secret key.

### AWS

Check the [AWS HOWTO](aws/HOWTO.md) for more details on how to properly set up
your AWS environment first. Make sure to thoroughly carry out any instructions
from that document. In addition, it also covers how to configure the
[Zappa Settings](zappa_settings.json) by explaining the relationships between
the values there and your AWS setup.

### JWT

In brief, [JSON Web Token (JWT)](https://en.wikipedia.org/wiki/JSON_Web_Token)
is a way of encoding any JSON data into a signed token. The signature ensures
the integrity of the data, i.e. the fact that it has not been changed in any
way in transit between the sender and the recipient.

The JWT standard supports many different algorithms for signing tokens but we
are interested in HS256. The algorithm requires to generate (and securely store
somewhere) a 256-bit (i.e. 64-character) string a.k.a. the secret key.

Once a secret key has been generated and used for encoding your third-party
credentials into a JWT, the token has to be provided on each request to the
application as the `Authorization: Bearer <JWT>` header (this will be
automatically done for you if you create a corresponding module in Threat
Response). Unless the signature verification fails, the application will decode
the token to restore your original third-party credentials and will try to
authenticate to the corresponding third-party service on your behalf.

Probably, the easiest way to generate your JWT is to use the interactive
Debugger located on [JWT.IO](https://jwt.io/). You just have to go through the
following steps:

1. Select the HS256 algorithm from the drop-down list and make sure that the
Header section of the Decoded pane looks like this:
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

2. Make sure your third-party credentials has already been converted to JSON.
Copy and paste them into the Payload section of the Decoded pane. Notice that
the actual structure of your payload is integration-specific so it has to be
explicitly documented for each particular third-party integration. Here is an
example of how it may look like:
```json
{
  "username": "gdavoian",
  "password": "4everYoung!"
}
```

3. In the Verify Signature section of the Decoded pane replace the
`your-256-bit-secret` placeholder with your actual secret key.

4. Your JWT must already be in the Encoded pane. It is ready to use!

Do not worry, the tool does not record your data, everything is done on the
client side.

Make sure to save both the secret key and the token so that we can refer to
them later on. Let us name those as `SECRET_KEY` and `JWT` respectively.

## Installation

First of all, make sure that you already have Python 3 installed by typing
```
python3 --version
```
in your command-line shell.

The application has been implemented and tested using `Python 3.7`. You may try
to use any higher versions if you wish as they should be backward-compatible.

After that, you have to create a "virtual environment" to isolate the
application-specific requirements from the libraries globally installed to your
system. Here are the steps to follow:

1. Create a virtual environment named `venv`:

   `python3 -m venv venv`

2. Activate the virtual environment:
   - Linux/Mac: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate.bat`

3. Upgrade PIP (optional):

   `pip install --upgrade pip`

**NOTE**. The virtual environment has to be created only once, you just have
to make sure to activate it each time you are working on or playing with the
application (modern IDEs can automatically do that for you). You can deactivate
a previously activated virtual environment by simply typing `deactivate` in
your command-line shell.

Finally, install the libraries required for the application to function from
the [requirements.txt](requirements.txt) file:

```
pip install --upgrade --requirement requirements.txt
```

## Deployment

Besides the application's requirements, you also have to install a couple of
extra tools from the [deploy-requirements.txt](deploy-requirements.txt) file
for actually deploying the application:
```
pip install --upgrade --requirement deploy-requirements.txt --upgrade-strategy eager
```

To `deploy` your application to AWS as a Lambda function for the first time,
run the following command:
```
zappa deploy dev
```

**NOTE**. Here `dev` is just the name of the default stage. You may define as
many stages as you like. Each Zappa command requires a stage to be specified so
make sure to replace `dev` with the name of your custom stage when necessary.

**NOTE**. If you are experiencing any problems with running the command then
check the [AWS Common Errors](aws/CommonErrors.md) guide on troubleshooting
of some most common types of errors.

You can check the `status` of your deployment with the corresponding command:
```
zappa status dev
```

Once the Lambda has been deployed, make sure to set the `SECRET_KEY`
environment variable introduced in the [JWT](#JWT) section. This is important
since the Lambda has to know the `SECRET_KEY` so that it can verify and decode
the `JWT` from incoming requests. Check the
[AWS Environment Variables](aws/EnvironmentVariables.md) guide on passing
arbitrary environment variables to Lambdas.

Also, do not forget to save the public `URL` to your Lambda returned by Zappa.
It will look like this:
```
https://<RANDOM_ID>.execute-api.<AWS_REGION>.amazonaws.com/<ZAPPA_STAGE>
```

Notice that you have to `deploy` your Lambda only once. Each time you make
changes to the source code or to the settings file you just have to `update`
the Lambda by running the following command:
```
zappa update dev
```

As a bonus, you can also monitor your Lambda's HTTP traffic in near real-time
with the `tail` command:
```
zappa tail dev --http
```

If you do not need your Lambda anymore you can run the following command to
get rid of it altogether and clean up the underlying resources:
```
zappa undeploy dev
``` 

**NOTE**. The `deploy` command always returns a brand new `URL`. The `update`
command does not change the current `URL`. The `undeploy` command destroys the
old `URL` forever.

TBD...

## Testing (optional)

If you want to test the application you have to install some additional
dependencies from the [test-requirements.txt](test-requirements.txt) file:
```
pip install --upgrade --requirement test-requirements.txt
```

You can perform two kinds of testing:

- Run static code analysis checking for any semantic discrepancies and
[PEP 8](https://www.python.org/dev/peps/pep-0008/) compliance:

  `flake8 .`

- Run the suite of unit tests and measure the code coverage:

  `coverage run --source api/ -m pytest --verbose tests/unit/ && coverage report`

## Implementation Details

**NOTE.** Remember that this application is just a template so here `N/A` means
that it has no implemented Relay endpoints and supported types of observables.
That will not be the case for real integrations with third-party services so
you may consider the next sections as some placeholders.

### Implemented Relay Endpoints

`N/A`

### Supported Types of Observables

`N/A`

### [JWT](#JWT) Payload Structure

```json
{}
```

**NOTE.** This particular implementation does not make any requests to external
services, it only verifies that your `JWT` has been signed with your
`SECRET_KEY`. Thus, no real credentials are necessary, and you may use any JSON
payload for encoding.
