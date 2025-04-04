import os
from typing import Optional

from pydantic import BaseModel, field_validator
import yaml

from jira_api import IssueType, JiraAPI, LinkType, Priority
from env_vars import get_env_vars


class Link(BaseModel):
    """
    Class representing a link between tasks.
    """
    type: str
    issue_key: str

    @field_validator("type")
    @classmethod
    def check_link_type(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and value not in LinkType._member_names_:
            raise ValueError(f"Invalid link type: {value}. Must be one of {LinkType._member_names_}.")
        return value


class Task(BaseModel):
    """
    Class representing a task with its attributes.
    """
    summary: str
    description: str | None = None
    assignee: str | None = None
    priority: str | None = None
    links: list[Link] | None = None
    labels: list[str] | None = None

    @field_validator("priority")
    @classmethod
    def check_priority(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and value not in Priority._member_names_:
            raise ValueError(f"Invalid priority: {value}. Must be one of {Priority._member_names_}.")
        return value


def create_task(task: Task):
    """
    Create a task with the given parameters.

    Args:
        task (Task): The task object containing the task details.
    """
    priority = [priority_enum for priority_enum in Priority if priority_enum.name == task.priority][0] if task.priority else None
    try:
        assignee_id = jira_api.find_users(task.assignee)[0]['accountId'] if task.assignee else None
    except IndexError:
        raise ValueError(f"User {task.assignee} not found in Jira.")
    
    result = jira_api.create_issue(
        project_key='MRC',
        issue_type=IssueType.TASK,
        summary=task.summary,
        description=task.description,
        priority=priority,
        assignee_id=assignee_id,
        labels=task.labels
    )
    if task.links:
        for link in task.links:
            link_type = [link_type_enum for link_type_enum in LinkType if link_type_enum.name == link.type][0]
            jira_api.add_issue_link(
                link_type=link_type,
                inward_issue_key=result['key'],
                outward_issue_key=link.issue_key
            )
    print(f"Task created: {get_env_vars().JIRA_URL}/browse/{result['key']}")
    

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))

    jira_api = JiraAPI(
        base_url='https://mercuryo.atlassian.net/', 
        email=get_env_vars().JIRA_EMAIL, 
        api_token=get_env_vars().JIRA_API_TOKEN
    )

    with open(os.path.join(current_dir, "tasks.yaml"), "r") as file:
        tasks_raw_data = yaml.safe_load(file)
    tasks_data = [Task(**task) for task in tasks_raw_data["tasks"]]
    for task in tasks_data:
        create_task(task)
