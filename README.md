# Automated-Airline-Data-Ingestion
This project automates the ingestion, processing, and storage of airline data in Amazon Redshift. The workflow is triggered by an S3 event when new files are uploaded to a specific S3 location. AWS Step Functions orchestrate the process, with each step handling different stages of data ingestion and error handling.

### Workflow Summary

1. **Data Upload**: New airlines_booking_data files are uploaded to a specific S3 bucket.
2. **Event Trigger**: EventBridge detects file uploads and triggers an AWS Step Function.
3. **Data Crawling**: AWS Glue catalogs the data in the Glue Data Catalog.
4. **ETL Job**: AWS Glue Jobs performs ETL and loads data into Redshift.
5. **Notifications**: Success and failure notifications are sent via SNS to email.

### Table of Contents

2. [Architecture Diagram](#architecture_diagram)
3. [Prerequisites](#prerequisites)
4. [Repository Outline](#repository-outline)
5. [Deployment Guide](#deployment-guide)
6. [Testing the Pipeline](#testing-the-pipeline)
7. [Troubleshooting](#troubleshooting)
8. [License](#license)

---

## Architecture Diagram

![Architecture Diagram](architecture.png)

---

## Prerequisites

- **AWS Account**: Free Tier or higher, with permissions to use S3, EventBridge, Step Functions, Glue, Redshift, and SNS.
- **AWS CLI**: Configured with appropriate IAM permissions.
- **Redshift Cluster**: With JDBC connection details.
- **SNS Topic**: For email notifications.

---
