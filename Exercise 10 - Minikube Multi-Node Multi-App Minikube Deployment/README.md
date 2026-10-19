# Multi-Node Kubernetes Cluster with Multiple Applications

## Objective

This project deploys two simple Flask applications for an e-commerce scenario on a three-node Minikube cluster:

- Product Catalog (`AppA`): 2 replicas serving `GET /products`.
- Shopping Cart (`AppB`): 3 replicas serving `GET /cart` and `POST /cart`.

Deployments create the ReplicaSets and pods. Required pod anti-affinity keeps replicas of the same application on different nodes.

## Architecture

```text
Minikube profile: devops-multinode
  node 1: shopping-cart replica
  node 2: shopping-cart replica, product-catalog replica
  node 3: shopping-cart replica, product-catalog replica
```

The exact node names and assignments can vary. With three healthy nodes, anti-affinity distributes Shopping Cart across all three nodes and Product Catalog across two nodes.

The cart is intentionally an in-memory list. Each replica has its own list, so a cart item is not persistent or shared between replicas; this is expected for this assignment.

## Technologies

- Python
- Flask
- Docker
- Kubernetes
- Minikube
- kubectl

## Project Structure

```text
Assignment 2 (Multi-Node Minikube)/
├── product_catalog.py
├── shopping_cart.py
├── Dockerfile.product
├── Dockerfile.shopping
├── product_catalog_deployment.yaml
├── shopping_cart_deployment.yaml
├── product_catalog_service.yaml
├── shopping_cart_service.yaml
├── README.md
└── .gitignore
```

## Check My Environment

Run these commands in PowerShell, Command Prompt, or WSL:

```powershell
python --version
docker --version
kubectl version --client
minikube version
git --version
```

They check Python, Docker, kubectl, Minikube, and Git respectively. If a command is not found, install only that missing tool:

- Python: <https://www.python.org/downloads/windows/>. Enable **Add python.exe to PATH**.
- Docker: Docker Desktop for Windows at <https://www.docker.com/products/docker-desktop/>. Start Docker Desktop before using Minikube.
- kubectl: `winget install Kubernetes.kubectl`, or <https://kubernetes.io/docs/tasks/tools/install-kubectl-windows/>.
- Minikube: `winget install Kubernetes.minikube`, or <https://minikube.sigs.k8s.io/docs/start/>.
- Git: Git for Windows at <https://git-scm.com/download/win>.

Reopen the terminal after installation. WSL is optional; PowerShell is sufficient.

## Setup and Docker

Open PowerShell in this project folder:

```powershell
cd "C:\path\to\devops\Assignment 2 (Multi-Node Minikube)"
```

Build both images:

```powershell
docker build -t product-catalog:latest -f Dockerfile.product .
docker build -t shopping-cart:latest -f Dockerfile.shopping .
```

Optional local Flask checks can run one application at a time. Both listen on port 80, so running both directly together causes a port conflict:

```powershell
python product_catalog.py
python shopping_cart.py
```

Stop a local server with `Ctrl+C`.

## Create the Three-Node Minikube Cluster

If an old profile is interfering, clean it up first:

```powershell
minikube stop -p devops-multinode
minikube delete -p devops-multinode
```

Create the required profile:

```powershell
minikube start --nodes 3 -p devops-multinode
```

Do not add `--force` for a normal Docker Desktop setup. Use it only when Minikube explicitly reports a recoverable problem and recommends it. If startup fails, see Troubleshooting.

Load the locally built images into the Minikube nodes:

```powershell
minikube -p devops-multinode image load product-catalog:latest
minikube -p devops-multinode image load shopping-cart:latest
```

`imagePullPolicy: Never` tells Kubernetes to use the image already loaded into Minikube and not try Docker Hub. A registry add-on is not needed when `image load` succeeds.

## Kubernetes Deployment

Apply the Deployments first, then the Services:

```powershell
kubectl apply -f product_catalog_deployment.yaml
kubectl apply -f shopping_cart_deployment.yaml

kubectl apply -f product_catalog_service.yaml
kubectl apply -f shopping_cart_service.yaml
```

All manifests explicitly use the `default` namespace. Verify the cluster and workloads:

```powershell
kubectl get nodes
kubectl get deployments
kubectl get pods
kubectl get pods -o wide
kubectl get services
```

Expected results:

- `kubectl get nodes`: three nodes in `Ready` state.
- `kubectl get deployments`: `product-catalog` at `2/2` and `shopping-cart` at `3/3`.
- `kubectl get pods`: five running application pods after startup.
- `kubectl get pods -o wide`: the `NODE` column shows distribution.
- `kubectl get services`: both `NodePort` services and assigned ports.

## Verify Replica Distribution

The most important evidence command is:

```powershell
kubectl get pods -o wide
```

The two `product-catalog` pods must have different node names. The three `shopping-cart` pods must each have a different node name. Pod names are generated automatically.

The manifests use `podAntiAffinity.requiredDuringSchedulingIgnoredDuringExecution` with topology key `kubernetes.io/hostname`. If a pod is `Pending`, inspect it:

```powershell
kubectl describe pod <pod-name>
kubectl get nodes
kubectl get events --sort-by=.lastTimestamp
```

Look for anti-affinity or insufficient-node messages. Confirm that three nodes are `Ready`, that this is the intended profile, and that no other pods consume all resources. Required anti-affinity intentionally refuses to place same-application replicas on one node.

After correcting the cluster, recreate the workloads:

```powershell
kubectl delete -f product_catalog_deployment.yaml
kubectl delete -f shopping_cart_deployment.yaml
kubectl apply -f product_catalog_deployment.yaml
kubectl apply -f shopping_cart_deployment.yaml
```

## Access Services and Test APIs

Ask Minikube to open each NodePort service:

```powershell
minikube -p devops-multinode service product-catalog-service
minikube -p devops-multinode service shopping-cart-service
```

These commands find the assigned NodePort and open or print a reachable URL. The localhost port may differ from examples. Print URLs without opening a browser with:

```powershell
minikube -p devops-multinode service product-catalog-service --url
minikube -p devops-multinode service shopping-cart-service --url
```

Use the printed values as `<PRODUCT_URL>` and `<CART_URL>`:

```powershell
curl.exe "<PRODUCT_URL>/products"
curl.exe "<CART_URL>/cart"
curl.exe -X POST "<CART_URL>/cart" -H "Content-Type: application/json" -d '{"id":1,"name":"Laptop","quantity":1}'
curl.exe "<CART_URL>/cart"
```

The Product Catalog response contains Laptop, Phone, and Headphones. The first cart GET returns `[]`. A successful POST returns HTTP `201` and the updated list. Because the cart is in memory, a later request may reach another replica with its own list.

PowerShell often aliases `curl` to `Invoke-WebRequest`; use `curl.exe` for curl syntax or use native PowerShell:

```powershell
Invoke-RestMethod -Uri "<PRODUCT_URL>/products"
Invoke-RestMethod -Uri "<CART_URL>/cart"
Invoke-RestMethod -Uri "<CART_URL>/cart" -Method Post -ContentType "application/json" -Body '{"id":1,"name":"Laptop","quantity":1}'
```

In CMD, use `curl` with escaped double quotes: `-d "{\"id\":1,\"name\":\"Laptop\",\"quantity\":1}"`. In WSL, use normal Linux curl quoting.

## Troubleshooting

**Docker not installed or not running:** install Docker Desktop, start it, then run `docker --version` and `docker run hello-world`. Minikube cannot use the Docker driver until Docker Desktop is running.

**Minikube not installed:** run `winget install Kubernetes.minikube`, reopen PowerShell, and run `minikube version`.

**kubectl not installed:** run `winget install Kubernetes.kubectl`, reopen PowerShell, and run `kubectl version --client`.

**Git not installed:** install Git for Windows, reopen PowerShell, and run `git --version`.

**Minikube will not start:** run `docker info`, `minikube status -p devops-multinode`, and `minikube logs -p devops-multinode`. Ensure Docker Desktop is running and virtualization is enabled. If needed, delete only this profile and retry.

**`ImagePullBackOff` or `ErrImageNeverPull`:** rebuild, load into this exact profile, and inspect the pod:

```powershell
docker images
minikube -p devops-multinode image load product-catalog:latest
minikube -p devops-multinode image load shopping-cart:latest
kubectl describe pod <pod-name>
```

**Pod stuck in `Pending`:** run `kubectl describe pod <pod-name>`. Check Events for required anti-affinity, missing nodes, or resource pressure. `kubectl get nodes` must show three `Ready` nodes for three Shopping Cart replicas.

**Service does not open:** check:

```powershell
kubectl get services
kubectl describe service product-catalog-service
kubectl describe service shopping-cart-service
minikube -p devops-multinode service product-catalog-service --url
```

Ensure selectors match pod labels and pods are `Running` and `Ready`.

**Flask container crashes:** inspect:

```powershell
kubectl logs <pod-name>
kubectl describe pod <pod-name>
```

## GitHub

Create an empty repository on GitHub. Replace `<MY_GITHUB_REPOSITORY_URL>` below with the HTTPS URL copied from that repository; do not invent a URL:

```powershell
git init
git add .
git commit -m "feat: add multi-node minikube deployment"
git branch -M main
git remote add origin <MY_GITHUB_REPOSITORY_URL>
git push -u origin main
```

For example, the replacement looks like `https://github.com/your-user/your-repository.git`. Verify locally with `git log --oneline --decorate -1`, then refresh GitHub and open its commit history. The message and timestamp should be visible.

## Evidence Checklist

Run these only after the cluster works and capture screenshots from your own machine. Do not fake output:

1. `minikube status -p devops-multinode` showing the profile is running.
2. `kubectl get nodes` showing three `Ready` nodes.
3. `docker images` showing both application images.
4. `kubectl get deployments` showing `product-catalog 2/2` and `shopping-cart 3/3`.
5. `kubectl get pods -o wide` showing replicas distributed across nodes. This is the key screenshot.
6. `kubectl get services` showing both NodePort services.
7. Product Catalog API response containing all three products.
8. Shopping Cart GET, POST, and updated GET responses.
9. GitHub repository page showing the project files.
10. GitHub commit history showing the commit and timestamp.

## Do This In Order

1. Run the five environment check commands.
2. Install only missing tools and start Docker Desktop.
3. Open PowerShell in `Assignment 2 (Multi-Node Minikube)`.
4. Confirm the nine project files are present.
5. Optionally run each Flask app locally, one at a time, and stop it with `Ctrl+C`.
6. Build `product-catalog:latest` with `Dockerfile.product`.
7. Build `shopping-cart:latest` with `Dockerfile.shopping`.
8. Stop and delete the old `devops-multinode` profile if necessary.
9. Start `minikube start --nodes 3 -p devops-multinode`.
10. Load both images with `minikube -p devops-multinode image load`.
11. Apply `product_catalog_deployment.yaml`.
12. Apply `shopping_cart_deployment.yaml`.
13. Apply `product_catalog_service.yaml`.
14. Apply `shopping_cart_service.yaml`.
15. Run `kubectl get nodes` and wait for three `Ready` nodes.
16. Run `kubectl get deployments` and wait for `2/2` and `3/3`.
17. Run `kubectl get pods -o wide` and confirm node distribution.
18. Get the Product Catalog URL with the Minikube service command.
19. Get the Shopping Cart URL with the Minikube service command.
20. Test Product Catalog `GET /products`.
21. Test Shopping Cart `GET /cart`.
22. Test Shopping Cart `POST /cart`, then run `GET /cart` again.
23. Capture the ten evidence screenshots listed above.
24. Run `git init` and `git add .`.
25. Commit with `git commit -m "feat: add multi-node minikube deployment"`.
26. Create an empty GitHub repository and copy its real HTTPS URL.
27. Add that URL with `git remote add origin <MY_GITHUB_REPOSITORY_URL>`.
28. Push with `git push -u origin main`.
29. Verify the repository files and commit history on GitHub.
