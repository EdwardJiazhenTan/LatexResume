# Use official Python image as base
FROM python:3.11-slim

# Install LaTeX and required packages
RUN apt-get update && apt-get install -y \
    texlive-latex-base \
    texlive-latex-extra \
    texlive-fonts-recommended \
    texlive-fonts-extra \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python dependencies
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY generate_resume.py .
COPY watch_resume.py .

# Create necessary directories
RUN mkdir -p /app/src /app/build /app/resume/backups

# Default command - generate resume
CMD ["python", "generate_resume.py"]
