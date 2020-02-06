[![Travis CI Build Status](https://travis-ci.com/CiscoSecurity/tr-05-serverless-relay.svg?branch=develop)](https://travis-ci.com/CiscoSecurity/tr-05-serverless-relay)

# Relay API Template

A generic Relay API template not bound to any third-party Threat Intelligence
service provider. The template aims to show the general structure for future
implementations. It also provides a couple of utility functions that might be
handy. Keep in mind that the main idea here is to just give a hint of a
possible approach rather than enforcing to do everything exactly the same way.

The API itself is just a simple Flask (WSGI) application which can be easily
packaged and deployed as an AWS Lambda Function working behind an AWS API
Gateway proxy using [Zappa](https://github.com/Miserlou/Zappa).

An already deployed Relay API (e.g., packaged as an AWS Lambda Function) can
be pushed to Threat Response as a Relay Module using the
[Threat Response Relay CLI](https://github.com/threatgrid/tr-lambda-relay).

## Installation

```bash
pip install -U -r requirements.txt
```

## Testing

```bash
pip install -U -r test-requirements.txt
```

- Check for *PEP 8* compliance: `flake8 .`.
- Run the suite of unit tests: `pytest -v tests/unit/`.

## Deployment

```bash
pip install -U -r deploy-requirements.txt
```

As an AWS Lambda Function:
- Deploy: `zappa deploy dev`.
- Check: `zappa status dev`.
- Update: `zappa update dev`.
- Monitor: `zappa tail dev --http`.

**Note.** Check the following [document](aws/README.md) for more detailed
information and a set of concrete instructions on proper AWS setup.

As a TR Relay Module:
- Create: `relay add`.
- Update: `relay edit`.
- Delete: `relay remove`.

**Note.** For convenience, each TR Relay CLI command may be prefixed with
`env $(cat .env | xargs)` to automatically read the required environment
variables from a `.env` file (i.e.`TR_API_CLIENT_ID`, `TR_API_CLIENT_PASSWORD`,
`URL`, `JWT`) and pass them to the corresponding command.

## Usage

```bash
pip install -U -r use-requirements.txt
```

```bash
export URL=<...>
export JWT=<...>

http POST "${URL}"/health Authorization:"Bearer ${JWT}"
echo '[{"type": "...", "value": "..."}, ...]' | http POST "${URL}"/deliberate/observables Authorization:"Bearer ${JWT}" ...
echo '[{"type": "...", "value": "..."}, ...]' | http POST "${URL}"/observe/observables Authorization:"Bearer ${JWT}" ...
echo '[{"type": "...", "value": "..."}, ...]' | http POST "${URL}"/refer/observables Authorization:"Bearer ${JWT}" ...
echo '[{"type": "...", "value": "..."}, ...]' | http POST "${URL}"/respond/observables Authorization:"Bearer ${JWT}" ...
http POST "${URL}"/respond/trigger Authorization:"Bearer ${JWT}" action-id=... observable_type=... observable_value=...
```
