# Телеграм-бот

```shell
# TODO: correct tag
# сборка докер-образа:
DOCKER_BUILDKIT=1 docker build -t cr.yandex/crpvs8762goaofer3sio/tg-bot:latest -f Dockerfile .

# Для запуска нужно смонтировать в докер-образ файл конфигурации:
docker run -it --rm  --mount type=bind,source=/path/to/config.yml,target=/app/config.yml tmp_nik /bin/sh
```