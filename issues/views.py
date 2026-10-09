
import json
from datetime import datetime
from pathlib import Path

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import (
    Reporter,
    Issue,
    CriticalIssue,
    LowPriorityIssue,
)


# JSON files are stored in the project's root folder
BASE_DIR = Path(__file__).resolve().parent.parent

REPORTERS_FILE = BASE_DIR / "reporters.json"
ISSUES_FILE = BASE_DIR / "issues.json"


# Helper function to read JSON data
def read_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# Helper function to save JSON data
def write_data(file_path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


# Helper function to read the request body
def get_request_data(request):
    try:
        return json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise ValueError("Invalid JSON")


# =========================
# REPORTER ENDPOINTS
# =========================

@csrf_exempt
def reporters_api(request):
    # GET /api/reporters/
    if request.method == "GET":
        reporters = read_data(REPORTERS_FILE)
        reporter_id = request.GET.get("id")

        if reporter_id is not None:
            try:
                reporter_id = int(reporter_id)
            except ValueError:
                return JsonResponse(
                    {"error": "Invalid reporter ID"},
                    status=400,
                )

            for reporter in reporters:
                if reporter["id"] == reporter_id:
                    return JsonResponse(reporter, status=200)

            return JsonResponse(
                {"error": "Reporter not found"},
                status=404,
            )

        return JsonResponse(reporters, safe=False, status=200)

    # POST /api/reporters/
    if request.method == "POST":
        try:
            data = get_request_data(request)

            reporter = Reporter(
                id=data["id"],
                name=data["name"],
                email=data["email"],
                team=data["team"],
            )
            reporter.validate()

            reporters = read_data(REPORTERS_FILE)

            if any(r["id"] == reporter.id for r in reporters):
                return JsonResponse(
                    {"error": "Reporter ID already exists"},
                    status=400,
                )

            reporters.append(reporter.to_dict())
            write_data(REPORTERS_FILE, reporters)

            return JsonResponse(
                reporter.to_dict(),
                status=201,
            )

        except ValueError as error:
            return JsonResponse({"error": str(error)}, status=400)
        except KeyError as error:
            return JsonResponse(
                {"error": f"Missing field: {error.args[0]}"},
                status=400,
            )
        except (TypeError, AttributeError):
            return JsonResponse(
                {"error": "Invalid reporter data"},
                status=400,
            )

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405,
    )


# =========================
# ISSUE ENDPOINTS
# =========================

@csrf_exempt
def issues_api(request):
    # GET /api/issues/
    if request.method == "GET":
        issues = read_data(ISSUES_FILE)

        issue_id = request.GET.get("id")
        status_filter = request.GET.get("status")

        # GET /api/issues/?id=1
        if issue_id is not None:
            try:
                issue_id = int(issue_id)
            except ValueError:
                return JsonResponse(
                    {"error": "Invalid issue ID"},
                    status=400,
                )

            for issue in issues:
                if issue["id"] == issue_id:
                    return JsonResponse(issue, status=200)

            return JsonResponse(
                {"error": "Issue not found"},
                status=404,
            )

        # GET /api/issues/?status=open
        if status_filter is not None:
            if status_filter not in Issue.ALLOWED_STATUSES:
                return JsonResponse(
                    {"error": "Invalid status"},
                    status=400,
                )

            filtered_issues = [
                issue
                for issue in issues
                if issue["status"] == status_filter
            ]

            return JsonResponse(
                filtered_issues,
                safe=False,
                status=200,
            )

        # GET /api/issues/
        return JsonResponse(issues, safe=False, status=200)

    # POST /api/issues/
    if request.method == "POST":
        try:
            data = get_request_data(request)

            # Choose the correct class based on priority
            if data["priority"] == "critical":
                issue = CriticalIssue(
                    id=data["id"],
                    title=data["title"],
                    description=data["description"],
                    status=data["status"],
                    priority=data["priority"],
                    reporter_id=data["reporter_id"],
                )

            elif data["priority"] == "low":
                issue = LowPriorityIssue(
                    id=data["id"],
                    title=data["title"],
                    description=data["description"],
                    status=data["status"],
                    priority=data["priority"],
                    reporter_id=data["reporter_id"],
                )

            else:
                issue = Issue(
                    id=data["id"],
                    title=data["title"],
                    description=data["description"],
                    status=data["status"],
                    priority=data["priority"],
                    reporter_id=data["reporter_id"],
                )

            # Validate the issue before saving it
            issue.validate()

            issues = read_data(ISSUES_FILE)

            if any(existing["id"] == issue.id for existing in issues):
                return JsonResponse(
                    {"error": "Issue ID already exists"},
                    status=400,
                )

            # Check that the reporter exists
            reporters = read_data(REPORTERS_FILE)

            if not any(
                reporter["id"] == issue.reporter_id
                for reporter in reporters
            ):
                return JsonResponse(
                    {"error": "Reporter not found"},
                    status=400,
                )

            # Add creation time to the stored record
            issue_data = issue.to_dict()
            issue_data["created_at"] = str(datetime.now())

            issues.append(issue_data)
            write_data(ISSUES_FILE, issues)

            # Include the subclass's describe() message in the response
            response_data = issue.to_dict()
            response_data["message"] = issue.describe()

            return JsonResponse(response_data, status=201)

        except ValueError as error:
            return JsonResponse({"error": str(error)}, status=400)
        except KeyError as error:
            return JsonResponse(
                {"error": f"Missing field: {error.args[0]}"},
                status=400,
            )
        except (TypeError, AttributeError):
            return JsonResponse(
                {"error": "Invalid issue data"},
                status=400,
            )

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405,
    )
