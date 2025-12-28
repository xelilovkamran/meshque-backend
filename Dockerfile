FROM python:3.12.2-alpine3.19
LABEL maintainer="Kamran Khalilov"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache \
      postgresql-client \
      jpeg-dev \
    && apk add --no-cache --virtual .tmp-build-deps \
      build-base \
      postgresql-dev \
      musl-dev \
      zlib-dev \
      linux-headers

# install uv (global)
RUN pip install --no-cache-dir uv

# project root
WORKDIR /meshque

# copy only dependency files first
COPY pyproject.toml uv.lock ./

# tell uv where the venv must live
ENV UV_PROJECT_ENVIRONMENT=/py
RUN uv venv /py && uv sync --frozen --no-dev

# now copy the rest
COPY . .

RUN mkdir -p /scripts \
  && cp -r /meshque/scripts/* /scripts/ \
  && chmod -R +x /scripts \
  && adduser --disabled-password --no-create-home django-user \
  && mkdir -p /vol/web/media /vol/web/static \
  && chown -R django-user:django-user /vol \
  && chmod -R 755 /vol \
  && apk del .tmp-build-deps

ENV PATH="/scripts:/py/bin:$PATH"

WORKDIR /meshque/app
EXPOSE 8000

USER django-user
CMD ["run.sh"]
