# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity
# from google import genai
# from dotenv import load_dotenv
# import os

# # Example knowledge-base chunks
# chunks = [
#     {
#         "content": "Python uses indentation to define blocks of code.",
#         "source": "python.md"
#     },
#     {
#         "content": "Java is a class-based, object-oriented programming language.",
#         "source": "java.md"
#     },
#     {
#         "content": "Spring Boot simplifies the development of Java applications.",
#         "source": "spring-boot.md"
#     },
#     {
#         "content": "React is a JavaScript library used to build interactive user interfaces.",
#         "source": "react.md"
#     },
#     {
#         "content": "PostgreSQL is an open-source relational database management system.",
#         "source": "postgresql.md"
#     },
#     {
#         "content": "REST APIs allow applications to communicate using HTTP methods such as GET, POST, PUT, and DELETE.",
#         "source": "rest-api.md"
#     },
#     {
#         "content": "JWT (JSON Web Token) is commonly used to securely transmit information between parties and implement authentication.",
#         "source": "jwt.md"
#     },
#     {
#         "content": "Docker packages applications and their dependencies into containers, making them easier to deploy consistently.",
#         "source": "docker.md"
#     },
#     {
#         "content": "Apache Kafka is a distributed event-streaming platform used to publish, store, and consume streams of events.",
#         "source": "kafka.md"
#     },
#     {
#         "content": "Redis is an in-memory data store commonly used for caching, session management, and fast data access.",
#         "source": "redis.md"
#     },
#     {
#         "content": "Machine learning enables computers to learn patterns from data and use those patterns to make predictions.",
#         "source": "machine-learning.md"
#     },
#     {
#         "content": "Retrieval-Augmented Generation (RAG) combines information retrieval with language models to generate answers grounded in relevant documents.",
#         "source": "rag.md"
#     },
#     {
#         "content": "Embeddings represent text as numerical vectors that can be compared to identify semantically similar content.",
#         "source": "embeddings.md"
#     },
#     {
#         "content": "A vector database stores and searches vector embeddings, making it useful for semantic search and retrieval systems.",
#         "source": "vector-database.md"
#     },
#     {
#         "content": "Python's NumPy library provides efficient multidimensional arrays and mathematical operations for numerical computing.",
#         "source": "numpy.md"
#     }
# ]

# #Load the embedding model
# model = SentenceTransformer("all-MiniLM-L6-v2")






# # Generate embeddings for document chunks
# chunk_texts = [chunk["content"] for chunk in chunks]
# chunk_text_embeddings = model.encode(chunk_texts)

# def retrieve_chunks(question, chunks, chunk_embeddings, model, top_k=3):

#     # 1. Convert the question into an embedding
#     question_embedding = model.encode([question])

#     # 2. Calculate cosine similarity
#     similarities = cosine_similarity(
#         question_embedding,
#         chunk_embeddings
#     )[0]

#     # 3. Determine how many chunks we can retrieve
#     top_k = min(top_k, len(chunks))

#     # 4. Get indices of the highest similarity scores
#     top_indices = similarities.argsort()[::-1][:top_k]

#     # 5. Collect the matching chunks
#     retrieved_chunks = []

#     for index in top_indices:

#         index = int(index)

#         retrieved_chunks.append({
#             "content": chunks[index]["content"],
#             "source": chunks[index]["source"],
#             "similarity": float(similarities[index])
#         })

#     return retrieved_chunks


# # Ask a question
# question = input("Enter your question: ")

# # Generate embedding for the question
# question_embedding = model.encode([question])


# # Compare question embedding with chunk embeddings
# similarities = cosine_similarity(question_embedding, chunk_text_embeddings)

# # --------------------------------------------------
# # Retrieve the top 3 most relevant chunks
# # --------------------------------------------------

# # top_k = 3

# # # Get the indices of chunks sorted by similarity
# # top_indices = similarities.argsort()[::-1][:top_k]

# # # Retrieve the corresponding chunks
# # retrieved_chunks = []

# # for index in top_indices:
# #     index = int(index)  # Convert NumPy integer to Python int
# #     retrieved_chunks.append({
# #         "content": chunks[index]["content"],
# #         "source": chunks[index]["source"],
# #         "similarity_score": similarities[index]
# #     })

# # # # Find the most relevant chunk
# # # best_match_index = similarities.argmax()

# # # best_match = chunks[best_match_index]

# # # Display retrieved chunks
# # for chunk in retrieved_chunks:
# #     print("\nSource:", chunk["source"])
# #     print("Similarity:", chunk["similarity"])
# #     print("Content:", chunk["content"])

# # Make sure similarities is a 1D array
# similarities = similarities.flatten()

# # Retrieve the top 3 most relevant chunks
# top_k = min(3, len(chunks))

# top_indices = similarities.argsort()[::-1][:top_k]

# retrieved_chunks = []

# for index in top_indices:
#     index = index.item()  # Convert NumPy scalar to Python integer

#     retrieved_chunks.append({
#         "content": chunks[index]["content"],
#         "source": chunks[index]["source"],
#         "similarity": float(similarities[index])
#     })


# # Display retrieved chunks
# for chunk in retrieved_chunks:
#     print("\nSource:", chunk["source"])
#     print("Similarity:", chunk["similarity"])
#     print("Content:", chunk["content"])


# # --------------------------------------------------
# # Send retrieved context to Gemini
# # --------------------------------------------------
# load_dotenv()

# api_key = os.getenv("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError("GEMINI_API_KEY not found in .env file")

# client = genai.Client(
#     api_key=api_key
# )


# retrieved_context = "\n\n".join(
#     chunk["content"] for chunk in retrieved_chunks
# )

# prompt = f"""
# Answer the user's question using the following retrieved context.

# If the context does not contain enough information to answer,
# say that the knowledge base does not contain enough information.

# Retrieved context:
# {retrieved_context}

# User question:
# {question}
# """

# response = client.models.generate_content(
#     model="gemini-3.5-flash-lite",
#     contents=prompt
# )

# print("\nAI Answer:")
# print(response.text)


import glob
import os

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from langchain_text_splitters import RecursiveCharacterTextSplitter


# --------------------------------------------------
# 1. Load all Markdown documents
# --------------------------------------------------

def load_documents():
    documents = []

    # Find all Markdown files inside knowledge-base
    file_paths = glob.glob(
        "knowledge-base/**/*.md",
        recursive=True
    )

    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

        # Ignore empty files
        if content.strip():
            documents.append({
                "content": content,
                "source": file_path
            })

    return documents


# --------------------------------------------------
# 2. Split documents into chunks
# --------------------------------------------------

def create_chunks(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = []

    for document in documents:
        document_chunks = text_splitter.split_text(
            document["content"]
        )

        for chunk_text in document_chunks:
            chunks.append({
                "content": chunk_text,
                "source": document["source"]
            })

    return chunks


# --------------------------------------------------
# 3. Generate embeddings for chunks
# --------------------------------------------------

def create_embeddings(chunks, embedding_model):
    if not chunks:
        return np.empty((0, 384))

    chunk_texts = [
        chunk["content"]
        for chunk in chunks
    ]

    embeddings = embedding_model.encode(chunk_texts)

    return np.asarray(embeddings)


# --------------------------------------------------
# 4. Retrieve the most relevant chunks
# --------------------------------------------------

def retrieve_chunks(
    question,
    chunks,
    chunk_embeddings,
    embedding_model,
    top_k=3
):
    # Handle an empty knowledge base
    if not chunks or len(chunk_embeddings) == 0:
        return []

    # Convert the user's question into an embedding
    question_embedding = embedding_model.encode([question])

    # Calculate cosine similarity between the question
    # and every chunk embedding
    similarities = cosine_similarity(
        question_embedding,
        chunk_embeddings
    ).ravel()

    # Select the indexes of the highest similarity scores
    top_k = min(top_k, len(chunks))

    top_indices = similarities.argsort()[::-1][:top_k]

    retrieved_chunks = []

    for index in top_indices:
        index = int(index)

        retrieved_chunks.append({
            "content": chunks[index]["content"],
            "source": chunks[index]["source"],
            "similarity": float(similarities[index])
        })

    return retrieved_chunks


# --------------------------------------------------
# 5. Run a simple retrieval test
# --------------------------------------------------

def main():
    print("Loading embedding model...")

    embedding_model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )

    print("Loading documents...")

    documents = load_documents()

    if not documents:
        print(
            "No Markdown documents found in knowledge-base."
        )
        return

    print(f"Loaded {len(documents)} documents.")

    print("Creating chunks...")

    chunks = create_chunks(documents)

    print(f"Created {len(chunks)} chunks.")

    print("Generating embeddings...")

    chunk_embeddings = create_embeddings(
        chunks,
        embedding_model
    )

    print(
        "Embedding shape:",
        chunk_embeddings.shape
    )

    # Ask a question
    question = input("\nEnter your question: ").strip()

    if not question:
        print("Please enter a question.")
        return

    retrieved_chunks = retrieve_chunks(
        question=question,
        chunks=chunks,
        chunk_embeddings=chunk_embeddings,
        embedding_model=embedding_model,
        top_k=3
    )

    print("\n--- Retrieved Chunks ---")

    for chunk in retrieved_chunks:
        print("\nSource:", chunk["source"])
        print("Similarity:", round(chunk["similarity"], 4))
        print("Content:", chunk["content"])


if __name__ == "__main__":
    main()