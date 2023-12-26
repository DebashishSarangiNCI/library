import boto3
from botocore.exceptions import ClientError
from botocore.exceptions import NoCredentialsError
import pandas as pd
from io import StringIO

class FinanceCalculator:
    def __init__(self, region='eu-west-1'):
        self.lambda_client = boto3.client('lambda', region_name=region)
        self.s3_client = boto3.client('s3', region_name=region)

    def compound_interest(self, principal, rate, time):
        # Calculation logic
        payload = {
            "principal": principal,
            "rate": rate,
            "time": time
        }
        try:
            response = self.invoke_lambda_function('finance', payload)
            return response['Payload'].read().decode('utf-8')
        except (NoCredentialsError, ClientError) as e:
            print(f"Error during compound interest calculation: {e}")
            return None

    def invoke_lambda_function(self, function_name, payload):
        try:
            response = self.lambda_client.invoke(
                FunctionName=function_name,
                Payload=str(payload)
            )
            return response
        except ClientError as e:
            print(f"Error invoking Lambda function: {e}")
            return None

    def upload_to_s3(self, file_name, bucket_name):
        try:
            with open(file_name, 'rb') as file:
                self.s3_client.upload_fileobj(file, bucket_name, file_name)
            print(f"{file_name} uploaded to {bucket_name} on S3")
        except ClientError as e:
            print(f"Error uploading to S3: {e}")

# Example usage:
calculator = FinanceCalculator()
result = calculator.compound_interest(1000, 0.05, 3)
if result:
    print("Compound Interest:", result)
else:
    print("Failed to calculate compound interest.")

data = {
    'Date': ['2023-01-01', '2023-01-02', '2023-01-03'],
    'Stock': ['AAPL', 'GOOGL', 'MSFT'],
    'Price': [150.25, 2000.0, 180.50],
    'Volume': [1000000, 500000, 750000],
}

df = pd.DataFrame(data)


csv_buffer = StringIO()
df.to_csv(csv_buffer, index=False)
csv_buffer.seek(0)

# Initialize AWS S3 client
s3 = boto3.client('s3',
                  aws_access_key_id='x22162844@student.ncirl.ie',
                  aws_secret_access_key='Kni8@6110786')

bucket_name = 'createforcsv'  
file_name = 'financial_data.csv'

# Upload CSV file to S3 bucket
s3.put_object(Bucket=bucket_name, Key=file_name, Body=csv_buffer.getvalue().encode())
print(f"File '{file_name}' uploaded to '{bucket_name}' bucket successfully.")
