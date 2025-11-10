# Multi-stage build for full-stack deployment
FROM node:18 AS frontend-build

# Build frontend
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

FROM python:3.11-slim

# Install Python dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY src/ ./src/

# Copy built frontend
COPY --from=frontend-build /app/frontend/dist ./frontend/dist

# Expose port
EXPOSE 8000

# Environment variables
ENV PORT=8000

# Start both services
# Serve frontend static files through FastAPI
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]

