```sh
# deploy serverless framework
serverless deploy --region ap-southeast-1

python3 -m venv venv
source venv/bin/activate

serverless plugin install -n serverless-python-requirements 
pip install requests
pip freeze > requirements.txt
```