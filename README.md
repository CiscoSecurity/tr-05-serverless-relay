[![Travis CI Build Status](https://travis-ci.com/CiscoSecurity/tr-05-serverless-relay.svg?branch=develop)](https://travis-ci.com/CiscoSecurity/tr-05-serverless-relay)

# Relay Template

A generic Relay template not bound to any real third-party Threat Intelligence
service provider.

**NOTE.** The template aims to show the general structure for future
implementations. It also provides a couple of utility functions that might be
handy. Keep in mind that the main idea here is to just give a hint of a
possible approach rather than enforcing to do everything exactly the same way.

The Relay itself is just a simple application written in Python that can be
easily packaged and deployed as an AWS Lambda Function using
[Zappa](https://github.com/Miserlou/Zappa).

## Rationale

1. We need an application that will translate API requests from CTR to the
third-party integration, and vice versa. This application is provided here in
the GitHub repository, and we are going to install it in AWS Lambda using Zappa.

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
third-party credentials into a JWT token using some generated secret key.

### AWS

Check the [AWS HOWTO](aws/HOWTO.md) for more details on how to properly set up
your AWS environment first. Make sure to thoroughly carry out any instructions
from that document. In addition, it also covers how to configure the
[Zappa Settings](zappa_settings.json) by explaining the relationships between
the values there and your AWS setup.

### JWT

In brief, JWT is a way of encoding any JSON data into a signed token. The
signature ensures the integrity of the data, i.e. the fact that it has not been
changed in any way in transit between the sender and the recipient.

The JWT standard supports many different algorithms for signing tokens but we
are interested in HS256. The algorithm requires to generate (and securely store
somewhere) a 256-bit (i.e. 64-character) string a.k.a. the secret key.

Once a secret key has been generated and used for encoding your third-party
credentials into a JWT token, the token has to be provided on each request to
the application as the `Authorization: Bearer <JWT>` header (this will be
automatically done for you if you create a corresponding module in CTR). Unless
the signature verification fails, the application will decode the token to
restore your original third-party credentials and will try to authenticate to
the corresponding third-party service on your behalf.

Probably, the easiest way to generate your JWT token is to use the interactive
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
the actual format of your payload is integration-specific so it has to be
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

4. Your JWT token must already be in the Encoded pane. It is ready to use!

Do not worry, the tool does not record your data, everything is done on the
client side.

Make sure to save both the secret key and the token so that we can refer to
them later on. Let us name those as `SECRET_KEY` and `JWT` respectively.

## Installation

TBD...
