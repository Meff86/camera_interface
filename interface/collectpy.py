import os
import boto3

AWS_S3_ACCESS_KEY_ID = 'YCAJED2HUj8DMX6N6ROlMjD4O'
AWS_S3_SECRET_ACCESS_KEY = 'YCMZKYsIcf9dQN7MC_Hoe9-8mQhZcxusZb4VeZu1'
AWS_STORAGE_BUCKET_NAME = 'meff1986'
AWS_S3_ENDPOINT_URL = 'https://storage.yandexcloud.net'


def download_folder(date_string, local_path):
    s3 = boto3.client('s3',
                      aws_access_key_id=AWS_S3_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_S3_SECRET_ACCESS_KEY,
                      endpoint_url=AWS_S3_ENDPOINT_URL)

    folder_name = date_string

    objects = s3.list_objects_v2(Bucket=AWS_STORAGE_BUCKET_NAME, Prefix=folder_name)

    if 'Contents' in objects:
        for obj in objects['Contents']:
            key = obj['Key']
            filename = os.path.join(local_path, key)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            s3.download_file(AWS_STORAGE_BUCKET_NAME, key, filename)
            print(f"Downloaded: {key}")
    else:
        print(f"No folder found for date: {date_string}")


if __name__ == "__main__":
    # Введите название даты в формате "гггг_мм_дд"
    date_string = input("Enter date in the format 'yyyy_mm_dd': ")

    # Локальный путь для сохранения файлов
    local_path = 'downloaded_folder'

    download_folder(date_string, local_path)
    print("Download complete.")
