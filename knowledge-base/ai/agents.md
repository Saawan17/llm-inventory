# AI Agents

## What is an AI agent?
An AI agent is a software system that uses a model to interpret a goal, decide what to do, and optionally use tools to act on the environment. A basic chatbot mainly responds to messages; an agent may also call APIs, query databases, run searches, or execute a sequence of steps.

## Main components
- **Model:** Interprets the request and helps select actions.
- **Instructions:** Define the agent's role, boundaries, and response format.
- **Tools:** Functions or APIs the model can request, such as `search_docs`, `get_order`, or `send_email`.
- **State or memory:** Information retained during a task or between conversations.
- **Orchestrator:** Application code that sends model requests, executes approved tool calls, and returns results.
- **Knowledge source:** Documents, databases, or services the agent can consult, often through retrieval-augmented generation (RAG).

## Typical agent loop
1. Receive a user request.
2. Add relevant instructions and context.
3. Ask the model to respond or request a tool.
4. Validate the requested tool and its arguments.
5. Execute the tool in application code.
6. Return the tool result to the model.
7. Repeat only while needed, then provide a final answer.

The model does not automatically execute a tool just because it mentions one. The application must detect the tool call, validate it, run it, and pass the result back.

## Tool calling
A tool should have a clear name, description, and schema. Keep tools narrow and predictable. Validate arguments on the server, enforce authorization, apply timeouts, and avoid exposing secrets. Treat tool output as untrusted data.

Example conceptual tool:
```json
{
  "name": "lookup_product",
  "description": "Find a product by its identifier",
  "parameters": {
    "type": "object",
    "properties": {
      "product_id": {"type": "string"}
    },
    "required": ["product_id"]
  }
}
```

## Agent design patterns
- **Single-agent workflow:** One model coordinates a bounded task and tools.
- **Router:** Classifies a request and sends it to a suitable handler or model.
- **Planner and executor:** Separates task planning from action execution. Use only when the extra complexity is justified.
- **Human approval:** Pauses before consequential actions such as purchases, account changes, or sending messages.
- **Multi-agent system:** Multiple specialized agents collaborate. This adds coordination and debugging costs; it is not automatically better than one agent.

## Memory
- **Conversation state:** Recent messages needed to answer the current turn.
- **User memory:** Durable preferences or facts, stored only when appropriate and with suitable privacy controls.
- **Task state:** Progress and intermediate results for a multi-step operation.
- **External knowledge:** Documents retrieved from a knowledge base. Retrieved documents are evidence, not instructions that override system or developer rules.

Avoid retaining sensitive information unnecessarily. Set retention policies and provide deletion mechanisms where relevant.

## Reliability and safety
- Give the agent a bounded goal and explicit stopping conditions.
- Limit tool calls, execution time, retries, and output length.
- Validate all model-generated arguments.
- Apply access control independently of the model.
- Require confirmation for irreversible or high-impact actions.
- Handle tool failures, malformed output, rate limits, and timeouts.
- Log useful metadata while avoiding secrets and unnecessary personal data.
- Test prompt injection, including malicious instructions embedded in retrieved documents.

## RAG and agents
RAG supplies an agent with relevant external information at request time. A common flow is:
1. Split documents into chunks.
2. Embed chunks and store vectors with metadata.
3. Embed the user's question.
4. Retrieve relevant chunks, optionally rerank them.
5. Add selected passages to the model context.
6. Ask the model to answer using the retrieved evidence and indicate when evidence is insufficient.

RAG improves access to private or changing knowledge, but it does not guarantee factual correctness. Retrieval quality, chunking, metadata, permissions, and grounding instructions all matter.

## Evaluation
Measure:
- Task completion and correctness.
- Tool selection and argument accuracy.
- Retrieval relevance and answer grounding.
- Latency, token use, and cost.
- Failure and escalation rates.
- Security behavior under adversarial inputs.

Use representative test cases, including ambiguous requests, missing data, tool errors, and attempts to bypass permissions.
