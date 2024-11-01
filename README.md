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

![Architecture]()

## Principle

In this application, users can upload a PDF file through the user interface (UI). The PDF is then processed using PyPDF, which divides the content into manageable chunks. These chunks are transformed into vectors, providing a machine-learning-friendly representation of the PDF's content. The resulting vectors are subsequently stored in an Amazon S3 bucket for efficient access and retrieval.

The application operates within a Docker container, utilizing Streamlit to create a visually appealing and user-friendly interface. This combination of technologies ensures a smooth and interactive experience for users as they engage with the content of their uploaded PDFs. 

