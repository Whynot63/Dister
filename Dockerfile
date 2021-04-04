FROM python:3.9.1-slim
RUN  python -m pip install celery[redis]
WORKDIR /app
COPY src /app/
ENV C_FORCE_ROOT="true"
CMD ["celery", "-A", "tasks", "worker", "--loglevel", "debug"]