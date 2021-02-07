from utils.s3_writer import HandlerS3Writer

extracted_file="test_file.txt"
extraction_name="test_file.txt"
extraction_source="testing"
bucket="health-lake-input"
HandlerS3Writer(extracted_file, extraction_name, extraction_source, bucket)