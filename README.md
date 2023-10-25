# Data Processing & Analytics Pipeline with AWS and Airflow

This repository outlines a data processing and analytics pipeline leveraging AWS services and Apache Airflow. The main objective is to automate the process of fetching data, storing it in AWS, processing with Glue and Athena, and preparing it for visualization.

## Dataset Source

The data used in this pipeline is sourced from Kaggle, specifically the [Telco Customer Churn (IBM) Dataset](https://www.kaggle.com/datasets/yeanzc/telco-customer-churn-ibm-dataset?resource=download).

## Use Cases

### Data Querying with Athena

Once the data has been processed and stored, analysts or other data professionals can directly query the dataset using Amazon Athena. This provides a serverless interactive query service that simplifies the analysis of data in Amazon S3 using standard SQL. Analysts can use Athena to generate insights, build reports, or create datasets for further use.

### Data Visualization

While this pipeline does not directly include a dashboard, it prepares the data in such a way that it can easily be connected to visualization tools like Tableau, PowerBI, or other reporting tools. Users can connect to the data stored in Amazon Redshift or directly from Athena to build visual reports and dashboards. This flexibility allows organizations to pick a visualization tool that best fits their needs and expertise.

## Diagram Overview

![Pipeline Diagram](aws_churn_pipeline.pptx.jpg)

1. **Data Download**: Source data from the Internet.
2. **Amazon S3**: Store data in an S3 bucket.
3. **AWS Glue Crawler**: Extract schema and create metadata tables.
4. **Amazon Athena**: Query data directly from S3.
5. **Amazon Redshift**: Store processed data for complex analytics.

## Code Structure

- Apache Airflow DAG: Automates data transfer from S3 to Redshift using AWS Glue.

### Workflow:

1. Trigger the AWS Glue job to transfer data from S3 to Redshift.
2. Fetch the Glue job's run ID.
3. Monitor the Glue job's status using a sensor.

## Getting Started

### Prerequisites

- AWS account with permissions to S3, Glue, Athena, and Redshift.
- Apache Airflow setup.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/pjvillasista/customer-churn-aws-ETL/
   ```

2. Configure your AWS credentials:
   ```bash
   aws configure
   ```

3. Set up your Apache Airflow environment.

4. Place the DAG in your Airflow DAGs directory.

### Usage

1. Start the Airflow web server:
   ```bash
   airflow webserver
   ```

2. Trigger the DAG from the Airflow UI.

3. Once data is processed and saved in Redshift, use PowerBI to connect to your Redshift cluster for visualization.

## Contributing

If you'd like to contribute to this project, please fork the repository, create your feature branch, commit your changes, and open a pull request.
