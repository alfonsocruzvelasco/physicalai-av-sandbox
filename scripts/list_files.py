from huggingface_hub import HfApi

REPO_ID = "nvidia/PhysicalAI-Autonomous-Vehicles"
api = HfApi()
files = api.list_repo_files(repo_id=REPO_ID, repo_type="dataset")

print("file_count:", len(files))
for f in files[:200]:
    print(f)
