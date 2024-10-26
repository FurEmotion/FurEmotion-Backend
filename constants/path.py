import os

PROJECT_DIR = os.getcwd()
ASSET_DIR = f'{PROJECT_DIR}/assets'
DATASET_DIR = f'{PROJECT_DIR}/dataset'
CRY_INSPECT_LOG_DIR = f'{DATASET_DIR}/cry_inspect_logs'
CRY_DATASET_DIR = f'{DATASET_DIR}/cry_dataset'
PET_PROFILE_DIR = f'{DATASET_DIR}/pet_profiles'

for path in [ASSET_DIR, DATASET_DIR, CRY_DATASET_DIR, CRY_INSPECT_LOG_DIR, PET_PROFILE_DIR]:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
