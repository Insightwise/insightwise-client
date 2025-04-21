# InsightWise Python Client

A lightweight Python client to interact with the InsightWise API, including project creation, document uploading, dashboard generation, and insight extraction.

## 📦 Installation

You can install directly from GitHub:

```bash
pip install git+https://github.com/insightwise/insightwise-client.git
```

## 🔧 Environment Variables

Before using the client, set the following environment variables:

| Variable         | Description                             |
|------------------|-----------------------------------------|
| `BASE_URL`       | The base URL for the InsightWise API.   |
| `CLIENT_ID`      | Cognito app client ID.                  |
| `USER_POOL_ID`   | Cognito user pool ID.                   |
| `REGION`         | The aws region                          |
| `USER`           | Your InsightWise username (email).      |
| `PASS`           | Your InsightWise password.              |

Example:

```bash
export BASE_URL=https://your-api.example.com
export CLIENT_ID=abc123xyz456
export USER_POOL_ID=ap-southeast-2_example
export REGION=ap-southeast-2
export USER=your@email.com
export PASS=yourpassword
```

## 🚀 Getting Started

Here's a simple example of how to use the client (For a full example check out main.py):

```python
from client.client import Client
from client.project.models import ProjectCreate
from client.documents.models import DocumentCreate
from client.dashboards.models import DashboardCreate, DashboardStatus
from time import sleep
import os

client = Client()
client.authenticate(os.environ["USER"], os.environ["PASS"])

# Create a new project
project = client.projects.create(data=ProjectCreate(name="API Test"))

# Upload documents
documents = [
    client.documents.upload(
        payload=DocumentCreate(name="Document 1"),
        project_id=project.id,
        file="Employee Interview 1.docx"
    ),
    client.documents.upload(
        payload=DocumentCreate(name="Document 2"),
        project_id=project.id,
        file="Employee Interview 2.docx"
    )
]

# Create dashboard with the documents
doc_ids = [doc.id for doc in documents]
dashboard = client.dashboards.create(
    data=DashboardCreate(name="Dashboard #1", document_ids=doc_ids),
    project_id=project.id,
)

# Poll dashboard progress
while True:
    updated = client.dashboards.get(dashboard.id, project_id=project.id)
    print(f"\rProgress: {updated.progress:.1f}%", end="", flush=True)
    if updated.progress >= 100:
        break
    sleep(10)

print("\nDashboard processing complete!")
```

## 🧱 Features

- ✅ **Authentication** with Cognito SRP
- 📁 Create and manage **Projects**
- 📄 Upload **Documents** via signed URL
- 📊 Create and poll **Dashboards**
- 💡 Extract **Insights**, **Themes**, and **Evidence**
- 📎 Full support for query params and pagination

## 🧪 Example Usage

See [`main.py`](./main.py) for a full working example.

## 🛠 Development

1. Clone the repository
2. Install dependencies with:

```bash
pip install -r requirements.txt
```

## 📄 License

MIT License.
