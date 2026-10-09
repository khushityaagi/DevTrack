from django.db import models


from abc import ABC, abstractmethod


# Parent class for all entities
class BaseEntity(ABC):

    @abstractmethod
    def validate(self):
        pass

    def to_dict(self):
        return {
            key: value
            for key, value in self.__dict__.items()
        }


# Reporter class
class Reporter(BaseEntity):

    def __init__(self, id, name, email, team):
        self.id = id
        self.name = name
        self.email = email
        self.team = team

    def validate(self):

        if not isinstance(self.id, int) or isinstance(self.id, bool):
            raise ValueError("Reporter ID must be an integer")
        
        if not self.name or not self.name.strip():
            raise ValueError("Name cannot be empty")

        if not self.email or "@" not in self.email:
            raise ValueError("Invalid email")


# Issue class
class Issue(BaseEntity):

    ALLOWED_STATUSES = [
        "open",
        "in_progress",
        "resolved",
        "closed"
    ]

    ALLOWED_PRIORITIES = [
        "low",
        "medium",
        "high",
        "critical"
    ]

    def __init__(
        self,
        id,
        title,
        description,
        status,
        priority,
        reporter_id
    ):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.reporter_id = reporter_id

    def validate(self):
        if not isinstance(self.id, int) or isinstance(self.id, bool):
            raise ValueError("Issue ID must be an integer")

        if not isinstance(self.reporter_id, int) or isinstance(self.reporter_id, bool):
            raise ValueError("Reporter ID must be an integer")
        
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")

        if self.status not in self.ALLOWED_STATUSES:
            raise ValueError("Invalid status")

        if self.priority not in self.ALLOWED_PRIORITIES:
            raise ValueError("Invalid priority")


    def describe(self):
        return f"{self.title} [{self.priority}]"


# Critical priority subclass
class CriticalIssue(Issue):

    def describe(self):
        return (
            f"[URGENT] {self.title} "
            "— needs immediate attention"
        )


# Low priority subclass
class LowPriorityIssue(Issue):

    def describe(self):
        return (
            f"{self.title} "
            "— low priority, handle when free"
        )

