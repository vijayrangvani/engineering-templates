# Kubernetes templates

Files are numbered in apply order. Try it locally with kind:

```bash
kind create cluster --name dev
docker build -t items-api:1.0 ../fastapi-app
kind load docker-image items-api:1.0 --name dev   # copy local image into the cluster nodes
cp 02-secret.example.yaml 02-secret.yaml          # edit values (02-secret.yaml is git-ignored)
kubectl apply -f 00-namespace.yaml -f 01-configmap.yaml -f 02-secret.yaml -f 03-deployment.yaml -f 04-service.yaml
kubectl -n items get pods,svc
kubectl -n items port-forward svc/items-api 8000:80
```

The default DATABASE_URL points to a Postgres that is not in this folder. For a quick test, set it to
`sqlite:///./app.db` in your secret.

## Don't memorise fields, look them up
```bash
kubectl explain deployment.spec.template.spec.containers   # shows fields + docs for any path
kubectl explain deployment.spec --recursive | less
kubectl create deployment x --image=nginx --dry-run=client -o yaml   # generate a starting YAML
```
