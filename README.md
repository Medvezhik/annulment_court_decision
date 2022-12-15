# Annulment Court Decision

![изображение](https://user-images.githubusercontent.com/114733751/207960109-2337a8f3-3766-4c31-a443-d424e7910540.png)

Проект посвящен исследованию решений судов общей юрисдикции первой инстанции на предмет возможности прогнозирования их отмены судами апелляционной инстанции.

# Настройка окружения

1. Установить Python 3.8
2. Установить python-библиотеки из requirements.txt.
```
pip install -r requirements.txt

# Если возникают проблема при установке pygit2, то вероятно вот этот баг:
# https://github.com/iterative/dvc/issues/7096
# В этом случае попробуйте:
pip install --prefer-binary -r requirements.txt
```
## Данные

Данные лежат в [Yandex Object Storage](https://cloud.yandex.ru/services/storage). Синхронизация данных делается через [dvc](https://dvc.org). Связаться с @nik123 для получения credentials для доступа к данным. Затем положить credentials в файл `~/.aws/credentials`. Протестировать доступ к данным:
```
dvc pull test.txt.dvc
```

# Статус

В работе было осуществлено написание парсеров для сбора данных, в необходимой связке: решение суда первой инстанции + результат рассмотрения апелляционной жалобы. Были разного рода сложности с разными сайтами - источниками данных, в том числе проблемы с выкладыванием решений судов без уникального идентификатора дела, что слишком затрудняло процесс поиска апелляционного решения по делу первой инстанции, или же наоброт, апелляционного определения по делу нижестоящей инстанции. Необходимые данные были собраны с сайта https://www.mos-gorsud.ru/, в количестве около 100000 обектов. Страницы, содержащие информацию о первой и второй инстанции отдельного дела, были распарсены и сохранены в формате csv для удобства дальнейшего их исследования и аппробации различных моделей машинного обучения. 

Бинарная классификация длинных текстов (предсказание отмены решения суда) осуществлялась спомощью логистической регрессии. Для этого тексты решений суда первично были оцищены от цифр, дат, и одиночных букв (содержащихся, например в Фамилия И.О. или  Ф.И.О.), затем производилась лемматизация, далее данные обрабатывались с использованием tfidfvectorizer, с параметрами, подобранными с условием - максимальное качество обученной модели при размере файла обученного tfidfvectorizer не более 1Гб. 

Взаимодействие с пользователем осуществляется посредством телеграмм-бота @predict_decision_bot, в котором реализованы минимальная проверка на предмет является ли присланный обект судебным решением, очистка входных данных, модель предсказания успешной апелляции. Модель реализована как отдельный сервис, в отдельном докер контейнере, через Fast Api.
