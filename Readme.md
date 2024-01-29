# Road Detection
## Overview
Project Description

## Getting Started

1. Clone the Repository:
   ```bash
   git clone https://github.com/silvadirceu/Road_detection_CNN.git
   cd road-scanner
   ```
2. Setup Environment Variables:

Copy the `.env.example` file to a new file named `.env` and configure the necessary environment variables. Adjust the values according to your deployment requirements.

```bash
cp .env.example .env
```
3. Deploy docker-compose
```bash
docker-compose -f docker-compose.yml
```

3. Monitoring
Monitoring services are listed:
- RabbitMQ - Port: 15672
- Flower - Port: 5555