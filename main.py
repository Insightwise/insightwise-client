import os
from time import sleep

from client.client import Client
from client.dashboards.models import DashboardCreate, DashboardStatus
from client.documents.models import DocumentCreate, DocumentStatus
from client.insights.models import InsightCardStatus
from client.project.models import ProjectCreate

POLL_INTERVAL = 10


def run():
    client = Client()
    client.authenticate(os.environ["USER"], os.environ["PASS"])

    # Create a project
    project = client.projects.create(data=ProjectCreate(name="API test"))

    # Upload all the documents to the project
    file_paths = [
        "Employee Interview 1.docx",
        "Employee Interview 2.docx"
    ]
    documents = [
        client.documents.upload(
            payload=DocumentCreate(name="test.docx"),
            project_id=project.id,
            file=file
        )
        for file in file_paths
    ]
    doc_ids = [d.id for d in documents]

    # Create the analysis dashboard with the newly created documents
    dashboard = client.dashboards.create(
        data=DashboardCreate(name="Dashboard #1", document_ids=doc_ids),
        project_id=project.id,
    )

    # Wait until files have been processed
    print(f"Processing files ...")
    progress = 0
    credit_cost = 0
    while progress < 100:
        documents = client.documents.list(
            query_params=dict(id__in=dashboard.document_ids),
            project_id=dashboard.project_id
        )
        progress = sum([d.progress or 0 for d in documents.results]) / len(documents.results)
        credit_cost = sum([d.credit_cost or 0 for d in documents.results])
        print(f"\r\033[K{progress: .1f}%", end="", flush=True)

        failed_docs = list(filter(lambda d: d.status == DocumentStatus.FAILED, documents.results))
        for d in failed_docs:
            print(f"{d.name} failed")
        if len(failed_docs) > 0:
            exit(-1)
        sleep(POLL_INTERVAL)

    print(f"\nCredits consumed {credit_cost: .1f}")

    # Wait until dashboard has been processed
    print(f"Processing dashboard ...")
    while True:
        updated_dashboard = client.dashboards.get(dashboard.id, project_id=dashboard.project_id)
        print(f"\r\033[K{updated_dashboard.progress: .1f}%", end="", flush=True)

        if updated_dashboard.status == DashboardStatus.FAILED:
            print(f"Dashboard {dashboard.id} failed")
            exit(-1)
        elif updated_dashboard.progress >= 100:
            break
        sleep(POLL_INTERVAL)

    # Wait until insights are generated
    print(f"\nProcessing insights ...")
    while True:
        insights = client.insights.list(
            project_id=dashboard.project_id,
            dashboard_id=dashboard.id
        )
        finalised_insights = len(
            list(
                filter(lambda i: i.status in [InsightCardStatus.FAILED, InsightCardStatus.COMPLETE], insights.results)
            )
        )
        print(f"\r\033[K{finalised_insights} complete out of {insights.total_items}", end="", flush=True)
        if finalised_insights == insights.total_items:
            break
        sleep(POLL_INTERVAL)

    print(f"\nDashboard id '{dashboard.id}' has been processed. Insights are ready.")

    # Fetch the data (Insights, Themes, Evidence)
    insights = client.insights.list(project_id=dashboard.project_id, dashboard_id=dashboard.id)
    first_insight = insights.results[0]
    themes = client.dashboard_themes.list(project_id=dashboard.project_id, dashboard_id=dashboard.id)
    first_theme = themes.results[0]

    # List all evidence (paginated 100 per page)
    evidence = client.evidence.list(
        project_id=dashboard.project_id,
        dashboard_id=dashboard.id,
        query_params=dict(page=1)
    )

    # Evidence for a specific theme
    theme_evidence = client.evidence.list(
        project_id=dashboard.project_id,
        dashboard_id=dashboard.id,
        query_params=dict(page=1, related_insights__theme__in=[first_theme.theme])
    )

    # Evidence for a specific insight
    insight_evidence = client.evidence.list(
        project_id=dashboard.project_id,
        dashboard_id=dashboard.id,
        query_params=dict(page=1, related_insights__insight__in=[first_insight.description])
    )
    print(insights.results)
    print(themes.results)
    print(evidence.results)
    print(theme_evidence.results)
    print(insight_evidence.results)

if __name__ == "__main__":
    run()
