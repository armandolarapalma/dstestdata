def loadtostorage(bucket, dfpast, name):
    from google.cloud import storage
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket)
    df_procesed = dfpast
    bucket.blob(name).upload_from_string(df_procesed.to_csv(), 'text/csv') 