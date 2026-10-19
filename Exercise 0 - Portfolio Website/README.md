# Personal Portfolio

## About

A static personal portfolio for Asritha Sriram, an Information Science and Engineering student at B.M.S College of Engineering. It presents her work across software development, AI/ML, cloud computing, research, and full-stack projects.

## Features

- Responsive single-page portfolio
- Scroll reveal animations and active navigation
- Mobile navigation menu
- Interactive project card hover states
- Terminal-inspired hero panel
- Experience timeline, skills, education, certifications, and contact sections

## Technologies

- HTML
- CSS
- JavaScript
- Nginx
- Docker

## Running Locally

No Node.js or npm is required. Open `index.html` directly in a browser.

## Running with Docker

The static website is containerized with Docker and served by Nginx:

```powershell
docker build -t asritha-portfolio .
docker run -p 8080:80 asritha-portfolio
```

Open http://localhost:8080 in a browser.

## Project Structure

```text
Exercise 0 - Portfolio Website/
├── index.html
├── style.css
├── script.js
├── README.md
├── Dockerfile
└── .gitignore
```

## DevOps

Docker packages the static site into an image, while Nginx serves the HTML, CSS, and JavaScript from the running container. Git and GitHub provide version control and repository history.

### Docker on Windows

1. Check whether Docker is installed:

   ```powershell
   docker --version
   ```

2. If it is not installed, download Docker Desktop for Windows from https://www.docker.com/products/docker-desktop/, run the installer, keep the recommended WSL 2 option, and restart Windows if prompted. Open Docker Desktop and wait until it reports that it is running.

3. Verify the installation:

   ```powershell
   docker run hello-world
   ```

4. Open PowerShell in this folder, the folder containing `Dockerfile`, and build the image:

   ```powershell
   docker build -t asritha-portfolio .
   ```

5. Run the container:

   ```powershell
   docker run -p 8080:80 asritha-portfolio
   ```

   Visit http://localhost:8080. Keep this terminal open while using the site.

6. In another PowerShell window, see running containers:

   ```powershell
   docker ps
   ```

   Stop a container with its ID or name:

   ```powershell
   docker stop <container-id-or-name>
   ```

   Remove a stopped container when needed:

   ```powershell
   docker rm <container-id-or-name>
   ```

### Git and GitHub

1. Check whether Git is installed:

   ```powershell
   git --version
   ```

2. If needed, install Git for Windows from https://git-scm.com/downloads, using the recommended installer options. Reopen PowerShell afterward.

3. On GitHub, choose **New repository**, enter a portfolio repository name, choose the visibility required by your class, and create it without adding another README. Do not use a URL until GitHub has created the repository.

4. In PowerShell, move into this project folder and initialize Git:

   ```powershell
   cd "C:\path\to\Exercise 0 - Portfolio Website"
   git init
   git branch -M main
   ```

5. Add the files and create the first commit:

   ```powershell
   git add index.html style.css script.js README.md Dockerfile .gitignore
   git commit -m "Create personal portfolio website"
   ```

6. Connect the local project to your GitHub repository. Replace the placeholder with the actual URL copied from GitHub:

   ```powershell
   git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
   ```

7. Push the project:

   ```powershell
   git push -u origin main
   ```

Useful commands for showing your professor the project history:

```powershell
git log --oneline --decorate --all
git log --stat
git show --summary
```

`git log --oneline --decorate --all` shows commit IDs, messages, branch labels, and all visible local references. `git log --stat` shows commit dates and which files changed. `git show --summary` shows the selected commit, author, date, and message. GitHub displays the pushed commit history on the repository's commits page and individual commit details after pushing.
