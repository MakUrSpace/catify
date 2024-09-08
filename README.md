# catify
Catify a phrase

## Local Dev Steps


## AWS Installation Steps
1. `npm install -g aws-cdk`
1. `python3 -m venv venv`
1. `source venv/bin/activate`
1. `pip install -r aws/requirements.txt`
1. [Set AWS Profile environment variables](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-envvars.html) to your account's credentials
1. `cdk bootstrap aws://{account id}/{app region}`
1. `cdk deploy -a aws/catify_static_site.aws.py`

## Local development
1. `python3 -m venv venv`
1. `source venv/bin/activate`
1. `python -m http.server` -- [http://localhost:8000/catify.html](http://localhost:8000/catify.html)
