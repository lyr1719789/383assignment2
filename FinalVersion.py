import manual
import os

# 创建虚拟机,vm instance
os.system("gcloud deployment-manager deployments create my-deployment --template template.py")
os.system("gcloud compute instances delete-access-config deployment-vm --access-config-name 'External NAT'")
os.system("gcloud compute instances add-access-config deployment-vm --access-config-name \"External NAT\" --address %s"%manual.ip)
print("vm instance finished")

os.system("gcloud compute --project=%s firewall-rules create for-apache --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:80 --source-ranges=0.0.0.0/0"%manual.project)

os.system("gcloud compute --project=%s firewall-rules create open-ports1 --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:6000-7000 --source-ranges=0.0.0.0/0"%manual.project)
os.system("gcloud compute --project=%s firewall-rules create open-ports2 --direction=EGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:6000-7000 --destination-ranges=0.0.0.0/0"%manual.project)
os.system("gcloud compute --project=%s firewall-rules create open-ports3 --direction=EGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:20-21 --destination-ranges=0.0.0.0/0"%manual.project)
os.system("gcloud compute --project=%s firewall-rules create open-ports4 --direction=INGRESS --priority=1000 --network=default --action=ALLOW --rules=tcp:20-21 --source-ranges=0.0.0.0/0"%manual.project)


# 创建磁盘 --project=projectname,create disk
os.system("gcloud beta compute disks create backup --project=%s --type=pd-standard --size=500GB --zone=us-central1-a --physical-block-size=4096"%manual.project)
# 连接磁盘 --disk=diskname, connect disk
os.system("gcloud compute instances attach-disk deployment-vm --disk backup")
print("disk finished")

# 数据库添加网络，google sql connect instance
os.system("gcloud sql instances patch my-moodle --assign-ip")
os.system("gcloud sql instances patch my-moodle --authorized-networks=%s"%manual.ip)
print("add ip to sql finished")
