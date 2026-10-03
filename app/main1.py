# # import os

# # from dotenv import load_dotenv
# # from google import genai
# # import json

# # load_dotenv()


# # knowledge_base = ""

# # with open("knowledge-base/python.md", "r", encoding="utf-8") as f:
# #     knowledge_base = f.read()

# # print(knowledge_base)

# # with open("app/memory.json", "r") as f:
# #     messages = json.load(f)

# # client = genai.Client(
# #     api_key=os.getenv("GEMINI_API_KEY")
# # )

# # chat = client.chats.create(
# #     model="gemini-3.6-flash",
# #      config={
# #         "system_instruction": """
# #         You are a helpful AI engineering tutor.

# #         Explain concepts in simple language.
# #         Use small examples when useful.
# #         If the user asks for a short answer, keep it short.
# #         """
# #     }
# # )



# # # 3. Restore previous conversation into the new chat
# # for message in messages:
# #     chat.send_message(message["content"])

# # print("Welcome to the AI Assistant! Type 'exit' to quit.")



# # while True:
# #     user_input = input("You: ")

# #     if user_input.lower() == "exit":
# #         break

# #     # messages.append({"role": "user", "content": user_input})

# #     response = chat.send_message(
# #         user_input
# #     )


# #     assistant_message = response.text

# #     print("AI:", assistant_message)

# #     messages.append({
# #         "role": "user",
# #         "content": user_input
# #     })

# #     messages.append({
# #         "role": "model",
# #         "content": assistant_message
# #     })

# #     with open("app/memory.json", "w") as f:
# #         json.dump(messages, f, indent=4)

# #     # messages.append({"role": "assistant", "content": assistant_message})



# import os
# import json
# import glob
# from dotenv import load_dotenv
# from google import genai
# from google.genai import types

# from langchain_text_splitters import RecursiveCharacterTextSplitter


# # --------------------------------------------------
# # 1. Load environment variables
# # --------------------------------------------------

# load_dotenv()

# api_key = os.getenv("GEMINI_API_KEY")

# if not api_key:
#     raise ValueError("GEMINI_API_KEY not found in .env file")

# # --------------------------------------------------
# # 2. Load all Markdown documents
# # --------------------------------------------------

# documents = []

# file_paths = glob.glob(
#     "knowledge-base/**/*.md",
#     recursive=True
# )

# for file_path in file_paths:

#     with open(file_path, "r", encoding="utf-8") as f:
#         content = f.read()

#     # knowledge_base += f"\n\n--- DOCUMENT: {file_path} ---\n\n"
#     # knowledge_base += content
#     documents.append({
#         "content": content,
#         "source": file_path
#     })


# # print(f"Loaded {len(file_paths)} Markdown documents.")

# # --------------------------------------------------
# # 3. Split documents into chunks and preserve metadata
# # --------------------------------------------------


# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=500,
#     chunk_overlap=100,
# )

# chunks = []

# for document in documents:

#     document_chunks = text_splitter.split_text(
#         document["content"]
#     )

#     for chunk_text in document_chunks:

#         chunks.append({
#             "content": chunk_text,
#             "source": document["source"]
#         })


# print(f"Created {len(chunks)} chunks.")


# for index, chunk in enumerate(chunks):

#     print(f"\n--- Chunk {index + 1} ---")
#     print("Source:", chunk["source"])
#     print("Content:", chunk["content"])
# # --------------------------------------------------
# # 3. Load previous conversation from memory.json
# # --------------------------------------------------

# with open("app/memory.json", "r", encoding="utf-8") as f:
#     messages = json.load(f)


# # --------------------------------------------------
# # 4. Convert saved messages into Gemini chat history
# # --------------------------------------------------
# recent_messages = messages[-10:]

# history = []


# for message in recent_messages:
#     history.append(
#         types.Content(
#             role=message["role"],
#             parts=[
#                 types.Part.from_text(
#                     text=message["content"]
#                 )
#             ]
#         )
#     )


# # --------------------------------------------------
# # 5. Create Gemini client
# # --------------------------------------------------

# client = genai.Client(
#     api_key=api_key
# )


# # --------------------------------------------------
# # 6. Create chat with previous history
# # --------------------------------------------------

# chat = client.chats.create(
#     model="gemini-3.5-flash-lite",
#     history=history,
#     config={
#         "system_instruction": f"""
#         You are a helpful AI engineering tutor.

#         Explain concepts in simple language.
#         Use small examples when useful.
#         Keep answers concise unless the user asks for details.

#         KNOWLEDGE BASE:
#         # {document_chunks}

#         Instructions:
#         - Use the knowledge base when relevant.
#         - Reproduce examples accurately when requested.
#         - If information is missing from the knowledge base,
#           say so clearly.
#         """
#     }
# )


# # --------------------------------------------------
# # 7. Start chatbot
# # --------------------------------------------------

# print("\nWelcome to the AI Assistant!")
# print("Type 'exit' to quit.\n")


# while True:

#     user_input = input("You: ")

#     if user_input.lower() == "exit":
#         print("Goodbye!")
#         break


#     # --------------------------------------------------
#     # 8. Send new message to Gemini
#     # --------------------------------------------------

#     response = chat.send_message(
#         user_input
#     )

#     assistant_message = response.text

#     print("AI:", assistant_message)


#     # --------------------------------------------------
#     # 9. Save conversation to memory.json
#     # --------------------------------------------------

#     messages.append({
#         "role": "user",
#         "content": user_input
#     })

#     messages.append({
#         "role": "model",
#         "content": assistant_message
#     })


#     # --------------------------------------------------
#     # 10. Write updated memory to file
#     # --------------------------------------------------

#     with open("app/memory.json", "w", encoding="utf-8") as f:
#         json.dump(
#             messages,
#             f,
#             indent=4,
#             ensure_ascii=False
#         )


import os

from dotenv import load_dotenv
from google import genai

from semantic_search import (
    load_documents,
    create_chunks,
    create_embeddings,
    retrieve_chunks
)

from sentence_transformers import SentenceTransformer


# --------------------------------------------------
# 1. Load environment variables
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")


# --------------------------------------------------
# 2. Initialize Gemini
# --------------------------------------------------

client = genai.Client(api_key=api_key)

GEMINI_MODEL = "gemini-3.1-pro-preview"


# --------------------------------------------------
# 3. Initialize the embedding model
# --------------------------------------------------

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# --------------------------------------------------
# 4. Load documents and create embeddings
# --------------------------------------------------

print("Loading knowledge-base documents...")

documents = load_documents()

if not documents:
    raise ValueError(
        "No Markdown documents found in knowledge-base."
    )

chunks = create_chunks(documents)

chunk_embeddings = create_embeddings(
    chunks,
    embedding_model
)

print(f"Loaded {len(documents)} documents.")
print(f"Created {len(chunks)} chunks.")


# --------------------------------------------------
# 5. Chat loop
# --------------------------------------------------

print("\nPersonal AI Knowledge Assistant is ready!")
print("Type 'exit' to quit.\n")


while True:

    question = input("You: ").strip()

    if question.lower() == "exit":
        print("Goodbye!")
        break

    if not question:
        print("Please enter a question.")
        continue


    # --------------------------------------------------
    # 6. Retrieve relevant chunks
    # --------------------------------------------------

    retrieved_chunks = retrieve_chunks(
        question=question,
        chunks=chunks,
        chunk_embeddings=chunk_embeddings,
        embedding_model=embedding_model,
        top_k=3
    )


    # --------------------------------------------------
    # 7. Prepare context for Gemini
    # --------------------------------------------------

    if retrieved_chunks:

        context = "\n\n".join(
            [
                f"Source: {chunk['source']}\n"
                f"Content: {chunk['content']}"
                for chunk in retrieved_chunks
            ]
        )

    else:
        context = "No relevant information was found."


    # --------------------------------------------------
    # 8. Create the prompt
    # --------------------------------------------------

    prompt = f"""
You are a helpful Personal AI Knowledge Assistant.

Answer the user's question using the provided knowledge-base context.

Instructions:
- Use the context as your primary source of information.
- If the context does not contain enough information, clearly say so.
- Do not invent facts and pretend they came from the knowledge base.
- Explain concepts clearly and simply.
- You may use general knowledge to clarify an explanation, but distinguish it
  from information found in the provided context.

Knowledge-base context:

{context}

User's question:

{question}
"""


    # --------------------------------------------------
    # 9. Send the prompt to Gemini
    # --------------------------------------------------

    try:

        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        answer = response.text

        print("\nAI:", answer, "\n")

    except Exception as error:

        print("\nAn error occurred:", error, "\n")