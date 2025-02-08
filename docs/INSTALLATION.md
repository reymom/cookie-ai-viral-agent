# 🚀 Installation & Setup Guide

This guide explains how to set up the **Obfuscated Cat Agent**.

## **1️⃣ Prerequisites**

- Python 3.8+
- Node.js 18+
- Redis Server (for Celery tasks)
- Solana CLI installed

## **2️⃣ Install Dependencies**

```bash
pip install -r backend/requirements.txt
cd solana && npm install
```

## **3️⃣ Start Backend Services**

```bash
redis-server
celery -A config.celery worker --loglevel=info
celery -A config.celery beat --loglevel=info
```

## **4️⃣ Deploy a Video Token**

```bash
python -m scripts.test_deploy_token
```

For full details, read the main **[README.md](./README.md)**
