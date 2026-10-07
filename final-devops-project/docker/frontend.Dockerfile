FROM node:24-alpine AS build
WORKDIR /app
COPY application/frontend/package*.json ./
RUN npm ci
COPY application/frontend/ ./
RUN npm run build
FROM nginxinc/nginx-unprivileged:stable-alpine
USER root
RUN apk upgrade --no-cache
COPY --from=build /app/dist /usr/share/nginx/html
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
USER 101:101
EXPOSE 8080
