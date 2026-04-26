# Docker

### What is Docker?

* Docker is a container technology: A tool for creating and managing containers
* Container is a standardized unit of software.
  - a package of code **and** dependencies to run that code. (ex. Py code + the Py runtime)
  - the same container yields the exact same application and execution behaviour, irrespective of executor or the system of execution.

### Why Containers?

For independent and standardized "application packages"

* because we want the`exact same env` for dev & prod
* we want`reproducibility` of behaviour
* for isolation of dependencies/preventing dependency conflicts

### Virutal Machines vs. Docker Containers

* Simple Virtual Machine structure

- This wastes a lot of space on the hard drive and tends to be slow

```mermaid
flowchart TB
  host["Your Operating System"]

  subgraph A["Environment A"]
    A1["App A"]
    A2["Libraries, Dependencies, Tools"]
    A3["Virtual OS (e.g. Linux)"]
    A1 --> A2 --> A3
  end

  subgraph B["Environment B"]
    B1["App B"]
    B2["Libraries, Dependencies, Tools"]
    B3["Virtual OS (e.g. Linux)"]
    B1 --> B2 --> B3
  end

  subgraph C["Environment C"]
    C1["App C"]
    C2["Libraries, Dependencies, Tools"]
    C3["Virtual OS (e.g. Linux)"]
    C1 --> C2 --> C3
  end

  A3 --> host
  B3 --> host
  C3 --> host
```

| Pros of VM                                     |                      Cons of VM                      |
| ---------------------------------------------- | :--------------------------------------------------: |
| Separated environments                         |              Redundant, Waste of space              |
| Env-specific config                            |        Slow performance and longer boot time        |
| Shareable env-config for reproducing behaviour | reproducing on another server is possible but tricky |

### Docker Containers

```mermaid
flowchart TB

subgraph C1[Container A]
A1[App A]
L1[Libraries, Dependencies, Tools]
A1 --> L1
end

subgraph C2[Container B]
A2[App B]
L2[Libraries, Dependencies, Tools]
A2 --> L2
end

subgraph C3[Container C]
A3[App C]
L3[Libraries, Dependencies, Tools]
A3 --> L3
end

Docker[Docker Engine]
Support[OS Built-in / Emulated Container Support]
HostOS[Your Operating System]

L1 --> Docker
L2 --> Docker
L3 --> Docker

Docker --> Support
Support --> HostOS
```

| Docker Containers                                  | Virtual Machines                                                     |
| -------------------------------------------------- | -------------------------------------------------------------------- |
| Low impact on OS, very fast and minimal disk usage | High impact on OS, slower and higher disk usage                      |
| Sharing, re-building & distribution is easy        | Sharing, re-building & distribution can be tricky                    |
| Encapsulates the app/environment                   | Encapsulates the whole machine ~ results in bloating the application |


### Images

- Images are **blueprints / templates** for containers — they do not run themselves
- Contain the app code + required tools, runtimes, and OS dependencies
- Images are **read-only**; no application data is stored in them
- Come in two flavors:
  - **Pre-built** — pulled from Docker Hub (e.g. `node`, `python`, `nginx`)
  - **Custom** — defined by writing your own `Dockerfile`

### Containers

- Containers are **running instances of Images**
- When a container is created (`docker run`), a thin **read-write layer** is added on top of the image
- Multiple containers can run from the **same image**, each fully isolated with their own data
- Data in the container layer is **ephemeral** — lost when the container is removed

```
┌────────────────────────────────────────────┐
│  Container Writable Layer  ✏️               │  ← unique per container, lost on removal
├────────────────────────────────────────────┤
│  Layer N: CMD ["npm", "start"]  🔒          │
│  Layer 3: EXPOSE 80             🔒          │  ← read-only image layers
│  Layer 2: RUN npm install       🔒          │  ← cached & shared across containers
│  Layer 1: COPY . /app           🔒          │
│  Layer 0: FROM node (base image) 🔒         │
└────────────────────────────────────────────┘
```

### Image Layers & Caching

- Every Dockerfile instruction creates a **new layer** in the image
- Docker **caches** unchanged layers — only modified layers and those after are rebuilt
- Layers are **shared between images**, keeping images small and builds fast
- The `CMD` instruction is special: it runs when the **container starts**, not during the build

### Building a Custom Image (Dockerfile)

Key Dockerfile instructions:

| Instruction | Purpose |
|---|---|
| `FROM <image>` | Base image to build upon |
| `WORKDIR <path>` | Set working directory inside container |
| `COPY <src> <dest>` | Copy files from host into the container |
| `RUN <cmd>` | Execute a command during image build |
| `EXPOSE <port>` | Document the port the app listens on |
| `CMD ["cmd"]` | Default command to run when container starts |

```Dockerfile
FROM node                   # start from official node base image
WORKDIR /app                # all subsequent commands run from /app
COPY . /app                 # copy host project files into /app
RUN npm install             # install dependencies (runs at build time)
EXPOSE 80                   # document that app listens on port 80
CMD ["node", "server.js"]   # run the app when container starts
```

# Basic Commands

### Images

| Command | Description |
|---|---|
| `docker build .` | Build image from Dockerfile in current directory |
| `docker build -t <name> .` | Build and tag with a name |
| `docker build -t <name>:<tag> .` | Build and tag with a specific version |
| `docker build -t <name> <path>` | Build from Dockerfile in a different directory |
| `docker images` | List all locally stored images |
| `docker image inspect <name>` | Inspect image metadata (layers, config, env) |
| `docker rmi <image-id>` | Remove a specific image |
| `docker rmi -f <image-id>` | Force-remove image (even if in use) |
| `docker rmi <img-1> <img-2>` | Remove multiple images |
| `docker image prune` | Remove all dangling (untagged) images |
| `docker image prune -a` | Remove ALL unused local images |

---

### Container Lifecycle

| Command | Description |
|---|---|
| `docker run <image>` | Create and start a container |
| `docker run -p 3000:80 <image>` | Map host port 3000 → container port 80 |
| `docker run -d <image>` | Run in detached (background) mode |
| `docker run -it <image>` | Run in interactive terminal mode |
| `docker run --name <name> <image>` | Assign a custom name to the container |
| `docker run --rm <image>` | Auto-remove container when it stops |
| `docker run -d -p 3000:80 --name myapp --rm <image>` | Combine flags (most common pattern) |
| `docker ps` | List running containers |
| `docker ps -a` | List all containers (running + stopped) |
| `docker stop <id/name>` | Gracefully stop a running container |
| `docker start <id/name>` | Start a stopped container |
| `docker start -a <id/name>` | Start and attach (see output) |
| `docker start -ai <id/name>` | Start in interactive + attached mode |
| `docker rm <id/name>` | Remove a stopped container |
| `docker rm -f <id/name>` | Force-remove a running container |
| `docker rm <c-1> <c-2>` | Remove multiple containers |
| `docker container prune` | Remove all stopped containers |

---

### Attach & Detach

| Command | Description |
|---|---|
| `docker attach <id/name>` | Attach to a running detached container |
| `docker attach --sig-proxy=false <id/name>` | Attach without forwarding signals (safer) |
| `Ctrl + P, Ctrl + Q` | Detach from container without stopping it |

---

### Exec — Run Commands Inside a Container

| Command | Description |
|---|---|
| `docker exec <id/name> <cmd>` | Run a one-off command in a running container |
| `docker exec -it <id/name> bash` | Open an interactive bash shell |
| `docker exec -it -u root <id/name> bash` | Open shell as root user |
| `docker exec -it -e VAR=value <id/name> bash` | Set env variable for the session |
| `docker exec -it -w /app <id/name> bash` | Open shell in a specific working directory |

---

### Inspect & Logs

| Command | Description |
|---|---|
| `docker logs <id/name>` | View container logs |
| `docker logs -f <id/name>` | Follow logs in real time |
| `docker container inspect <id/name>` | Full container metadata (network, mounts, etc.) |
| `docker image inspect <name>` | Full image metadata (layers, env, entrypoint) |
| `docker inspect --format='{{.NetworkSettings.IPAddress}}' <id>` | Extract a specific field |

---

### Copying Files

| Command | Description |
|---|---|
| `docker cp <id>:<container-path> <host-path>` | Copy file/dir **from** container to host |
| `docker cp <host-path> <id>:<container-path>` | Copy file/dir **from** host into container |

```bash
docker cp myapp:/app/logs/error.log ./error.log   # container → host
docker cp ./config.json myapp:/app/config.json    # host → container
```

---

### Sharing Images (DockerHub)

| Command | Description |
|---|---|
| `docker tag <image> <user>/<repo>:<tag>` | Tag image with DockerHub repo name |
| `docker login` | Login to DockerHub |
| `docker logout` | Logout from DockerHub |
| `docker push <user>/<repo>:<tag>` | Push image to DockerHub |
| `docker pull <user>/<repo>:<tag>` | Pull image from DockerHub |

```bash
docker tag myapp myuser/myapp:latest
docker push myuser/myapp:latest
```

---

### Cleanup

| Command | Removes |
|---|---|
| `docker rm <id/name>` | A stopped container |
| `docker rm -f <id/name>` | A running container (force) |
| `docker container prune` | All stopped containers |
| `docker rmi <image-id>` | A specific image |
| `docker image prune` | Dangling (untagged) images |
| `docker image prune -a` | All unused images |
| `docker system prune` | Stopped containers + dangling images + build cache |
| `docker system prune -a` | Everything above + all unused images |

# Data and Volumes

### The Problem

| Problem | Cause | Solution |
|---|---|---|
| Data written in a container **doesn't persist** | Container layer is destroyed on removal | **Volumes** |
| Host file changes **not reflected** in container | Image is read-only; code is copied at build time | **Bind Mounts** |

---

### Data Categories

| Type | Who writes it | Storage | Persisted? |
|---|---|---|---|
| **App Code + Env** | Developer | Baked into Image | ✅ (read-only) |
| **Temporary App Data** | App at runtime | Memory / temp files | ❌ |
| **Permanent App Data** | App at runtime | Volumes | ✅ Must persist |

---

### Storage Types — Overview

```
┌──────────────────────────────────────────────────────┐
│                  docker run -v ...                   │
├─────────────────────┬────────────────────────────────┤
│   Volumes           │        Bind Mounts             │
│  (Managed by Docker)│       (Managed by YOU)         │
├──────────┬──────────┤                                │
│ Anonymous│  Named   │  You control the host path     │
│ (auto    │ (persist │  Best for live code sync       │
│ removed) │ removal) │  during development            │
└──────────┴──────────┴────────────────────────────────┘
```

---

### Anonymous Volumes

- Created with `-v /path/in/container` (no name given)
- Docker manages the location on the host — you don't know where
- **Auto-removed** when container stops if `--rm` was used
- Can also be declared in a `Dockerfile`: `VOLUME ["/path"]`
- Useful for **protecting specific container paths** from being overwritten by a Bind Mount

```bash
docker run --rm -v /app/node_modules <image>
```

---

### Named Volumes

- Created with `-v some-name:/path/in/container`
- **Cannot** be defined in a Dockerfile — only via `docker run`
- **NOT** removed when a container is removed
- Data survives container removal and can be re-mounted to a new container
- Best for: **databases, logs, any data that must persist**

```bash
docker run -v mydata:/app/data <image>
```

---

### Bind Mounts

- Created with `-v /absolute/host/path:/path/in/container`
- **You control** exactly where the folder lives on the host
- **Cannot** be defined in a Dockerfile — only via `docker run`
- Changes on the host are **immediately reflected** in the container (no rebuild needed)
- Best for: **live-syncing source code during development**
- ⚠️ Not suitable for production — requires a specific host filesystem path

```bash
# macOS / Linux
docker run -v $(pwd):/app <image>

# Windows CMD
docker run -v %cd%:/app <image>

# Windows PowerShell
docker run -v ${pwd}:/app <image>
```

---

### Mounting Mechanics

> **If the volume/mount target path in the container is empty:**
> → Container files are **COPIED INTO** the volume.

> **If the volume/mount is NOT empty:**
> → Volume content **takes ownership** of the folder. Existing container files are **hidden** (not deleted).

### 🛡️ Protection Rule — Specific Path Beats General Path

When a Bind Mount covers a broad path (e.g. `/app`) AND an Anonymous Volume covers a nested path (e.g. `/app/node_modules`), the **more specific path wins** — the `node_modules` folder is preserved from the container image, while the rest of `/app` is overwritten by the host mount.

```bash
# Pattern: Bind Mount whole project, protect node_modules inside container
docker run \
  -v $(pwd):/app \          # Bind Mount → live sync host code into /app
  -v /app/node_modules \    # Anonymous Volume → protect /app/node_modules
  <image>
```

---

### Read-Only Volumes & Mounts

Add `:ro` to make a volume/mount **read-only** from the container's perspective (container can read but not write):

```bash
# Read-only Named Volume
docker run -v mydata:/app/data:ro <image>

# Read-only Bind Mount (container can't write to host files)
docker run -v $(pwd):/app:ro <image>
```

---

### Comparison Table

| Feature | Named Volume | Bind Mount | Anonymous Volume |
|---|---|---|---|
| **Syntax** | `-v name:/path` | `-v /host/path:/path` | `-v /path` |
| **Persistent** | ✅ Survives removal | ✅ Survives removal | ❌ Removed with container |
| **Location** | Managed by Docker | Managed by You | Managed by Docker |
| **Shareable** | ✅ Across containers | ✅ Across containers | ❌ Unique to one |
| **Defined in Dockerfile** | ❌ | ❌ | ✅ (`VOLUME ["/path"]`) |
| **Typical Use** | Persist DB / logs | Live sync source code | Protect internal paths |

---

### Volume Commands

| Command | Description |
|---|---|
| `docker volume create <name>` | Create a new Named Volume |
| `docker volume ls` | List all Named Volumes |
| `docker volume inspect <name>` | Detailed info about a volume (path, driver, etc.) |
| `docker volume rm <name>` | Delete a specific Named Volume |
| `docker volume prune` | Remove all **unused** volumes |

---

# .dockerignore

The `.dockerignore` file tells Docker which files and folders to **exclude from the build context** when running `docker build`. This keeps images smaller and prevents sensitive files from being accidentally included.

- Lives in the **same directory as the Dockerfile**
- Uses the same glob syntax as `.gitignore`
- Docker reads it before sending the build context to the daemon

### Why it matters

Without `.dockerignore`, every file in the project directory is sent to the Docker daemon — including `node_modules`, `.env`, `.git`, logs, etc. This can:
- Massively slow down builds
- Bloat image size
- Expose secrets or credentials

### Common patterns

```
# Dependencies (let the container install them)
node_modules
vendor

# Build artifacts
dist
build
*.o
*.out

# Git history
.git
.gitignore

# Secrets / local config
.env
*.pem
*.key
secrets/

# Docker files themselves
Dockerfile
.dockerignore

# Logs and temp files
*.log
tmp/
.DS_Store
```

### Example: Node.js `.dockerignore`

```
node_modules
npm-debug.log
.git
.env
dist
.DS_Store
```

> **Rule of thumb:** Start from `.gitignore` and add anything else that shouldn't go into the image (like secrets or build outputs the container doesn't need).

---

# ARG and ENV — Build-time vs Runtime Variables

| Feature | `ARG` | `ENV` |
|---|---|---|
| **Set at** | Build time only | Runtime (persists in image) |
| **Available in** | Dockerfile only | Dockerfile + running container |
| **Passed via** | `docker build --build-arg` | `docker run -e` / `--env-file` |
| **Visible in image** | ❌ Not stored in final image | ✅ Stored in image metadata |
| **Use case** | Build configuration (e.g. Node version) | App config (e.g. PORT, DB_URL) |

---

### ENV — Runtime Environment Variables

Set in Dockerfile, available in the container at runtime:

```Dockerfile
FROM node
WORKDIR /app

# Set default values
ENV PORT=80
ENV NODE_ENV=production

COPY . .
RUN npm install
EXPOSE $PORT          # can use ENV vars in Dockerfile too
CMD ["node", "server.js"]
```

Override at runtime with `docker run`:

```bash
# Pass a single env variable
docker run -e PORT=3000 <image>

# Pass multiple env variables
docker run -e PORT=3000 -e NODE_ENV=development <image>

# Load from a file (recommended for secrets)
docker run --env-file ./.env <image>
```

`.env` file format:
```
PORT=3000
NODE_ENV=development
DB_URL=mongodb://localhost:27017/mydb
```

---

### ARG — Build-time Arguments

`ARG` values are only available **during the build**, not in the running container:

```Dockerfile
FROM node

# Declare ARG with an optional default
ARG NODE_ENV=production
ARG APP_VERSION=1.0.0

# Use ARG during build
RUN echo "Building version $APP_VERSION in $NODE_ENV mode"

WORKDIR /app
COPY . .
RUN npm install
CMD ["node", "server.js"]
```

Pass values at build time:

```bash
# Pass a single build arg
docker build --build-arg NODE_ENV=development .

# Pass multiple build args
docker build --build-arg NODE_ENV=staging --build-arg APP_VERSION=2.1.0 -t myapp .
```

### Combining ARG + ENV

A common pattern is using `ARG` to set an `ENV` (making the value available at both build AND runtime):

```Dockerfile
ARG NODE_ENV=production
ENV NODE_ENV=$NODE_ENV     # ARG feeds into ENV
```

```bash
docker build --build-arg NODE_ENV=development -t myapp .
# NODE_ENV is now "development" both at build time AND in the running container
```

> ⚠️ **Security Warning:** `ENV` values are stored in the image and visible via `docker image inspect`. Never use `ENV` for secrets like API keys or passwords — use `--env-file` at runtime or Docker Secrets instead.

---

# Dockerfile Examples

### 1. Node.js Web App

```Dockerfile
FROM node:18-alpine              # use slim Alpine-based image

WORKDIR /app

COPY package*.json ./            # copy manifests first (layer cache optimization)
RUN npm ci --only=production     # install only production deps

COPY . .                         # copy rest of source

ARG PORT=80
ENV PORT=$PORT

EXPOSE $PORT
CMD ["node", "server.js"]
```

```bash
docker build -t myapp .
docker run -p 3000:80 --rm myapp
```

---

### 2. Python Flask App

```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt   # no-cache keeps image small

COPY . .

ENV FLASK_ENV=production
ENV PORT=5000

EXPOSE 5000
CMD ["python", "app.py"]
```

```bash
docker build -t flask-app .
docker run -p 5000:5000 -e FLASK_ENV=development flask-app
```

---

### 3. Multi-Stage Build (Node.js — Build then Serve)

Multi-stage builds produce a tiny final image by discarding the build tools:

```Dockerfile
# --- Stage 1: Build ---
FROM node:18 AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build             # output goes to /app/dist

# --- Stage 2: Serve ---
FROM nginx:alpine             # only the lightweight nginx image
COPY --from=builder /app/dist /usr/share/nginx/html   # copy only the build output
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

```bash
docker build -t my-frontend .
docker run -p 8080:80 my-frontend
```

> The final image only contains nginx + the compiled static files — no Node.js, no source code, no `node_modules`.

---

### 4. Development Setup — Live Sync with Bind Mount + Volume

```Dockerfile
FROM node:18

WORKDIR /app

COPY package*.json ./
RUN npm install              # installed into container's node_modules

COPY . .

EXPOSE 3000
CMD ["npm", "run", "dev"]   # dev server with hot reload
```

```bash
# Bind Mount host code → /app (live sync)
# Anonymous Volume → protect /app/node_modules from being overwritten
docker run -p 3000:3000 \
  -v $(pwd):/app \
  -v /app/node_modules \
  --rm myapp-dev
```

---

### 5. App with Named Volume (Persistent Data)

```Dockerfile
FROM mongo:6

ENV MONGO_INITDB_ROOT_USERNAME=admin
ENV MONGO_INITDB_ROOT_PASSWORD=secret

EXPOSE 27017
```

```bash
# Create a named volume so data survives container removal
docker volume create mongo-data

docker run -d \
  -p 27017:27017 \
  -v mongo-data:/data/db \
  --name mongodb \
  mongo:6
```

---

# Networks & Container Communication

### Why Multi-Container Apps?

In real applications, you often need **more than one container** running simultaneously. There are two main reasons:

1. **Single-responsibility principle** — it's best practice to have each container focus on **one main task** (e.g. one container for the web server, another for the database)
2. **Practical difficulty** — it's very hard to configure a container that reliably does more than one "main thing"

So multi-container setups are the norm. But when containers are split up, they often need to **talk to each other** — or to the outside world.

There are **three communication scenarios** in Docker:

| Scenario | Target | How |
|---|---|---|
| Container → Internet (WWW) | External APIs / websites | Works out of the box |
| Container → Host Machine | Local DB / services on your laptop | Use `host.docker.internal` |
| Container → Container | Another Docker container | Use a Docker Network |

---

### 1. 🌐 Communicating with the World Wide Web (WWW)

Containers can send HTTP requests to external servers **without any configuration**. It just works.

```js
// Inside your container — this works perfectly
fetch('https://some-api.com/my-data').then(...)
```

> ✅ No extra setup needed. The container has internet access by default.

---

### 2. 🖥️ Communicating with the Host Machine

You might need your container to reach a service running **on your laptop** — for example, a local development database.

**The problem:** Inside a container, `localhost` refers to the **container itself**, NOT your actual host machine.

```js
// ❌ This FAILS inside a container
fetch('localhost:3000/demo').then(...)
```

**The fix:** Use the special hostname `host.docker.internal` — Docker automatically translates this to the IP address of your host machine.

```js
// ✅ This works inside a container
fetch('host.docker.internal:3000/demo').then(...)
```

> 🔍 **How it works:** Docker does **not** change your source code. It detects outgoing requests and resolves the IP for `host.docker.internal` at runtime.

> 💡 **When is this useful?** Mainly during **development** — when you have a database or another service running locally on your machine, not in a container.

---

### 3. 📦 Communicating with Other Containers

When you need containers to talk to each other (e.g., a web app container talking to a database container), you have two options:

| Option | How | Problem |
|---|---|---|
| Option 1 | Manually find the other container's IP | IP can change — not reliable |
| Option 2 | Use a **Docker Network** | ✅ Best approach — Docker resolves IPs automatically |

#### How Docker Networks Work

When two or more containers are on the **same Docker network**, they can reach each other simply by using the **container name** as the hostname. Docker handles IP resolution automatically.

```
┌─────────────────────────────────────────┐
│             Docker Network              │
│                                         │
│  ┌───────────┐       ┌───────────────┐  │
│  │  cont1    │ ←───→ │    cont2      │  │
│  │ (web app) │       │  (database)   │  │
│  └───────────┘       └───────────────┘  │
│                                         │
│  Containers can reach each other by     │
│  name: fetch('cont2/my-data')           │
└─────────────────────────────────────────┘
```

#### Setting Up a Docker Network

**Step 1 — Create the network:**
```bash
docker network create my-network
```

**Step 2 — Attach containers to that network:**
```bash
docker run --network my-network --name cont1 my-image
docker run --network my-network --name cont2 my-other-image
```

**Step 3 — Use the container name as the address in your code:**
```js
// Inside cont1 — talking to cont2 by name
fetch('cont2/my-data').then(...)
```

> 🔍 **How it works:** Docker detects the outgoing request and resolves `cont2` to its IP address automatically. It does **not** change your source code — it resolves at the network level.

---

### Summary — All Three Communication Types

```
┌─────────────────────────────────────────────────────────┐
│                Your Container (App)                     │
└────────────┬──────────────────┬──────────────┬──────────┘
             │                  │              │
             ▼                  ▼              ▼
   ┌──────────────────┐ ┌──────────────┐ ┌──────────────────┐
   │  Internet / WWW  │ │ Host Machine │ │ Other Containers │
   │                  │ │              │ │                  │
   │ Works out of box │ │ Use:         │ │ Use Docker       │
   │ No config needed │ │ host.docker  │ │ Networks +       │
   │                  │ │ .internal    │ │ container names  │
   └──────────────────┘ └──────────────┘ └──────────────────┘
```

---

### Network Commands

| Command | Description |
|---|---|
| `docker network create <name>` | Create a new Docker network |
| `docker network ls` | List all Docker networks |
| `docker network inspect <name>` | Inspect a network (see connected containers, IPs, etc.) |
| `docker network rm <name>` | Remove a network |
| `docker network prune` | Remove all unused networks |
| `docker run --network <name> ...` | Attach a container to a specific network |
| `docker network connect <network> <container>` | Connect a running container to a network |
| `docker network disconnect <network> <container>` | Disconnect a container from a network |

---

### Default Networks

Docker automatically creates some networks:

| Network | Driver | Description |
|---|---|---|
| `bridge` | bridge | Default network for containers — isolated from host |
| `host` | host | Container shares the host's network stack directly |
| `none` | null | No networking — fully isolated container |

> 💡 When you run a container without `--network`, it joins the default `bridge` network. But containers on the **default** bridge cannot reach each other by name — you need a **custom network** for that.

---

### Real-World Example — Node App + MongoDB

```bash
# Step 1: Create a shared network
docker network create app-network

# Step 2: Start MongoDB on the network
docker run -d \
  --name mongodb \
  --network app-network \
  -v mongo-data:/data/db \
  mongo:6

# Step 3: Start the Node.js app on the same network
docker run -d \
  --name nodeapp \
  --network app-network \
  -p 3000:3000 \
  my-node-app
```

Inside the Node.js app, connect to MongoDB using the container name:

```js
// Use 'mongodb' (the container name) as the host
mongoose.connect('mongodb://mongodb:27017/mydb')
```

> ✅ Docker resolves `mongodb` to the correct container IP automatically — no hardcoded IPs needed.