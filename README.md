# Generative AI app: PDF ChatBot with AWS Bedrock 

In this project, we will develop an advanced AI-powered chatbot designed to facilitate seamless interaction with PDF documents. Users will have the capability to upload files of up to 200MB and pose questions to the chatbot, enabling them to explore and extract valuable insights from the content of the documents.

This innovative application will enhance user experience by providing a conversational interface that simplifies the process of retrieving information from complex PDF files. By leveraging cutting-edge natural language processing techniques, the chatbot will understand and respond to user inquiries intelligently, making it a powerful tool for both educational and professional settings.

The development of this application will utilize a range of sophisticated tools and technologies, ensuring robust performance and an intuitive user experience. The tools used to build this application include:

- Amazon bedrock
- AWS S3
- AWS EC2
- Docker
- Langchain
- Streamlit

## Architecture

![Architecture](https://github.com/Ndzenyuy/chatPdf/blob/main/images/architecture.jpg)

## Principle

In this application, users can upload a PDF file through the user interface (UI). The PDF is then processed using PyPDF, which divides the content into manageable chunks. These chunks are transformed into vectors, providing a machine-learning-friendly representation of the PDF's content. The resulting vectors are subsequently stored in an Amazon S3 bucket for efficient access and retrieval.
When a user Queries the PDF, the application processes the vector from the S3 for similarities and generates a prompt with the query and context, these are then used as input for Jurassic-2 Mid llm model which will generate an answer and respond to the user.

The application operates within a Docker container, utilizing Streamlit to create a visually appealing and user-friendly interface. This combination of technologies ensures a smooth and interactive experience for users as they engage with the content of their uploaded PDFs. 

## How to build It

### Launch an EC2 instance

Longin to AWS console and Launch a  t2.micro instance with the following configuration
```
    Name: pdf-Chat-Bot
    Instance type: t2.micro
    AMI: Ubuntu:latest
    Volume: 8GiB
    Security gate: Create new
        - inbound rules 
            => allow 8083 from everywhere
            => allow ssh from my IP  
    launch template:       
```

```bash
    #!bin/bash
    # Add Docker's official GPG key:
    sudo apt-get update
    sudo apt-get install ca-certificates curl
    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    # Add the repository to Apt sources:
    echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
    $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
    sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
    sudo apt-get update
    sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

```

### Create an IAM Role for the EC2 instance to access Bedrock and S3

Go to AWS console -> IAM -> Roles -> Create role
```
name: pdfBotRole
attach policies: 
    - AmazonBedrockFullAccess
    - AmazonS3FullAccess
```

### Attach role to EC2 instance

Go to the EC2 console, select the instance then select Actions -> Security -> Modify IAM role
Select the IAM role previously created "pdfBotRole" and click Apply

### Create S3 bucket

On the console, search S3 then create a bucket with the following(xxx are random numbers to make the bucket name unique)

```
    name: bedrock-chatpdf-xxx
    region: us-east-one
    allow defaults and choose create
```

Copy the bucket name as well use it in the next steps

### SSH into the instance and clone Source code

Copy the public address of the instance and open a terminal
```bash
ssh -i "path/to/.pem-file" ubuntu@public-ip-address
```
Verify docker installation

```bash
docker ps
```

If docker is installed, will see a table for existing docker containers which will of course be empty

### Clone source

Open a terminal and run the following
```bash
    git clone https://github.com/Ndzenyuy/chatPdf.git
    cd chatPdf
```

### Access for LLM models in Amazon Bedrock

On the console Amazon Bedrock -> Base models -> Model Access
Make sure you have access to ```Jurassic-2 Ultra``` and ```Titan Embeddings G1 - Text```, if not you can access by requesting access.

### Build and Run App docker image

Make sure you are inside chatPdf folder and run the following command

```bash
    docker build -t chatPdf-app .
```

The image will be built, then we can run it with the following

```bash
    docker run -d -e BUCKET_NAME="yourBucketName" -p 8083:8083 chatPdf
```

Now copy the public IP of the EC2 instance and type it on the browser followed by the port number 8083. For instance

```
XX.XX.XX.XX:8083
```
## How to use the App

The landing page will first require the user to upload a pdf document
![Landing Page](https://github.com/Ndzenyuy/chatPdf/blob/main/images/landingPage.png)

Either drag and drop or Click on the button "Browse files" Load the PDF document and ask questions based on its content

![Ask questions](https://github.com/Ndzenyuy/chatPdf/blob/main/images/queryPdf.png)

## Conclusion

In this project, we have successfully developed an innovative PDF chatbot application designed to significantly reduce the time spent on research and reading. By transforming hours of traditional document review into just a few minutes of interactive engagement, users can efficiently understand the content, authorship, summaries, and key findings of PDF documents.

This application serves as a valuable tool for students, enhancing their ability to engage with academic articles and literature. By streamlining the process of extracting relevant information from complex texts, the chatbot not only saves time but also fosters critical thinking and enhances research skills. This project represents a significant advancement in educational technology, paving the way for improved student capabilities in navigating and relating to scholarly articles.
