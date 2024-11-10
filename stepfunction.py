{
  "Comment": "A description of my state machine",
  "StartAt": "StartCrawler",
  "States": {
    "StartCrawler": {
      "Type": "Task",
      "Parameters": {
        "Name": "daily_raw_crawler"
      },
      "Resource": "arn:aws:states:::aws-sdk:glue:startCrawler",
      "Next": "GetCrawler"
    },
    "GetCrawler": {
      "Type": "Task",
      "Parameters": {
        "Name": "daily_raw_crawler"
      },
      "Resource": "arn:aws:states:::aws-sdk:glue:getCrawler",
      "Next": "Crawler Status Check"
    },
    "Crawler Status Check": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.Crawler.State",
          "StringMatches": "RUNNING",
          "Next": "Wait"
        }
      ],
      "Default": "Glue StartJobRun"
    },
    "Wait": {
      "Type": "Wait",
      "Seconds": 10,
      "Next": "GetCrawler"
    },
    "Glue StartJobRun": {
      "Type": "Task",
      "Resource": "arn:aws:states:::glue:startJobRun.sync",
      "Parameters": {
        "JobName": "airline-data-ingestion"
      },
      "Next": "Glue-Job Status Check",
      "Catch": [
        {
          "ErrorEquals": [
            "States.TaskFailed"
          ],
          "Comment": "Glue Job Failed",
          "Next": "failed_notification"
        }
      ]
    },
    "Glue-Job Status Check": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.JobRunState",
          "StringMatches": "SUCCEEDED",
          "Next": "success_notification"
        }
      ],
      "Default": "failed_notification"
    },
    "failed_notification": {
      "Type": "Task",
      "Resource": "arn:aws:states:::sns:publish",
      "Parameters": {
        "Message": "Glue Job Execution Failed !!",
        "TopicArn": "arn:aws:sns:us-east-1:940482409720:first_sns"
      },
      "End": true
    },
    "success_notification": {
      "Type": "Task",
      "Resource": "arn:aws:states:::sns:publish",
      "Parameters": {
        "TopicArn": "arn:aws:sns:us-east-1:940482409720:first_sns",
        "Message": "Glue Job Execution Successfull"
      },
      "End": true
    }
  }
}