# this_file: Dockerfile
# 
# Multi-stage Dockerfile for Phiton
# Creates a small, efficient container for running Phiton

# Build stage
FROM python:3.12-slim as builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install UV
RUN curl -LsSf https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies and build
RUN uv venv --python 3.12 && \
    . .venv/bin/activate && \
    uv sync && \
    uv run python -m build --outdir dist

# Install the built package
RUN uv pip install --system dist/*.whl

# Runtime stage
FROM python:3.12-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash phiton

# Copy installed package from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin/phiton /usr/local/bin/phiton

# Set working directory
WORKDIR /workspace

# Switch to non-root user
USER phiton

# Set entrypoint
ENTRYPOINT ["phiton"]
CMD ["--help"]

# Add labels
LABEL org.opencontainers.image.title="Phiton"
LABEL org.opencontainers.image.description="Python code compressor using symbolic notation"
LABEL org.opencontainers.image.source="https://github.com/twardoch/phiton"
LABEL org.opencontainers.image.licenses="MIT"