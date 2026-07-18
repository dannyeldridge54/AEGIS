# AEGIS Optimizer — SaaS API Server
# Copyright (c) 2012-2026 Danny Lee Eldridge. All rights reserved.
#
# Build:  docker build -t aegis-optimizer .
# Run:    docker run -p 3000:3000 -e API_KEYS=your-key aegis-optimizer

FROM node:20-alpine

LABEL maintainer="Danny Lee Eldridge"
LABEL description="AEGIS Optimizer SaaS API Server"
LABEL version="1.0.0"

WORKDIR /app

# Copy package files first for layer caching
COPY package*.json ./
COPY sdk/package.json sdk/

# Install dependencies
RUN npm ci --omit=dev 2>/dev/null || npm install --omit=dev

# Copy source
COPY dist/ dist/
COPY seeker/dist/ seeker/dist/
COPY sdk/ sdk/
COPY saas/ saas/

# Build info
RUN echo "AEGIS Optimizer v1.0.0 — Built $(date -u +%Y-%m-%dT%H:%M:%SZ)" > /app/BUILD_INFO

ENV NODE_ENV=production
ENV PORT=3000

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s \
  CMD wget -qO- http://localhost:3000/api/health || exit 1

CMD ["node", "saas/server.js"]
