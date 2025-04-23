import asyncio
from utils.retrieve import generate_answer

def main():
    query = "What is the effective date of the agreement?"
    response = asyncio.run(generate_answer(query))
    print(response)

if __name__ == "__main__":
    main()
