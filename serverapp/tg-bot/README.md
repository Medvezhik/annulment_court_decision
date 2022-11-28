# Телеграм-бот

```shell
# сборка докер-образа:
DOCKER_BUILDKIT=1 docker build -t nkodenko/ods-acd-tg-bot:latest -f Dockerfile .

# Для запуска нужно смонтировать в докер-образ файл конфигурации:
docker run --rm --mount type=bind,source=/path/to/config.yml,target=/app/config.yml nkodenko/ods-acd-tg-bot
```
