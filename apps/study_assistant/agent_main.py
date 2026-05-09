from agent_service import run_agent

while True:
    q = input("\nAsk: ")

    if q == "exit":
        break

    result = run_agent(q)
    print("\nFINAL ANSWER:\n", result)