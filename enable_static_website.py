# enable_static_website.py
import os
from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient, StaticWebsite

ACCOUNT = os.environ["STORAGE_ACCOUNT_NAME"]
account_url = f"https://{ACCOUNT}.blob.core.windows.net"

cred = DefaultAzureCredential()
service = BlobServiceClient(account_url, credential=cred)

service.set_service_properties(
    static_website=StaticWebsite(
        enabled=True,
        index_document="index.html",
        error_document404_path="404.html",   # <-- SEE WARNING BELOW
    )
)
print("Verifying live configuration state via Read-Back...")

live_properties = service.get_service_properties()


static_web_config = live_properties.get('static_website') if isinstance(live_properties, dict) else getattr(live_properties, 'static_website', None)

if static_web_config:
    
    if isinstance(static_web_config, dict):
        actual_404_path = static_web_config.get('error_document404_path')
    else:
        actual_404_path = getattr(static_web_config, 'error_document404_path', None)
else:
    actual_404_path = None


try:
    assert actual_404_path == "404.html", (
        f"CRITICAL ERROR: 404 page routing was silently dropped! "
        f"Expected '404.html', but cloud reports: '{actual_404_path}'"
    )
    print(f"✅ SUCCESS: 404 error routing verified. Live state: '{actual_404_path}'")
except AssertionError as e:
    print(f"❌ VALIDATION FAILED: {e}")
    sys.exit(1)