from dagster import repository
from pipeline.jobs import full_pipeline

@repository
def project_repo():
    return [full_pipeline] 