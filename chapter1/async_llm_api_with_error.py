import asyncio
import os
import logging
import random
from dotenv import load_dotenv
from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# 1. 비동기 클라이언트 생성
openai_client1 = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
openai_client2 = AsyncOpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

async def simulate_random_failure():
    # 50% 확률로 실패 발생시키기
    if random.random() < 0.5:
        logger.warning("인위적으로 API 호출 실패 발생 (테스트용)")
        raise ConnectionError("인위적으로 발생시킨 연결 오류 (테스트용)")
    
    # 약간의 지연시간 추가 (0.1~0.5초 사이)
    await asyncio.sleep(random.uniform(0.1, 0.5))

# tenacity를 사용한 재시도 데코레이터 적용
@retry(
    stop=stop_after_attempt(3),     # 최대 3번 시도
    wait=wait_exponential(multiplier=1, min=2, max=10), # 지수 백오프: 2, 4, 8초...
    retry=retry_if_exception_type(),    # 모든 예외에 대해 재시도
    before_sleep=lambda retry_state: logger.warning(
        f"API 호출 실패: {retry_state.outcome.exception()}, {retry_state.attempt_number}번째 재시도 중..."
    )
)

async def call_async_openai1(prompt: str, model: str = "gpt-5-nano") -> str:
    # 2. await를 사용해 비동기적으로 API 응답을 기다림
    # 랜덤한 확률로 실패하는 call_async_openai 함수
    logger.info(f"OpenAI API 호출1 시작: {model}")

    # 테스트를 위한 랜덤 실패 시뮬레이션
    await simulate_random_failure()

    response = await openai_client1.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    return response.choices[0].message.content

async def call_async_openai2(prompt: str, model: str = "gpt-5-nano") -> str:
    # 3. await를 사용해 비동기적으로 API 응답을 기다림
    # 랜덤한 확률로 실패하는 call_async_openai 함수
    logger.info(f"OpenAI API 호출2 시작: {model}")

    # 테스트를 위한 랜덤 실패 시뮬레이션
    await simulate_random_failure()

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
    # gather는 전체 작업 중 하나라도 실패하면 예외 발생
    openai_response1, openai_response2 = await asyncio.gather(
        openai_task1, openai_task2, return_exceptions=False)
    print(f"OpenAI 응답1: {openai_response1}")
    print(f"OpenAI 응답2: {openai_response2}")

if __name__ == "__main__":
    asyncio.run(main())         # 6. 비동기 메인 함수를 이벤트 루프에서 실행