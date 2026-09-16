# Flask Flash Sale - Kubernetes ReplicaSet

## Objective

This exercise deploys a simple Flask flash-sale checkout service to a **single-node Minikube cluster** using a Kubernetes **ReplicaSet**. It starts with 3 Pods, scales to 5, and demonstrates self-healing when one Pod is deleted.

## Architecture

```text
Minikube
   |
   +-- 1 node
        |
        +-- ReplicaSet: flashsale-rs
             +-- 3 Pods initially
             +-- 5 Pods after scaling
                  |
                  +-- Service: flashsale-svc
```

All five Pods should show the same node in `kubectl get pods -o wide`, because this assignment intentionally uses one Minikube node.

## Project Structure

```text
Assignment 3 (Flask ReplicaSet Scaling)/
|-- ex3-flash-sale.py
|-- Dockerfile
|-- flashsale-replicaset.yaml
|-- README.md
`-- .gitignore
```

## Application Endpoints

- `GET /` returns a welcome message, timestamp, and the Pod hostname.
- `GET /buy` returns a randomly selected item, user, time, and serving Pod. Use `/buy?user=123` to provide a user; without it, the app generates one.
- `GET /health` returns the health status and Pod hostname. Kubernetes uses this endpoint for readiness and liveness probes.

The sale items are `Smartphone`, `Shoes`, `Headphones`, and `Laptop`.

## Check Your Environment

Run these commands in PowerShell:

```powershell
python --version
docker --version
kubectl version --client
minikube version
git --version
```

Install only missing tools:

- Python: install Python for Windows from <https://www.python.org/downloads/windows/> and enable **Add python.exe to PATH**.
- Docker: install Docker Desktop for Windows from <https://www.docker.com/products/docker-desktop/> and start it before using Minikube.
- kubectl: run `winget install Kubernetes.kubectl`, or follow <https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/>.
- Minikube: run `winget install Kubernetes.minikube`, or follow <https://minikube.sigs.k8s.io/docs/start/>.
- Git: install Git for Windows from <https://git-scm.com/download/win>.

Reopen PowerShell after installing a command-line tool. WSL is optional; the commands below work in PowerShell.

## Docker

Build the image from this project folder:

```powershell
docker build -t flashsale:1.0 .
```

The Kubernetes manifest uses `imagePullPolicy: Never`, so Minikube must have a local copy of the image. With Docker Desktop on Windows, the simplest approach is:

```powershell
minikube image load flashsale:1.0
```

This loads the image into Minikube without requiring Docker Hub. Docker Hub is not required for this assignment. If you do need to publish it, tag it with your own Docker Hub username and push it:

```powershell
docker tag flashsale:1.0 YOUR-DOCKERHUB-USERNAME/flashsale:1.0
docker push YOUR-DOCKERHUB-USERNAME/flashsale:1.0
```

Do not use `eval $(minikube docker-env)` in PowerShell; `minikube image load` is the portable Windows approach.

## Start One-Node Minikube

Stop and remove an old default cluster only if necessary:

```powershell
minikube stop
minikube delete
```

Start the required single-node cluster:

```powershell
minikube start --nodes=1
kubectl get nodes
```

The successful result has exactly one `Ready` Minikube node. If no old cluster exists, `minikube stop` or `minikube delete` may report that there is nothing to do.

## Apply the ReplicaSet

From this folder, apply both the ReplicaSet and Service in the same manifest:

```powershell
kubectl apply -f flashsale-replicaset.yaml
kubectl get rs
kubectl get pods
```

The ReplicaSet should show `DESIRED 3`, `CURRENT 3`, and `READY 3`. Kubernetes generates Pod names dynamically, so do not expect fixed names.

## Test the Application

The Service is internal (`ClusterIP`). In one PowerShell window, forward it to your computer:

```powershell
kubectl port-forward service/flashsale-svc 8080:80
```

Keep that command running and use a second PowerShell window:

```powershell
Invoke-RestMethod http://localhost:8080/
Invoke-RestMethod http://localhost:8080/buy
Invoke-RestMethod "http://localhost:8080/buy?user=123"
Invoke-RestMethod http://localhost:8080/health
```

Each response includes the hostname of the Pod that handled the request. Stop port-forwarding with `Ctrl+C` when finished. You can also run `minikube service flashsale-svc` in a separate terminal if preferred.

## Scale From 3 to 5

```powershell
kubectl scale rs flashsale-rs --replicas=5
kubectl get rs
kubectl get pods
```

The ReplicaSet changes from 3 desired Pods to 5 and Kubernetes creates 2 additional Pods. Wait until the ReplicaSet reports `5 5 5` and all five Pods are `Running` and `Ready`.

## Demonstrate Self-Healing

List the real Pod names:

```powershell
kubectl get pods
```

Copy one actual name from that output and replace the placeholder:

```powershell
kubectl delete pod <actual-pod-name>
kubectl get pods
kubectl get pods -w
```

The ReplicaSet sees that the actual count briefly dropped from 5 to 4, then creates a replacement. The desired count remains 5. Press `Ctrl+C` after the replacement is `Running` and `Ready`.

## Verify Single-Node Distribution

```powershell
kubectl get pods -o wide
```

All five Pods should list the same node. This is expected for a one-node cluster and differs from the previous multi-node exercise.

## Useful Diagnostics

```powershell
kubectl get pods
kubectl describe pod <pod-name>
kubectl logs <pod-name>
kubectl describe rs flashsale-rs
kubectl get svc
minikube status
```

- `get pods` shows Pod status and readiness.
- `describe pod` shows scheduling, probe, image, and event details.
- `logs` shows application output from one Pod.
- `describe rs` shows ReplicaSet selectors, counts, and events.
- `get svc` shows the Service and its ports.
- `minikube status` shows whether the Minikube control plane, host, and kubelet are running.

## Evidence Checklist

Capture screenshots from your own computer; do not fabricate command output.

1. `minikube status` showing Minikube is running.
2. `kubectl get nodes` showing exactly one Ready node.
3. `kubectl get rs` showing 3 replicas initially.
4. `kubectl get pods` showing 3 Pods.
5. The `/`, `/buy`, or `/health` response showing a Pod hostname.
6. `kubectl scale rs flashsale-rs --replicas=5` followed by `kubectl get rs` showing 5 replicas.
7. `kubectl get pods` showing 5 Pods.
8. `kubectl delete pod <actual-pod-name>` followed by Pod output showing the replacement.
9. `kubectl get pods -o wide` showing all Pods on the one node.
10. The GitHub repository page showing these files.
11. GitHub commit history showing the commit timestamp.

## GitHub

From the repository root, commit the new folder. The existing assignments remain untouched:

```powershell
git add "Assignment 3 (Flask ReplicaSet Scaling)"
git commit -m "feat: add Flask ReplicaSet scaling exercise"
git push origin main
```

The repository already has a remote configured. If you are setting up a different clone, create an empty GitHub repository and replace the placeholder below with the real HTTPS URL copied from GitHub; do not invent a URL:

```powershell
git remote add origin <MY_GITHUB_REPOSITORY_URL>
git push -u origin main
```

Verify locally with `git log --oneline --decorate -1`, then refresh GitHub and open the repository's commit history. The commit message and timestamp should be visible.

## Do This In Order

1. Run the five environment check commands.
2. Install only missing tools and start Docker Desktop.
3. Open PowerShell in this repository and create/open `Assignment 3 (Flask ReplicaSet Scaling)`.
4. Confirm the five project files are present.
5. Build `flashsale:1.0` with Docker.
6. Stop and delete an old Minikube cluster if necessary.
7. Start Minikube with `minikube start --nodes=1`.
8. Load the image with `minikube image load flashsale:1.0`.
9. Apply `flashsale-replicaset.yaml`.
10. Run `kubectl get rs` and `kubectl get pods`; confirm 3 ready Pods.
11. Port-forward `flashsale-svc` and test `/`, `/buy`, and `/health`.
12. Run `kubectl scale rs flashsale-rs --replicas=5`.
13. Confirm 5 ready Pods with `kubectl get rs` and `kubectl get pods`.
14. Delete one actual Pod name from `kubectl get pods`.
15. Run `kubectl get pods -w` and observe the replacement.
16. Run `kubectl get pods -o wide` and confirm one node for every Pod.
17. Capture the evidence screenshots.
18. Create the GitHub repository if needed.
19. Run `git add "Assignment 3 (Flask ReplicaSet Scaling)"`.
20. Commit with `git commit -m "feat: add Flask ReplicaSet scaling exercise"`.
21. Push with `git push origin main`.
22. Verify the files, commit, and timestamp on GitHub.
