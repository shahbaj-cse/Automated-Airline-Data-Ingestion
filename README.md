# Automated-Airline-Data-Ingestion
This project automates the ingestion, processing, and storage of airline data in Amazon Redshift. The workflow is triggered by an S3 event when new files are uploaded to a specific S3 location. AWS Step Functions orchestrate the process, with each step handling different stages of data ingestion and error handling.
