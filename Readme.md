# Cleaning Leads SaaS - Turnkey Deployment

## Overview
This is a ready-to-use SaaS for cleaning businesses to collect leads via Facebook Messenger.

- Multi-tenant: each business owner has their own dashboard
- Secure: OAuth for Facebook Page connections
- Optional email notifications for new leads
- Payoneer workflow for payment collection

## Setup Instructions

### 1. Environment
1. Install Python 3.10+ and pip.
2. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt

