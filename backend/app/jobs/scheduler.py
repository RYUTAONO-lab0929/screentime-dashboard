from __future__ import annotations
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import asyncio


async def daily_aggregation() -> None:
    # TODO: usage_daily を再計算するETL（サンプルのためログのみ）
    print("[worker] running daily aggregation...")


async def main() -> None:
    scheduler = AsyncIOScheduler()
    scheduler.add_job(daily_aggregation, CronTrigger(hour=2, minute=0))
    scheduler.start()
    print("[worker] scheduler started")
    while True:
        await asyncio.sleep(3600)


if __name__ == "__main__":
    asyncio.run(main())
