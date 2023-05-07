import discord
import asyncio
import psutil
import GPUtil
import time

client = discord.Client()

# Discord Bot Token
token = ""

# 送信先のチャンネルID
channel_id = 


async def send_system_status():
    await client.wait_until_ready()
    channel = client.get_channel(channel_id)
    while not client.is_closed():
        # CPU使用率を取得
        cpu_percent = psutil.cpu_percent(interval=1)

        # GPU使用率、GPU温度を取得
        gpus = GPUtil.getGPUs()
        if len(gpus) > 0:
            gpu_percent = gpus[0].load * 100
            gpu_temp = gpus[0].temperature
        else:
            gpu_percent = 0
            gpu_temp = 0

        # メモリ使用率を取得
        mem = psutil.virtual_memory()
        mem_percent = mem.percent

        # メモリの利用可能な容量を取得
        mem_avail = mem.available / 1024 / 1024 / 1024

        # HDD使用率を取得
        hdd = psutil.disk_usage("/")
        hdd_usage = round(hdd.used / hdd.total * 100, 1)

        # SSD使用率を取得
        ssd = psutil.disk_usage("C:")
        ssd_usage = round(ssd.used / ssd.total * 100, 1)

        # 起動時間を取得
        uptime = int(time.time() - psutil.boot_time())
        uptime_hours, uptime_minutes = divmod(uptime // 60, 60)
        uptime_message = f"{uptime_hours}時間{uptime_minutes}分"

        # メッセージの送信
        message = f"CPU使用率: {cpu_percent}%\n"
        message += f"GPU使用率: {gpu_percent}%\n"
        message += f"GPU温度: {gpu_temp}℃\n"
        message += f"メモリ使用率: {mem_percent}%\n"
        message += f"利用可能なメモリ容量: {mem_avail:.2f} GB\n"
        message += f"HDD使用率: {hdd_usage}%\n"
        message += f"SSD使用率: {ssd_usage}%\n"
        message += f"起動時間: {uptime_message}\n"
        await channel.send(message)
        await asyncio.sleep(600)  # 10分ごとに実行する


@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    client.loop.create_task(send_system_status())

client.run(token)
