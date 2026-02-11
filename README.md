# Marathonic  Production-Style Flask Web Server on Raspberry Pi

##  Overview
Marathonic is a secure, production-style web application deployed on a Raspberry Pi using a hardened Linux environment. The project demonstrates real-world infrastructure practices including reverse proxy architecture, service orchestration, least-privilege execution, and secure deployment techniques.

The application allows users to track marathon runs while showcasing secure web hosting and system administration skills relevant to cybersecurity and DevOps roles.

---

## Architecture
**Application Layer**
- Python Flask Web Application
- MVC style routing and templating
- SQLite Database

**Web Server Layer**
- Nginx Reverse Proxy
- Port 80 traffic forwarding to internal Flask app (Port 5000)

**Process Management**
- Systemd service for persistent background execution
- Automatic restart on crash or reboot

**Security Practices**
- Python virtual environment (dependency isolation)
- Principle of Least Privilege (non-root service user)
- Reverse proxy isolation from direct internet access
- Log monitoring and system troubleshooting

---

## Security Features
- Non-root Linux service account execution
- Reverse proxy architecture to protect internal services
- Secure dependency management using Python venv
- Systemd service hardening
- Configuration syntax validation (`nginx -t`)
- Log analysis via systemd journal

---

## Technologies Used
- Raspberry Pi (Linux)
- Python 3
- Flask
- SQLite3
- Nginx
- Systemd
- Bash/Linux CLI
- pm2

---

## Deployment Steps (Simplified)
```bash
# Clone repository
git clone https://github.com/xAriees/marathonic.git

# Enter directory
cd marathonic

# Create virtual environment
python3 -m venv venv

# Activate environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start service
sudo systemctl start Marathonic
