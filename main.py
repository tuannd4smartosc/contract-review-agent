import asyncio
from utils.retrieve import generate_answer

def main():
    query = "What are the confidentiality terms?"
    response = asyncio.run(generate_answer(query))
    print(">>>>> RESPOONSE: \n\n", response)

if __name__ == "__main__":
    main()
