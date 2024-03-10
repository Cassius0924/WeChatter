FROM node:18-alpine3.18 as build
LABEL authors="jerryestt"

WORKDIR /configweb

ADD . /configweb

RUN ls -la /configweb

RUN npm install

# 使 loguru 支持颜色输出
ENV LOGURU_COLORIZE=True
# 设置日志级别
ENV WECHATTER_LOG_LEVEL=INFO

EXPOSE 3000 8000

CMD ["npm", "start"]
