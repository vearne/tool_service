FROM python:3.12

WORKDIR /app

COPY tool_script/requirements.txt /app/
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY tool_script /app/
ENTRYPOINT ["python3"]
CMD ["tool_script/tool_server.py"]