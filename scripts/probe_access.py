from huggingface_hub import HfApi

REPO_ID = "nvidia/PhysicalAI-Autonomous-Vehicles"
api = HfApi()
info = api.dataset_info(REPO_ID)

print("OK:", info.id)
print("gated:", getattr(info, "gated", None))
print("private:", getattr(info, "private", None))
