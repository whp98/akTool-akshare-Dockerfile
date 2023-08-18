# 基础镜像
FROM python:3.8-slim-buster
# 安装 Nginx
RUN apt-get update && apt-get install -y nginx
# 删除默认配置
RUN rm -rf /etc/nginx/conf.d
# 拷贝nginx配置
COPY ./config/nginx.conf /etc/nginx/nginx.conf
COPY ./config/conf.d /etc/nginx/conf.d
# 设置工作目录
WORKDIR /app
# 拷贝代码
COPY ./src /app/src
COPY ./requirements.txt /app/requirements.txt
# 安装依赖
RUN pip install  Flask
RUN pip install  waitress
RUN pip install aktools --upgrade
# 暴露端口
EXPOSE 38080
# 启动 Nginx 和 Python 应用
CMD service nginx start && python ./src/main.py
