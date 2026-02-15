FROM python:3.9-slim

# Install system tools for networking
RUN apt-get update && apt-get install -y \
    net-tools \
    iputils-ping \
    tcpdump \
    && rm -rf /var/lib/apt/lists/*

# Install Python libraries
RUN pip install scapy colorama

WORKDIR /app
CMD ["/bin/bash"]