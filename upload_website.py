import boto3
import os
import mimetypes

s3 = boto3.client("s3")

BUCKET_NAME = "aws-capstone-static-website-2026-kunal-004"
WEBSITE_FOLDER = "website"
REGION = "ap-south-1"


def create_bucket():
    try:
        s3.head_bucket(Bucket=BUCKET_NAME)
        print(f"Bucket already exists: {BUCKET_NAME}")

    except Exception:
        s3.create_bucket(
            Bucket=BUCKET_NAME,
            CreateBucketConfiguration={
                "LocationConstraint": REGION
            }
        )
        print(f"Bucket created successfully: {BUCKET_NAME}")


def configure_website():
    s3.put_bucket_website(
        Bucket=BUCKET_NAME,
        WebsiteConfiguration={
            "IndexDocument": {
                "Suffix": "index.html"
            }
        }
    )

    endpoint = (
        f"http://{BUCKET_NAME}.s3-website."
        f"{REGION}.amazonaws.com"
    )

    print("Static website hosting configured successfully.")
    print(f"Website endpoint: {endpoint}")


def upload_files():
    for root, directories, files in os.walk(WEBSITE_FOLDER):

        for file_name in files:

            local_path = os.path.join(root, file_name)

            relative_path = os.path.relpath(
                local_path,
                WEBSITE_FOLDER
            )

            s3_key = relative_path.replace("\\", "/")

            content_type, _ = mimetypes.guess_type(local_path)

            if content_type is None:
                content_type = "application/octet-stream"

            s3.upload_file(
                local_path,
                BUCKET_NAME,
                s3_key,
                ExtraArgs={
                    "ContentType": content_type
                }
            )

            print(
                f"Uploaded: {s3_key} ({content_type})"
            )


if __name__ == "__main__":
    create_bucket()
    configure_website()
    upload_files()

    print("\nDeployment completed successfully.")