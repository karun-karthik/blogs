## Why Docker?

- Containers bundle all steps and dependencies required to run an application.
- They provide a consistent runtime, simplifying deployment across environments.
- Additional benefits include portability, scalability, and resource efficiency.

## What is a Container?

- A Docker container image is a lightweight standalone, executable package of software that includes everything needed to run an application.
- History?

### Open Container Initiative (OCI)

- The OCI is an open governance structure for the express purpose of creating open industry standards around container formats and runtimes, this is a major player in container space before Docker.
- This helps in
    - Runtime specification
    - Image specification
    - Distribution specification

## Evolution of Virtualization

### Bare Metal

- Tightly coupled dependencies leading to conflicts
- Inefficient memory utilization
- Large blast radius
- Slow boot-up & shut-down speed, could take upto few minutes at minimum.
- Very slow provisioning & decommissioning
- Add image from Excalidraw

### Virtual Machine

- No dependency conflicts
- Better utilization
- Small blast radius
- Faster startup & shut-down speed, could take upto few minutes at max
- Faster provisioning & decommissioning
- Ex. AWS Nitro System, VmWare vSphere, Microsoft Hyper-V, VirtualBox

### Containers

- No dependency conflicts
- Even better utilization
- Smaller blast radius
- Faster startup & shutdown speed, in seconds.
- Faster provisioning & decommissioning
- Lightweight in nature
- Desktop container platforms – Docker, Podman, etc.
- Runtime engines – containerd, CRI‑O, runc, etc.

## Technology Overview

The core of the container involves the following:
1. Namespaces
2. Control Groups - CGroups
3. Union Filesystem

## Namespaces

### What Are Linux Namespaces?

Kernel-level isolation that virtualizes global system resources per process group.

### What Do They Isolate?

- PID Namespace → Separate process IDs
- Network Namespace → Own IP, interfaces, routing
- Mount Namespace → Independent filesystem view
- UTS Namespace → Unique hostname
- IPC Namespace → Isolated shared memory & queues
- User Namespace → UID/GID mapping (root inside ≠ root outside)
- Cgroup Namespace → Resource visibility isolation
- Time Namespace → Independent clock offsets

### How Containers Use Them

When you run a container:

1. A process is created
2. New namespaces are assigned
3. Resource limits applied via cgroups
4. Capabilities are reduced

## Control Groups (CGroups)

Linux cgroups (Control Groups) are a kernel feature that limit and monitor how much CPU, memory, disk I/O, and other resources a group of processes can use. While namespaces provide isolation, cgroups provide resource control. Container platforms like Docker and Kubernetes use cgroups to ensure each container gets defined resource limits, preventing one workload from exhausting the host system.

### What Are Linux Cgroups?

Kernel mechanism to limit, prioritize, account, and isolate resource usage of process groups.

### What Do Cgroups Control?

- CPU → Limit usage, set shares, throttle cores
- Memory → Hard/soft limits, OOM control
- Block I/O → Disk read/write throttling
- Network (via tc integration) → Bandwidth control
- PIDs → Limit number of processes
- Accounting → Track resource consumption

### How Containers Use Cgroups

When you run:

```bash
docker run --memory=512m --cpus=1 nginx
```

Behind the scenes:

- A cgroup is created
- Memory limit = 512 MB
- CPU quota applied
- Kernel enforces limits
- If memory exceeds limit → OOM kill
- If CPU exceeds quota → Throttled

### Namespaces vs Cgroups

| Feature | Namespaces | Cgroups |
|---------|-----------|---------|
| Purpose | Isolation | Resource control |
| View | Virtual view of system | Enforced limits |
| Effect | Hide other processes | Prevent resource abuse |
| Meaning | "Who you see" | "How much you can use" |

### Cgroups v1 vs v2

| Feature | v1 | v2 |
|---------|----|----|
| Controllers | Separate hierarchies | Unified hierarchy |
| Complexity | Higher | Simpler |
| Modern distros | Legacy | Default |

Most modern Linux distributions use cgroup v2.



## Union Mount Filesystems

A Union Mount Filesystem merges multiple directories (layers) into a single unified view. **OverlayFS** is the most widely used implementation and is the foundation of container image layering.

### How It Works

```
Lowerdir (read-only image layers)
         +
Upperdir (writable container layer)
         =
Merged (unified view)
```

When a container modifies a file from the lower layer, it's copied to the upper layer first (Copy-on-Write), keeping original layers untouched.

### Why It Matters

- **Disk efficiency**: Layers shared across containers and images
- **Fast startup**: No need to copy entire image
- **Layer caching**: Reuse unchanged layers in builds
- **Image distribution**: Smaller, more efficient transfers

### Example

```dockerfile
FROM ubuntu
RUN apt install nginx
COPY . /app
```

Each instruction creates a new read-only layer. OverlayFS stacks them, and Docker adds a writable layer on top for container changes.

### OverlayFS vs Traditional Filesystem

| Feature | Traditional | OverlayFS |
|---------|-----------|-----------|
| Structure | Single directory | Layered directories |
| Writes | Direct | Copy-on-write |
| Reusability | No layer sharing | Shared read-only layers |
| Efficiency | Lower | Higher |

### OverlayFS Core Components

A convenient reference to the four directories that OverlayFS uses internally. understanding these is helpful when reasoning about how layers are stacked and where changes actually live.

- 📦 **Lowerdir** → read-only layers (base image layers) that make up the immutable portion of an image.
- ✏️ **Upperdir** → the writable overlay where all container modifications are recorded; new files are created here and modified files are copied up into it.
- 🔀 **Workdir** → an internal workspace used by the kernel for bookkeeping during operations such as copy-on-write, not visible to container processes.
- 👀 **Merged** → the final unified view that container processes interact with; it presents the combination of lower and upper directories according to overlay rules.

OverlayFS stacks the immutable lower layers, applies any modifications in the upper layer, keeps temporary state in the workdir, and exposes the combined filesystem at the merged mount point.

### Docker Components & Flow

**Core stack (Linux native)**

- **Docker CLI** → user‑facing client
- **dockerd** (daemon / manager) → controls API, lifecycle, networking
- **containerd** (runtime manager) → supervises containers
- **runc** (OCI runtime) → spawns containers using kernel syscalls
- **Linux kernel** → enforces isolation & limits via namespaces, cgroups, overlayFS, capabilities

**Responsibilities**

| Component    | Role                                     | Mnemonic        |
|--------------|------------------------------------------|-----------------|
| Docker CLI   | Sends commands to the daemon            | Client          |
| dockerd      | Manages high‑level features & API        | Manager         |
| containerd   | Handles container lifecycle             | Runtime Manager |
| runc         | Executes containers via kernel           | Executor        |
| Linux kernel | Provides the actual isolation & control  | Infrastructure  |

**Execution flow (`docker run nginx`)**

1. CLI sends a REST request to dockerd.
2. dockerd validates the request and coordinates with containerd.
3. containerd prepares the container bundle.
4. `runc`:
   - creates the necessary namespaces,
   - sets up cgroups,
   - mounts the overlay filesystem,
   - starts the container process.
5. The kernel then executes and isolates the process.

**Docker Desktop vs native engine**

On **Linux hosts** the engine runs directly:

```
Linux host → Docker Engine → Containers
```

On **macOS/Windows**, a lightweight Linux VM is introduced:

```
Host OS → Linux VM → Docker Engine → Containers
```

Docker Desktop packages the engine inside that VM (WSL2 or Apple framework).

| Feature         | Docker Engine       | Docker Desktop           |
|-----------------|---------------------|--------------------------|
| Runtime         | Native on Linux     | Inside a VM              |
| Typical use     | Production servers  | Developer machines       |
| Hypervisor      | None                | Required (WSL2/Hyperkit) |

**Five key points to remember**

1. The **Linux kernel** provides isolation, not Docker itself.
2. `runc` interacts directly with the kernel.
3. `containerd` manages container lifecycle.
4. `dockerd` adds orchestration, networking, and API features.
5. Docker Desktop simply adds a Linux VM layer to the stack.