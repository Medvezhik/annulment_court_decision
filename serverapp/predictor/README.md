# Predictor

RestAPI сервер, делающий предикты по полученному тексту.

## Development environment

Настройка окружения для разработки:
1. Создать виртуальное окружение.
2. `pip install -r requirements.txt`
3. `pip install --prefer-binary -r dev-requirements.txt`
4. Создать файл `.env`
5. Прописать в `.env` переменные `VECTORIZER_PATH` и `MODEL_PATH`.

Запуск приложения:
```
export $(xargs <.env) && python -m predictor.main
```

## Docker

Сборка докер-образа:
```
DOCKER_BUILDKIT=1 docker build -t nkodenko/ods-acd-predictor -f Dockerfile .
```

Пример запуска докер-контейнера:
````
docker run --rm -v "$PWD":/data \
    -e VECTORIZER_PATH="/data/tfidf.joblib" \
    -e MODEL_PATH="/data/logreg.joblib" \
    -p 8080:8080 \
    nkodenko/ods-acd-predictor
```
