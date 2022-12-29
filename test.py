
import boto3
import argparse


def main(commit_message, branch):
    if "deploy" in commit_message:
      info = commit_message.split(":")[1]
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--commit_message", help="commit message")
    parser.add_argument("-b", "--branch", help="branch name")

    args = parser.parse_args()

    main(args.commit_message, args.branch)


