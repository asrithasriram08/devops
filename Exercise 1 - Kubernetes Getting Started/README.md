# Exercise 1 - Kubernetes Getting Started

This exercise deploys the Nginx storefront as a Kubernetes Pod and exposes it
through a NodePort Service.

## Deploy

```powershell
minikube start
kubectl apply -f hello-k8s.yaml
kubectl get pod hello-k8s
kubectl get service hello-k8s
minikube service hello-k8s
```

## Clean up

```powershell
kubectl delete -f hello-k8s.yaml
```

## Execution Evidence / Screenshots

![Exercise 1 screenshot 1](screenshots/exercise_1_1.png)
![Exercise 1 screenshot 2](screenshots/exercise_1_2.png)
![Exercise 1 screenshot 3](screenshots/exercise_1_3.png)
![Exercise 1 screenshot 4](screenshots/exercise_1_4.png)
![Exercise 1 screenshot 5](screenshots/exercise_1_5.png)
![Exercise 1 screenshot 6](screenshots/exercise_1_6.png)
