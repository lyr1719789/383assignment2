import os

# 创建数据库，google sql
os.system("gcloud sql tiers list")
os.system("gcloud sql instances create my-moodle --tier=db-f1-micro --region=asia-southeast1")
os.system("gcloud sql instances patch --assign-ip my-moodle")
os.system("gcloud sql users set-password root --host % --instance my-moodle --password Moodle123moodle")

# gcloud sql connect my-moodle --user=root
