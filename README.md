# Trading Signal Parser Bot

A desktop-based Python application that converts raw trading messages into structured JSON and publishes them to Kafka for downstream processing.

This project is designed to handle real-world, unstructured trading alerts and extract meaningful fields **without failing when data is missing**.

---

## 🔹 Key Features

- Parses multiple formats of trading messages
- Gracefully ignores missing or unavailable fields
- Kafka producer integration for message streaming
- Clean and user-friendly Tkinter UI
- Automatic CST (Central Standard Time) tagging
- Limit buffer calculation (10% above limit when available)
- Dockerized Kafka setup (Zookeeper + Kafka)

---

## 🛠️ Tech Stack

- Python 3
- Tkinter (Desktop UI)
- Apache Kafka
- Docker & Docker Compose
- Regex-based parsing

---
---

## ▶️ How to Run the Project

### 1️⃣ Prerequisites

- Python 3.9 or higher
- Docker & Docker Compose
- Git

---

### 2️⃣ Start Kafka (Docker)

```bash
docker compose up -d