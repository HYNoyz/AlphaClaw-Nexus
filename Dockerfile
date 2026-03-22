# 采用官方 Python 3.12 轻量级镜像，体积小，极客首选
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 环境变量：防止 Python 缓冲 stdout 和 stderr，确保大屏日志实时输出，不丢帧
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 将当前目录下的所有文件复制到容器的 /app 目录下
COPY . /app/

# 如果你的 TG Bot 用到了第三方库（比如 pyTelegramBotAPI 或 web3.py）
# 取消下面这行的注释来安装依赖。如果真的是 100% 纯原生 0 依赖，就保持注释
# RUN pip install --no-cache-dir -r requirements.txt

# 暴露 AlphaClaw 中枢与前端大屏通信的端口
EXPOSE 5000

# 物理引擎点火命令
CMD ["python", "final.py"]
