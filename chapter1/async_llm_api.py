import asyncio
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

# 1. 비동기 클라이언트 생성
openai_client1 = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
openai_client2 = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

async def call_async_openai1(prompt: str, model: str = "gpt-5-nano") -> str:
    # 2. await를 사용해 비동기적으로 API 응답을 기다림
    response = await openai_client1.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content

async def call_async_openai2(prompt: str, model: str = "gpt-5-nano") -> str:
    # 3. await를 사용해 비동기적으로 API 응답을 기다림
    response = await openai_client1.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content

async def main():
    print("동시에 API 호출하기")
    prompt1 = "비동기 프로그래밍에 대해 두세 문장으로 설명해주세요."
    prompt2 = "지구와 달의 거리를 알려주세요."

    # 4. 비동기 함수 호출 시 코루틴 객체 반환(실행은 아직 안 됨)
    openai_task1 = call_async_openai1(prompt1)
    openai_task2 = call_async_openai1(prompt2)

    # 5. 두 API 호출을 병렬로 실행하고 둘 다 완료될 때까지 대기
    openai_response1, openai_response2 = await asyncio.gather(openai_task1, openai_task2)
    print(f"OpenAI 응답1: {openai_response1}")
    print(f"OpenAI 응답2: {openai_response2}")

if __name__ == "__main__":
    asyncio.run(main())         # 6. 비동기 메인 함수를 이벤트 루프에서 실행