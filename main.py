import json

from vin_decoder import VINDecoder
import pandas as pd

patterns_df = pd.read_csv('model_patterns_27_11_2023.csv')

vd = VINDecoder(patterns_df)
def lambda_handler(event, context):
    vin = event['vin']  # No need for json.loads here

    if not vin:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'VIN is required'})
        }

    vin = vin.strip()
    vin = vin.upper()
    vd.vin = vin

    if not vd.is_valid:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Invalid VIN'})
        }

    if not vd.is_wmi_exist:
        return {
            'statusCode': 422,
            'body': json.dumps({'message': f"{vin[:3]} WMI not exists"})
        }
    try:
        return {
            'statusCode': 200,
            'body': vd.decode()
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f"Internal Server Error {str(e)}"})
        }

# if __name__ == '__main__':
#     event = {
#         'vin': "5NPD84LFXJH246284"  # No need to use json.dumps here
#     }
#
#     # Mock context (optional, depends on your use case)
#     context = {}
#
#     # Call the lambda handler
#     response = lambda_handler(event, context)
#
#     # Print the response
#     print(json.dumps(response, indent=4))
