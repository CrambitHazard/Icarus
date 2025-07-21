# TODO

1. LLM Intent Parsing (LLM as Brain)
    - Pass the user query to a fast, powerful LLM (via OpenRouter API).
    - Engineer the prompt to include:
        - Full context of the conversation
        - All available tools and functions (with descriptions)
        - All possible outputs the agent can produce
        - Message history (recent conversation turns)
    - The LLM acts as the "brain": it decides which tool or function to use, or whether to respond directly.
    - The LLM's output is a structured command (tool/function to call, with arguments) or a direct message.
    - All LLM-related features use the OpenRouter API key already present.

2. Plan Mode (Hierarchical Task Planning)
    - If a query is too complex for a single step, send it to a larger LLM (via OpenRouter API) with the same context as above.
    - The LLM generates a step-by-step plan, explicitly marking which steps can be performed in sequence and which can be parallelized.
    - The agent executes these steps by dispatching them to smaller agents (LLM intent parser or tool agents) one by one (or in parallel, as specified).
    - The plan is executed and results are aggregated for the user.
    - All LLM-related features use the OpenRouter API key already present.

3. Websearch via Perplexity App
    - Instead of basic websearch, use the Perplexity app installed on the laptop for advanced search.
    - The agent triggers Perplexity by simulating Ctrl+Shift+P keypresses.
    - The agent types out the query in Perplexity, waits for the response, and uses the result as the answer.
    - Integrate this as a tool callable by the LLM intent parser or plan mode.

4. Add a plan mode using better LLMs, and multiple models for different tasks.
    - Identify and benchmark available LLMs for different task types (e.g., planning, summarization, code generation).
    - Design a system to route tasks to the most appropriate model based on task type and complexity.
    - Implement a configuration or selection mechanism for plan mode (e.g., user can choose or system auto-selects best model).
    - Integrate multiple LLM APIs or endpoints as needed.
    - Test plan mode with real-world scenarios to ensure improved performance and reliability. 