import manual
import os

# 创建虚拟机,vm instance
os.system("gcloud deployment-manager deployments create my-deployment --template template.py")
os.system("gcloud compute instances delete-access-config deployment-vm --access-config-name 'External NAT'")
os.system("gcloud compute instances add-access-config deployment-vm --access-config-name \"External NAT\" --address %s"%manual.ip)

# 创建磁盘 --project=projectname,create disk
os.system("gcloud beta compute disks create diskname --project=my-project-first-252603 --type=pd-standard --size=500GB --zone=us-central1-a --physical-block-size=4096")
# 连接磁盘 --disk=diskname, connect disk
os.system("gcloud compute instances attach-disk deployment-vm --disk backup")

# 数据库添加网络，google sql connect instance
os.system("gcloud sql instances patch my-moodle --assign-ip")
os.system("gcloud sql instances patch my-moodle --authorized-networks=%s")%manual.ip

# 配置phpmyadmin
os.system("wget https://files.phpmyadmin.net/phpMyAdmin/4.6.3/phpMyAdmin-4.6.3-all-languages.tar.bz2 ")
os.system("mkdir phpMyAdmin")
os.system("tar -xvf phpMyAdmin-4.6.3-all-languages.tar.bz2 -C phpMyAdmin --strip-components=1")
pathOfphp = os.path.abspath('phpMyAdmin')

# create app.yaml
os.chdir(pathOfphp)
os.system("sudo touch app.yaml")
pathOfapp = os.path.abspath('app.yaml')
os.chdir(pathOfapp)
os.system("sudo chmod o+r app.yaml")
os.system("sudo chmod o+w app.yaml")
yaml="service: default\nruntime: php55\napi_version: 1\n\nhandlers:\n\n- url: /(.+\.(ico|jpg|png|gif))$\n  static_files: \\1\n  upload: (.+\.(ico|jpg|png|gif))$\n  application_readable: true\n\n- url: /(.+\.(htm|html|css|js))$\n  static_files: \\1\n  upload: (.+\.(htm|html|css|js))$\n  application_readable: true\n\n- url: /(.+\.php)$\n  script: \\1\n  login: admin\n\n- url: /.*\n  script: index.php\n  login: admin"
Modified_file_1 = open(pathOfapp,"w")
Modified_file_1.write(yaml)
Modified_file_1.close()

# create config.inc.php
os.chdir(pathOfphp)
os.system("touch config.inc.php")
os.system("sudo chmod o+r config.inc.php")
os.system("sudo chmod o+w config.inc.php")
pathOfconfig = os.path.abspath('config.inc.php')
config="<?php\n$cfg[\'blowfish_secret\'] = 'phpMyAdmin';\n\n$i = 0;\n\n// Change this to use the project and instance that you've created.\n$host = '/cloudsql/%s';\n$type = 'socket';\n\n$i++;\n\n$cfg['Servers'][$i]['auth_type'] = 'cookie';\n\n$cfg['Servers'][$i]['socket'] = $host;\n$cfg['Servers'][$i]['connect_type'] = $type;\n$cfg['Servers'][$i]['compress'] = false;\n\n$cfg['Servers'][$i]['extension'] = 'mysqli';\n$cfg['Servers'][$i]['AllowNoPassword'] = true;\n\n$cfg['UploadDir'] = '';\n$cfg['SaveDir'] = '';\n\n$cfg['PmaNoRelation_DisableWarning'] = true;\n$cfg['ExecTimeLimit'] = 60;\n$cfg['CheckConfigurationPermissions'] = false;"%manual.sql_name
Modified_file_2 = open(pathOfconfig,"w")
Modified_file_2.write(config)
Modified_file_2.close()

# create php.ini
os.chdir(pathOfphp)
os.system("touch php.ini")
os.system("sudo chmod o+r php.ini")
os.system("sudo chmod o+w php.ini")
pathOfini = os.path.abspath('php.ini')
php="google_app_engine.enable_functions = \"php_uname, getmypid\""
Modified_file_3 = open(pathOfini,"w")
Modified_file_3.write(php)
Modified_file_3.close()


os.system("sudo /google/google-cloud-sdk/bin/gcloud components update")
os.system("sudo /google/google-cloud-sdk/bin/gcloud app deploy")