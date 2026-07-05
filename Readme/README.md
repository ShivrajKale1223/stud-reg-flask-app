# 🎓 Flask-Based Student Registration Web Application
### Deployed using Jenkins CI/CD on AWS EC2

---

## 📌 Project Overview

This project is a **Flask-based web application** that allows users to register students by submitting their details via a web form. The application stores submitted data in a **MySQL database** and provides the ability to retrieve and display this information. The entire deployment is automated using **Jenkins CI/CD pipeline** on **AWS EC2**.

---

## 🏗️ Architecture

![alt text](Pic%200.png)

---

## 🛠️ Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML, CSS |
| Backend | Python (Flask) |
| Database | MySQL |
| Web Server | Gunicorn + Nginx |
| CI/CD | Jenkins |
| Cloud | AWS EC2 (t3.micro) |
| Version Control | Git & GitHub |
| OS | Ubuntu 22.04 LTS |

---

## ☁️ AWS Infrastructure

| Instance | Name | Type | IP | Purpose |
|----------|------|------|----|---------|
| EC2 #1 | Jenkins | t3.micro | 18.206.150.67 | Jenkins CI/CD Server |
| EC2 #2 | flask-student-app | t3.micro | 34.201.32.53 | Flask App + MySQL |

---

## 📋 Functional Requirements

### ✅ 1. Student Registration Form
- Fields: Name, Email, Phone, Course, Address, Contact
- Client-side and server-side validation
- Success/failure flash messages

### ✅ 2. Data Handling
- Form data stored in MySQL database on form submission
- Data persists across sessions

### ✅ 3. Data Retrieval
- View all registered students at `/students`
- Data displayed in tabular format

### ✅ 4. CI/CD Pipeline
- Automated deployment on every GitHub push
- Jenkins pipeline with 4 stages

---

## 🔁 Jenkins Pipeline Stages

```
Stage 1: Pull Code          → git pull from GitHub to App Server
Stage 2: Install Dependencies → pip install -r requirements.txt
Stage 3: Restart Flask App  → sudo systemctl restart flaskapp
Stage 4: Verify             → Check app is active (running)
```

---

## 📁 Project Structure

```
stud-reg-flask-app/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── jenkins                 # Jenkins pipeline script
├── templates/
│   ├── index.html          # Home page
│   ├── register.html       # Registration form
│   └── students.html       # View all students
└── README.md
```

---

## ⚙️ Setup Instructions

### Prerequisites
- AWS Account
- Two EC2 instances (Ubuntu 22.04)
- GitHub Account
- Git installed locally

### EC2 1 — Jenkins Server Setup

```bash
# Install Java
sudo apt update
sudo apt install openjdk-17-jdk -y

# Install Jenkins
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | \
  sudo tee /usr/share/keyrings/jenkins-keyring.asc > /dev/null
echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | \
  sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt update
sudo apt install jenkins -y
sudo systemctl start jenkins
sudo systemctl enable jenkins
```

### EC2 2 — Flask App Server Setup

```bash
# Install dependencies
sudo apt update
sudo apt install python3 python3-pip python3-venv git mysql-server -y
sudo apt install python3-dev default-libmysqlclient-dev build-essential pkg-config -y

# Clone repository
git clone https://github.com/ShivrajKale1223/stud-reg-flask-app.git
cd stud-reg-flask-app

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install flask flask-mysqldb gunicorn

# Setup MySQL
sudo mysql -u root
```

```sql
CREATE DATABASE student_db;
CREATE USER 'flaskuser'@'localhost' IDENTIFIED BY 'Flask@1234';
GRANT ALL PRIVILEGES ON student_db.* TO 'flaskuser'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Run Flask App as Service

```bash
sudo nano /etc/systemd/system/flaskapp.service
```

```ini
[Unit]
Description=Flask Student App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/stud-reg-flask-app
Environment="PATH=/home/ubuntu/stud-reg-flask-app/venv/bin"
ExecStart=/home/ubuntu/stud-reg-flask-app/venv/bin/gunicorn \
  --workers 3 --bind 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl daemon-reload
sudo systemctl start flaskapp
sudo systemctl enable flaskapp
```

---

## 🔗 GitHub Webhook Configuration

```
GitHub Repo → Settings → Webhooks → Add Webhook
Payload URL  : http://18.206.150.67:8080/github-webhook/
Content type : application/json
Events       : Just the push event
```

---

## 🚀 Jenkins Pipeline Script

```groovy
pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        APP_SERVER = '34.201.32.53'
        APP_DIR = '/home/ubuntu/stud-reg-flask-app'
        KEY = '/var/lib/jenkins/.ssh/mykey.pem'
    }

    stages {
        stage('Pull Code') {
            steps {
                sh """
                    ssh -i ${KEY} -o StrictHostKeyChecking=no ubuntu@${APP_SERVER} '
                        cd ${APP_DIR} && git pull origin main
                    '
                """
            }
        }
        stage('Install Dependencies') {
            steps {
                sh """
                    ssh -i ${KEY} -o StrictHostKeyChecking=no ubuntu@${APP_SERVER} '
                        cd ${APP_DIR} &&
                        source venv/bin/activate &&
                        pip install -r requirements.txt
                    '
                """
            }
        }
        stage('Restart Flask App') {
            steps {
                sh """
                    ssh -i ${KEY} -o StrictHostKeyChecking=no ubuntu@${APP_SERVER} '
                        sudo systemctl restart flaskapp
                    '
                """
            }
        }
        stage('Verify') {
            steps {
                sh """
                    ssh -i ${KEY} -o StrictHostKeyChecking=no ubuntu@${APP_SERVER} '
                        sudo systemctl status flaskapp | grep "active (running)"
                    '
                """
            }
        }
    }

    post {
        success { echo '✅ Deployment Successful!' }
        failure { echo '❌ Deployment Failed!' }
    }
}
```

---

## 📸 Screenshots

### 1. AWS EC2 Instances — Both Running
![EC2 Instances](Pic%201.png)

### 2. Jenkins Dashboard — Pipeline Success
![Jenkins Dashboard](Pic%202.png)

### 3. Jenkins Build History — Multiple Successful Builds
![Build History](Pic%203.png)

### 4. Jenkins Console Output — Deployment Successful
![Console Output](Pic%204.png)

### 5. Jenkins Trigger — GitHub Hook Configured
![Jenkins Trigger](Pic%205.png)

### 6. GitHub Repository
![GitHub Repo](Pic%206.png)

### 7. GitHub Webhook — Last Delivery Successful
![GitHub Webhook](Pic%207.png)

### 8. Student Registration Form
![Registration Form](Pic%208.png)

### 9. Form Validation Working
![Form Validation](Pic%209.png)

### 10. Registered Students List
![Students List](Pic%2010.png)

---

## 🌐 Application URLs

| Page | URL |
|------|-----|
| Registration Form | http://34.201.32.53 |
| All Students | http://34.201.32.53/students |
| Jenkins Dashboard | http://18.206.150.67:8080 |

---

## 🔒 Security Groups Configuration

### Jenkins Server (EC2 1)
| Port | Protocol | Purpose |
|------|----------|---------|
| 22 | TCP | SSH Access |
| 8080 | TCP | Jenkins Web UI |

### App Server (EC2 2)
| Port | Protocol | Purpose |
|------|----------|---------|
| 22 | TCP | SSH Access |
| 80 | TCP | HTTP Web Access |
| 5000 | TCP | Flask App Port |

---

## 👨‍💻 Author

**Shivraj Bapu Kale**
- GitHub: [ShivrajKale1223](https://github.com/ShivrajKale1223)
- Repository: [stud-reg-flask-app](https://github.com/ShivrajKale1223/stud-reg-flask-app)

---

## 📝 Key Components Explained

| Component | Explanation |
|-----------|-------------|
| Flask | Python web framework to handle routes and forms |
| MySQL | Relational database to store student records |
| Gunicorn | Production WSGI server for Flask |
| Jenkins | CI/CD tool to automate deployment |
| GitHub Webhook | Notifies Jenkins on every code push |
| EC2 | AWS virtual machines to host the application |
| Systemd Service | Keeps Flask app running automatically |

---

*Project — Flask-Based Student Registration Web Application deployed using Jenkins*
