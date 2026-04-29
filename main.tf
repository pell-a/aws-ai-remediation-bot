provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "insecure_bucket" {
  bucket = "test-bucket"
}

resource "aws_s3_bucket_ownership_controls" "insecure_bucket" {
  bucket = aws_s3_bucket.insecure_bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_public_access_block" "insecure_bucket" {
  bucket = aws_s3_bucket.insecure_bucket.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}