from constants import BUCKET_NAME


class TestsBucket:
    def test_s3_output_name(self):
        # Test if bucket name setting is valid.
        bucket_name = self.outputs.get("bucketName").value
        self.assertIn(f"{BUCKET_NAME}-bucket", bucket_name)

    def test_s3_exist(self):
        # Test if bucket is created successfully.
        buckets = self.s3.buckets.all()
        bucket_names = []
        for bucket in buckets:
            bucket_names.append(bucket.name)

        bucket_name = self.outputs.get("bucketName").value
        self.assertIn(bucket_name, bucket_names)

    def test_s3_create_permission(self):
        # Test creating a file in new s3 bucket.
        bucket_name = self.outputs.get("bucketName").value
        created_response = self.s3.Bucket(bucket_name).put_object(
            Key=self.FILE_NAME, Body="Hi"
        )
        self.assertEqual(created_response.key, self.FILE_NAME)

    def test_s3_delete_permission(self):
        # Test deleting the created file in new s3 bucket.
        bucket_name = self.outputs.get("bucketName").value
        delete_response = self.s3.meta.client.delete_object(
            Bucket=bucket_name, Key=self.FILE_NAME
        )
        self.assertIsNotNone(delete_response)
