import mimetypes
import os
from io import BytesIO
from typing import Union

import requests

from client.base_client import BaseClient
from client.documents.models import Document, DocumentCreate, DocumentUpdate


class DocumentClient(BaseClient[Document, DocumentCreate, DocumentUpdate]):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            endpoint="/v1/organisations/{organisation_id}/projects/{project_id}/project-documents",
            model=Document,
            create_model=DocumentCreate,
            update_model=DocumentUpdate,
            require_ids=["project_id"]
        )

    def upload(
        self,
        payload: DocumentCreate,
        file: Union[str, BytesIO],
        project_id: str,
        auto_confirm_credits: bool = True,
        verbose=True,
    ) -> Document:
        # Step 1: Prepare file content, size, and mime type
        if isinstance(file, str):
            guessed_type, _ = mimetypes.guess_type(file)
            mime_type = guessed_type or "application/octet-stream"
            file_size = os.path.getsize(file)
            with open(file, "rb") as f:
                file_data = f.read()
        elif isinstance(file, BytesIO):
            file.seek(0, os.SEEK_END)
            file_size = file.tell()
            file.seek(0)
            file_data = file.getvalue()
            mime_type = payload.content_type or "application/octet-stream"  # fallback
        else:
            raise TypeError("File must be a file path or a BytesIO object.")

        # Step 2: Add metadata to payload
        payload.size = file_size
        payload.content_type = mime_type

        # Step 3: Create the document (with updated metadata)
        document = self.create(payload, project_id=project_id)
        upload_url = document.url

        if not upload_url:
            raise ValueError("No upload URL provided in response document.")

        # Step 4: Upload to the signed URL
        upload_response = requests.put(upload_url, data=file_data, headers={"Content-Type": payload.content_type})

        if upload_response.status_code not in (200, 201):
            raise RuntimeError(f"File upload failed with status {upload_response.status_code}")

        # Step 5: Patch the document with upload completion info
        updated_document = self.update(
            item_id=document.id,
            data=DocumentUpdate(
                status="UPLOADED",
                confirmed=auto_confirm_credits,
            ),
            project_id=project_id,
        )

        if verbose:
            print(f"Uploaded document {payload.name}")

        return updated_document
