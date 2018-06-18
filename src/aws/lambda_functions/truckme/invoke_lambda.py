import json
import gzip
import boto3
import base64


def invoke_events():

    lambda_client = boto3.client('lambda', 'us-east-2')

    request = {
        "httpMethod": "GET",
        "pathParameters": {
            "proxy": "proxy"
        },
        "queryStringParameters": {
            "start_date": "2018-05-13T14:00:00",
            "end_date": "2018-05-13T15:00:00",
            "bundle_id": "com.lc.robots.tanks.of.war.game",
            "os": "android",
            "foo": "foo",
            "columns": "country_code,city,user_id,version,os_version"
        }
    }

    var = lambda_client.invoke(
        FunctionName='truckme',
        InvocationType='RequestResponse',
        Payload=json.dumps(request),
    )

    body = json.loads(var["Payload"].read().decode("utf-8"))["body"]
    body_decompress = gzip.decompress(base64.b64decode(body))

    print(f'{body_decompress}')


if __name__ == '__main__':

    invoke_events()
