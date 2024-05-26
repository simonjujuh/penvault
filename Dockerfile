# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /penvault

# Copy the rest of your application code into the container
COPY . .

# Install necessary packages and VeraCrypt
RUN apt-get update && \
    apt-get install dirmngr software-properties-common apt-transport-https curl lsb-release ca-certificates -y && \
    curl -fsSL https://notesalexp.org/debian/alexp_key.asc | gpg --dearmor | tee /usr/share/keyrings/alexp_key.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/alexp_key.gpg] https://notesalexp.org/debian/$(lsb_release -sc)/ $(lsb_release -sc) main" | tee /etc/apt/sources.list.d/alexp.list
    apt-get update && \
    apt-get install veracrypt --yes

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt
# Install penvault
RUN pip install .

# Install configuration
RUN mkdir -p ~/.penvault
RUN mkdir -p /opt/penvault/containers
RUN mkdir -p /opt/penvault/mount
RUN cp /penvault/penvault/data/config.ini ~/.penvault
RUN sed -i 's,/path/to/containers/folder,/opt/penvault/containers,' ~/.penvault/config.ini
RUN sed -i 's,/path/to/containers/mountpoint,/opt/penvault/mount,' ~/.penvault/config.ini

# Command to run your script
# CMD ["python", "your_script.py"]

