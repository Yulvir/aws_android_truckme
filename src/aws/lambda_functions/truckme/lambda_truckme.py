import os
import sys
import json
import gzip
import qrcode
import base64
import datetime
from io import BytesIO
from hurry.filesize import size
import psycopg2
if os.uname()[1] == "ncarvalho-GL502VMK":
    import library_functions.library_functions.logger.logger_configurator as logger_configurator
else:
    import library_functions.logger.logger_configurator as logger_configurator

logger = logger_configurator.get_logger(__name__)


def gzip_b64encode(data):

    """
    This function is used before send response data to compress using gzip and encode using Base64Encoded.
    :param data: response data before be sent
    :return: response data compressed and encoded
    """

    start_time = datetime.datetime.now()

    compressed = BytesIO()
    with gzip.GzipFile(fileobj=compressed, mode='w') as f:
        data_byte = data.tobytes()
        f.write(base64.b64encode(data_byte))

    logger.info(f'Response data without compress is about {size(sys.getsizeof(data))}')
    logger.info(f'Response data compressed and encoded in UTF-8 is about'
                f' {size(sys.getsizeof(base64.b64encode(compressed.getvalue()).decode("utf-8")))}')

    end_time = datetime.datetime.now()
    duration = (end_time - start_time).total_seconds()
    logger.info(f'The execution time of compression process was {duration} seconds')

    #return base64.b64encode(compressed.getvalue()).decode('utf-8')
    return base64.b64encode(compressed.getvalue()).decode('utf-8')


def create_response(message):

    """
    Function to wrap data in structured response which is needed by API Gateway.
    "body" key will be sent compressed and encoded
    :param message: data or message which be sent to the user
    :return: dict with necessary keys to API Gateway
    """

    logger.info(f'Response data on "Body" before encoding is ==> {message}')

    #body_message = gzip_b64encode(message)
    body_message = base64.b64encode(message).encode("UTF-8")

    return {
        "isBase64Encoded": True,
        'statusCode': 200,
        'body': json.dumps(body_message),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
            },

        }


def lambda_handler(event, context):
    try:
        conn = psycopg2.connect("dbname='PostgresqlTruckme' "
                                "user='cresko' "
                                "host='postgresql.cleytat6tuvh.us-east-2.rds.amazonaws.com' "
                                "password='postgresql-truckme' "
                                "connect_timeout=5")

        cur = conn.cursor()
        cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
        cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",(100, "abc'def"))
        cur.execute("SELECT * FROM test;")
        cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        logger.error(msg=" Couldn't connect to posgres", extra={"ERROR": e})

        return create_response(e)


    if 'body' in event:
        event = event

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data('Trucks Secret')
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    response_body = {
        "qr_code": img,
    }

    return create_response(img)


if __name__ == '__main__':

    with open('input.json') as file:
        event = file.read()

    print(lambda_handler(event, None))