#!/usr/bin/env bash

library_functions='../../../../library_functions'
# For now we will put this script in the same folder than lambda function
lambda_function_path='lambda_truckme.py'
deploy_dir='/tmp/deploy_lambda_api/input'

mkdir -p ${deploy_dir}
cp -r ${library_functions} ${deploy_dir}
cp -r ${lambda_function_path} ${deploy_dir}
cd ${deploy_dir}
cd ../
virtualenv env --python=python3.6
source env/bin/activate
pip3 install input/library_functions > /dev/null 2>&1

mkdir env_content
cp -r env/lib/python3.6/site-packages/* env_content/
cp input/lambda_truckme.py env_content/
cd env_content/
zip -r truckme.zip . > /dev/null 2>&1
mv -f truckme.zip ../
cd ..
pwd
aws s3 cp truckme.zip s3://lambda-zips-truckme/
aws --region us-east-2 lambda update-function-code --function-name truckme --s3-bucket lambda-zips-truckme --s3-key truckme.zip
deactivate
cd ..
rm -rf deploy_lambda_api