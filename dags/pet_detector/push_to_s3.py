import boto3

def upload_file_to_s3(endpoint_url, bucket_name, key, file_path):
    s3 = boto3.client('s3',
                      endpoint_url=endpoint_url,
                      aws_access_key_id='dummy-access-key-id',
                      aws_secret_access_key='dummy-secret-access-key')

    # Check if the bucket exists
    try:
        s3.head_bucket(Bucket=bucket_name)
    except:
        # Create the bucket if it doesn't exist
        s3.create_bucket(Bucket=bucket_name)

    with open(file_path, 'rb') as f:
        s3.upload_fileobj(f, bucket_name, key)
