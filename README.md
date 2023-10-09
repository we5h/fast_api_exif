# Практическое задание для отработки mongodb, fastapi.
---

### Сервис дает возможность загрузить фото и получить его exif данные.
---
## Как запустить проект:

- Клонировать репозиторий и перейти в него в командной строке:

```
https://github.com/we5h/fast_api_exif.git
```

- Установить Docker:

```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

либо Docker Desktop для вашей платформы:
https://docs.docker.com/engine/install/

- Перейти в корень проекта и выполнить команду:

```
docker сompose up -d
```
Теперь мы можем выполнить запросы в Fastapi : 127.0.0.1:8000

### Endpoints:


**Для лучшего опыта взаимодействия используйте swagger - /docs/**

1)
GET /photos/ - получим список загруженных фото.

2)
GET /photos/{id}/ - получим exif данные конкретной фотографии, если они существуют.

3)
POST /photos/ - загружаем фотографию(Валидация на определенные форматы).
