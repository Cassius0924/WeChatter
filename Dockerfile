FROM python:3.9-alpine3.18
LABEL authors="Cassius0924"

WORKDIR /wechatter

ADD . /wechatter

RUN pip install --no-cache-dir -r requirements.txt

# 使 loguru 支持颜色输出
ENV LOGURU_COLORIZE=True
# 设置日志级别
ENV WECHATTER_LOG_LEVEL=INFO

EXPOSE 4000

CMD ["python3", "-m", "wechatter"]