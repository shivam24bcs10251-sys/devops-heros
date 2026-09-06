# Session 7 — Docker Images (multi-stage builds & compose)

## Multi-stage build

A multi-stage Dockerfile uses a **builder** stage to install/compile and a
separate slim **production** stage that copies only what is needed, keeping the
final image small and free of build-time cruft.

```dockerfile
# Stage 1: Build
FROM node:24-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

# Stage 2: Production
FROM node:24-alpine AS production
WORKDIR /app
COPY --from=builder /app/package*.json ./
RUN npm install --omit=dev
COPY --from=builder /app/server.js ./
EXPOSE 3000
CMD ["npm", "start"]
```

Build and run:

![multi-stage build & run](./Outputs/multi_stage_output_1.png)

Verify the single production image and the running container:

![verify image & container](./Outputs/multi_stage_output_2.png)

The app served in the browser:

![multi-stage web](./Outputs/multi_stage.png)

## Docker Compose (nginx + redis)

`docker compose` brings up multiple services together. Here `web` (nginx,
published on `:8080`) depends on a `redis` service.

```yaml
services:
  web:
    image: nginx:alpine
    ports:
      - "8080:80"
    depends_on:
      - redis
  redis:
    image: redis:alpine
```

![docker compose ps](./Outputs/docker_compose_output.png)

![docker compose web](./Outputs/docker_compose_web.png)
