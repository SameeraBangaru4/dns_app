# Docker Fibonacci System

## Overview

This project runs a Fibonacci system using Docker Compose.  
It allows you to:

1. Build and start the containers
2. Register a hostname
3. Test the Fibonacci calculation through a browser

---

## 1️⃣ Build and Start Containers

Run the following command:

```bash
docker compose up --build
```

This will build the images and start all required services.

---

## 2️⃣ Register the Host

After the containers are running, execute:

```bash
curl -X PUT http://127.0.0.1:9090/register \
-H "Content-Type: application/json" \
-d '{
  "hostname": "fibonacci.com",
  "ip": "fs",
  "as_ip": "as",
  "as_port": "53533"
}'
```

This registers the hostname in the system.

---

## 3️⃣ Test the System

Open the following URL in your browser:

```
http://127.0.0.1:8080/fibonacci?hostname=fibonacci.com&fs_port=9090&number=23&as_ip=as&as_port=53533
```

If everything is working correctly, the system will return the Fibonacci result for `23`.

---

## Notes

- Make sure Docker is installed and running.
- Ensure ports `8080` and `9090` are available.
- If needed, stop containers with:

```bash
docker compose down
```
