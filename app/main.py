import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from sentence_transformers import SentenceTransformer

from semantic_search import (
    load_documents,
    create_chunks,
    create_embeddings,
    retrieve_chunks
)

from tools import (
    calculator,
    get_current_datetime,
    add_task,
    get_tasks,
    complete_task,
    get_location_coordinates,
    get_weather,
    get_location_coordinates_with_logging,
    get_weather_with_logging,
    convert_temperature
)


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

MODEL_NAME = "gemini-3.5-flash-lite"


# --------------------------------------------------
# 3. Load the embedding model
# --------------------------------------------------

print("Loading embedding model...")

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# --------------------------------------------------
# 4. Load knowledge-base documents
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
# 5. Create Gemini chat with tools
# --------------------------------------------------

chat = client.chats.create(
    model=MODEL_NAME,
    config=types.GenerateContentConfig(
        system_instruction="""
            You are a helpful Personal AI Knowledge Assistant.

            You have access to:

            - The user's knowledge base
            - Calculator
            - Date/time
            - Task manager
            - Location search
            - Weather

            Tool rules:

            1. Use tools when they are appropriate.
            2. Never invent a tool result.
            3. Never claim that a tool succeeded when it failed.
            4. Check the success field returned by tools.
            5. If success is false, explain the error to the user.
            6. Do not expose Python exceptions, stack traces, URLs, or internal
            implementation details unless necessary.

           Weather workflow:

            1. Determine the city and country requested by the user.
            2. Call get_location_coordinates with both city and country when the country
            is known or can be reliably determined.
            3. Check whether the location tool succeeded.
            4. If it succeeded, use its latitude and longitude with get_weather.
            5. Never assume that the first geocoding result is correct.
            6. If the location is ambiguous, ask the user to clarify the country.
            7. Never invent weather information.

            Keep responses simple and conversational.

            Temperature conversion rules:

            1. If the user requests a temperature in a different unit,
            ALWAYS call convert_temperature.
            2. Do not calculate the conversion yourself.
            3. If get_weather returns Celsius and the user requested Fahrenheit,
            call convert_temperature with:
                temperature = weather temperature
                from_unit = "C"
                to_unit = "F"
            4. Return the converted value from the tool.
            """,
            tools=[
        calculator,
        get_current_datetime,
        add_task,
        get_tasks,
        complete_task,
        get_location_coordinates_with_logging,
        get_weather_with_logging,
        convert_temperature
    ],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=False
        )
    )
)


# --------------------------------------------------
# 6. Start conversation
# --------------------------------------------------

print("\nPersonal AI Knowledge Assistant is ready!")
print("You can ask knowledge-base questions or use tools.")
print("Type 'exit' to quit.\n")


while True:

    question = input("You: ").strip()

    if question.lower() == "exit":
        print("Goodbye!")
        break

    if not question:
        continue


    # --------------------------------------------------
    # 7. Retrieve relevant knowledge-base chunks
    # --------------------------------------------------

    retrieved_chunks = retrieve_chunks(
        question=question,
        chunks=chunks,
        chunk_embeddings=chunk_embeddings,
        embedding_model=embedding_model,
        top_k=3
    )


    # --------------------------------------------------
    # 8. Prepare the retrieved context
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

        context = "No relevant information was retrieved."


    # --------------------------------------------------
    # 9. Build the prompt
    # --------------------------------------------------

    prompt = f"""
        Knowledge-base context:

        {context}


        User's question:

        {question}
        """


    # --------------------------------------------------
    # 10. Send message to Gemini
    # --------------------------------------------------

    try:

        response = chat.send_message(prompt)

        if response.text:
            print("\nAI:", response.text, "\n")

        else:
            print(
                "\nAI: No text response was returned.\n"
            )

    except Exception as error:

        print("\nAn error occurred:", error, "\n")