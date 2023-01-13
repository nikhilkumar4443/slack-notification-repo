import json
import boto3


def lambda_handler(event, context):
    print(event)
    jira_details = event["Records"][0]["Sns"]['Message']
    summary = jira_details['automationData']['Summary']
    description = jira_details['automationData']['Description']
    print(description)
    print(summary)
    
    info = description.split(":")[1]
    project_name,env_name,cluster = info.split(",")
    client = boto3.client('codepipeline', region_name="us-east-1")
    pipeline_name = f'project-ecs-{project_name}-{env_name}-{cluster}'
    print(pipeline_name)
    response= client.get_pipeline(name=pipeline_name)
    
    response['pipeline']['stages'][0]['actions'][0]['configuration']['Branch'] = branch
    print(f"updating the pipeline {pipeline_name}")
    
    client.update_pipeline(
        pipeline=response['pipeline']
    )
    print(f"starting the pipeline {pipeline_name}")
    
    resp=client.start_pipeline_execution(
      name=pipeline_name
    )
    
    print(f"Pipeline started successfully verfiy the execution status execution ID {resp['pipelineExecutionId']}")
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
