# Anchors

- [About](#About)
- [Launch](#Launch)
---
# About
This repository is the server part of the website [halloween.veganrussian.ru](https://halloween.veganrussian.ru/), 
which is an administrative interface and database. 

The project is designed to be deployed on a server in an isolated Kubernetes container environment, which provides 
simplified scaling and allows automated deployment.

The project architecture is divided into modules, each of which performs a specific function and can be independently 
updated or scaled according to needs. In addition to the main backend, the repository can include configuration files, 
CI/CD scripts, documentation and other components necessary for the full development cycle.

---
- [Stage](https://github.com/Seal-Pavel/halloween.veganrussian.ru)
- [Backend](https://github.com/Seal-Pavel/halloween_vegan_backend)
- [API](https://seal-pavel.website/api/schema/swagger-ui/) (OpenApi3)

---
# Execution environment
Для локальной разработки и тестирования достаточно [Docker Desktop](https://www.docker.com/products/docker-desktop/) с включенной в настройках поддержкой kubernetes.

Для развертывания на сервере понадобится минимальная конфигурация: 2 CPU • 4 Гб RAM • 20 Гб NVMe, а также установить 
и настроить Kubernetes.

---
# Launch🚀

### `NameSpace`
Для изоляции я разворачиваю проект в своем пространстве имен(veg-hw):
```sh
kubectl apply -f ./shared-k8s/namespace-vegan-halloween.yaml
```

### `Environment variables`
Создайте .env файлы:
```sh
cp postgres/.env-example postgres/.env && cp app/.env-example app/.env
```
и заполните их своими данными:
```sh
sudo nano путь/до/файла/.env
```
(или через редактор: [postgres/.env](postgres%2F.env) и [app/.env](app%2F.env))

Чтобы сгенерировать секретный ключ django для проекта, выполните следующую команду в Python Shell:

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```
Эта команда выведет случайно сгенерированный DJANGO_SECRET_KEY. Добавьте его в ваш файл .env [app/.env](app%2F.env).

### `Kubernetes secrets`
Запустите генерацию секретов кубернетес из этих .env файлов:
```sh
kubectl create secret generic postgres-secret --from-env-file="./postgres/.env" --namespace=veg-hw --dry-run=client -o yaml > ./postgres/k8s/pg-secret.yaml
```
```sh
kubectl create secret generic django-secret --from-env-file="./app/.env" --namespace=veg-hw --dry-run=client -o yaml > ./app/k8s/django-secret.yaml
```
и примените их:
```sh
kubectl apply -f ./postgres/k8s/pg-secret.yaml
```
```sh
kubectl apply -f ./app/k8s/django-secret.yaml
```

### `Ingress Controller(Reverse Proxy)`
Для локальной разработки можно вместо прокси использовать port-forward до пода с приложением:
```sh
kubectl port-forward service/<deployment_name> <local_port>:<remote_port> -n veg-hw
```
Для сервера я использую NGINX Ingress Controller:
```sh
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update
helm install ingress-nginx ingress-nginx/ingress-nginx
```
и соответствующие манифесты для класса и ingress:
```sh
kubectl apply -f ./shared-k8s/ingress-class.yaml
```
```sh
kubectl apply -f ./app/k8s/django-ingress.yaml
```
```sh
kubectl apply -f ./app/k8s/chat-ingress.yaml
```

### `StorageClass`
(в Docker Desktop есть по умолчанию)

Для сервера я использую [Local Path Provisioner](https://github.com/rancher/local-path-provisioner):
```sh
kubectl apply -f https://raw.githubusercontent.com/rancher/local-path-provisioner/master/deploy/local-path-storage.yaml
```

### `Database(Postgres)`
Примените манифесты для базы данных:
```sh
kubectl apply -f ./postgres/k8s/pg-service.yaml
```
```sh
kubectl apply -f ./postgres/k8s/pg-statefulset.yaml
```

### `Django application`
Примените манифесты для django приложения:
```sh
kubectl apply -f ./app/k8s/django-service.yaml
```
```sh
kubectl apply -f ./app/k8s/django-deployment.yaml
```

