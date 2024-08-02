FROM openjdk:11-jdk

WORKDIR /app

# Copy the Maven project files (pom.xml and src folder) to the container
COPY pom.xml .
COPY src ./src

RUN apt-get update && apt-get install -y maven
RUN mvn clean package
CMD ["sleep", "infinity"]
