# Anchors

- [About](#About)
- [Launch](#Launch)

# About

This repository is the backend for the [halloween.veganrussian.ru](https://halloween.veganrussian.ru/).

# Launch🚀

### Заполнить .env файлы своими данными
```sh
$ sudo nano путь/до/файла/.env
```
```sh
$ sudo nano путь/до/файла/.env
```
### Запустить генерацию секретов кубернетес из этих .env файлов
```sh
$ kubectl create secret generic postgres-secret --from-env-file="./postgres/.env" --namespace=veg-hw --dry-run=client -o yaml > ./postgres/k8s/pg-secret.yaml
```
```sh
$ kubectl create secret generic django-secret --from-env-file="./app/.env" --namespace=veg-hw --dry-run=client -o yaml > ./app/k8s/django-secret.yaml
```
### Применить их
```sh
$ kubectl apply -f ./postgres/k8s/pg-secret.yaml
```
```sh
$ kubectl apply -f ./app/k8s/django-secret.yaml
```
### Сборка образа
#### [$ docker build -t ваше_имя_пользователя_docker_hub/my-django-app ./app]
```sh
$ docker build -t sealpavel/halloween_vegan_backend ./app
```
### Авторизация и деплой образа в dockerHub
#### [$ docker push ваше_имя_пользователя_docker_hub/my-django-app]
```sh
$ docker login
```
```sh
$ docker push sealpavel/halloween_vegan_backend
```