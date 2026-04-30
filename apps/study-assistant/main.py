from service import ask

while True:
    q = input("\nAsk (type 'exit'): ")

    if q.lower() == "exit":
        break

    print(ask(q))