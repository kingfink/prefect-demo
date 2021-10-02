import time

from prefect.storage.github import GitHub
from prefect import task, Flow, Parameter
from prefect.run_configs import ECSRun

@task
def say_hello():
    time.sleep(10)

    logger.info(f'Hello!')

with Flow('hello-flow-ecs-github') as flow:
    say_hello()

flow.storage = GitHub(
    repo='king-fink/prefect-demo', 
    path='hello_flow_ecs_github.py', 
    ref='main'
)

flow.run_config = ECSRun(
    cpu='.25 vCPU',
    memory='0.5 GB',
    task_role_arn='arn:aws:iam::134777600073:role/prefectTaskRole',
    execution_role_arn='arn:aws:iam::134777600073:role/prefectECSAgentTaskExecutionRole',
    run_task_kwargs=dict(cluster='prefectEcsCluster', launchType='FARGATE'),
    env={'GREETING': 'Hello'},
    image='prefecthq/prefect:latest-python3.7'
)

flow.register(
    project_name='Prefect Tutorial',
    labels=['prod'],
    add_default_labels=False
)
