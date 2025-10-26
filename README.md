
# Serverless Email API

A **Serverless REST API** built using the **Serverless Framework** and **SendGrid**, allowing you to send emails by providing the recipient email, subject, and body. The API is fully tested locally with **Serverless Offline** and includes robust error handling.

---

## Table of Contents

* [Features](#features)
* [Prerequisites](#prerequisites)
* [Installation](#installation)
* [Environment Variables](#environment-variables)
* [Running Locally](#running-locally)
* [API Endpoints](#api-endpoints)
* [Error Handling](#error-handling)
* [License](#license)

---

## Features

* REST API to send emails using **SendGrid**
* Input validation for `receiver_email`, `subject`, and `body_text`
* Proper HTTP response codes for success and errors (`200`, `400`, `401`, `403`, `500`)
* Local testing using **Serverless Offline**
* CORS headers enabled for frontend integration

---

## Prerequisites

* **Python 3.9+**
* **Node.js** (for Serverless Framework)
* **Serverless Framework** (`npm install -g serverless`)
* **SendGrid API key**

---

## Installation

1. Clone the repository:

```bash
git clone <your-repo-url>
cd serverless-email-api
```

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Install Serverless Offline plugin:

```bash
npm install
```

---

## Environment Variables

Set the following environment variables before running the project:

| Variable           | Description                       |
| ------------------ | --------------------------------- |
| `SENDGRID_API_KEY` | Your SendGrid API key             |
| `FROM_EMAIL`       | Verified sender email in SendGrid |

For local testing, you can set them in your terminal:

```bash
set SENDGRID_API_KEY=your_sendgrid_api_key
set FROM_EMAIL=your_verified_email
```

---

## Running Locally

Start the API with **Serverless Offline**:

```bash
serverless offline
```

You should see:

```
POST | http://localhost:8080/dev/send-email
```

The API is now running locally on port 8080.

---

## API Endpoints

### **Send Email**

**URL:** `POST /dev/send-email`
**Content-Type:** `application/json`

**Request Body:**

```json
{
  "receiver_email": "recipient@example.com",
  "subject": "Email Subject",
  "body_text": "Email body content"
}
```

**Success Response (200 OK):**

```json
{
  "success": true,
  "message": "Email sent successfully",
  "messageId": "wZqfj0SKR4--kKDI9G4zBg",
  "data": {
    "receiver_email": "recipient@example.com",
    "subject": "Email Subject",
    "sent_at": "2025-10-26T11:53:33.427195Z"
  }
}
```

---

## Error Handling

* **400 Bad Request**: Missing fields, invalid JSON, invalid email format
* **401 Unauthorized**: Invalid SendGrid API key
* **403 Forbidden**: SendGrid API key lacks permissions
* **500 Internal Server Error**: Server misconfiguration or SendGrid service errors

Example error response:

```json
{
  "success": false,
  "error": "Missing required field",
  "message": "receiver_email is required"
}
```



