# KowAI Backend - Updated Deployment Documentation

## Overview

This document provides comprehensive deployment instructions for the KowAI Backend using Docker Swarm for development and Kubernetes for production environments.

## Deployment Environments

### Development Environment: Docker Swarm
- **Purpose**: Local development, testing, and staging
- **Orchestration**: Docker Swarm
- **Configuration**: `docker-swarm-dev.yml`
- **Features**: Hot reload, debugging, easy scaling

### Production Environment: Kubernetes
- **Purpose**: Production deployment
- **Orchestration**: Kubernetes
- **Configuration**: Kustomize manifests in `k8s/`
- **Features**: High availability, auto-scaling, monitoring

## Prerequisites

### General Requirements
- Docker 20.10+ with Docker Compose v2
- Git
- Basic knowledge of containerization

### Development (Docker Swarm)
- Docker Swarm mode enabled
- 8GB+ RAM recommended
- Ports 80, 3306, 4200, 6379, 8000, 8080, 8081 available

### Production (Kubernetes)
- Kubernetes cluster (1.25+)
- kubectl configured
- kustomize installed
- NGINX Ingress Controller
- cert-manager (for SSL certificates)
- Storage class configured

## Development Deployment (Docker Swarm)

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd kowai/backend
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Deploy using script**:
   ```bash
   ./scripts/deployment/deploy-swarm-dev.sh
   ```

### Manual Deployment

1. **Initialize Docker Swarm** (if not already done):
   ```bash
   docker swarm init
   ```

2. **Create persistent volumes**:
   ```bash
   mkdir -p volumes/{mariadb,redis,prefect}
   sudo chown -R 999:999 volumes/mariadb
   sudo chown -R 999:999 volumes/redis
   sudo chown -R 1000:1000 volumes/prefect
   ```

3. **Build the application image**:
   ```bash
   docker build -t kowai/backend:dev .
   ```

4. **Deploy the stack**:
   ```bash
   docker stack deploy -c docker-swarm-dev.yml kowai-dev
   ```

5. **Monitor deployment**:
   ```bash
   docker stack services kowai-dev
   ```

### Accessing Services

| Service | URL | Description |
|---------|-----|-------------|
| Backend API | http://localhost:8000 | Main API endpoints |
| API Documentation | http://localhost:8000/docs | Swagger UI |
| Prefect UI | http://localhost:4200 | Workflow management |
| Traefik Dashboard | http://localhost:8080 | Load balancer UI |
| Redis Commander | http://localhost:8081 | Redis management |

### Management Commands

```bash
# View service status
docker stack services kowai-dev

# View logs
docker service logs kowai-dev_kowai-backend -f

# Scale services
docker service scale kowai-dev_kowai-backend=3

# Update service
docker service update --image kowai/backend:latest kowai-dev_kowai-backend

# Remove stack
docker stack rm kowai-dev
```

### Development Features

#### Hot Reload
The development setup includes volume mounting for hot reload:
```yaml
volumes:
  - ./app:/app/app:ro
```

#### Service Scaling
Easily scale services for load testing:
```bash
# Scale backend to 5 replicas
docker service scale kowai-dev_kowai-backend=5

# Scale Prefect workers
docker service scale kowai-dev_prefect-worker=3
```

#### Load Balancing
Traefik provides automatic load balancing and service discovery.

## Production Deployment (Kubernetes)

### Cluster Requirements

#### Minimum Resources
- **CPU**: 8 cores
- **Memory**: 16GB RAM
- **Storage**: 100GB+ with fast SSD
- **Nodes**: 3+ nodes for high availability

#### Required Add-ons
- NGINX Ingress Controller
- cert-manager for SSL certificates
- Prometheus + Grafana (monitoring)
- Storage provisioner

### Quick Start

1. **Prepare secrets**:
   ```bash
   cd k8s/production/secrets
   # Update all secret files with production values
   echo "your-database-url" > database-url
   echo "your-secret-key" > secret-key
   # ... update other secrets
   ```

2. **Deploy using script**:
   ```bash
   ./scripts/deployment/deploy-k8s-prod.sh apply
   ```

3. **Check status**:
   ```bash
   ./scripts/deployment/deploy-k8s-prod.sh status
   ```

### Manual Deployment

1. **Create namespace**:
   ```bash
   kubectl create namespace kowai
   ```

2. **Deploy application**:
   ```bash
   kustomize build k8s/production | kubectl apply -f -
   ```

3. **Wait for deployment**:
   ```bash
   kubectl wait --for=condition=available --timeout=600s deployment/kowai-backend -n kowai
   ```

4. **Verify deployment**:
   ```bash
   kubectl get all -n kowai
   ```

### Configuration Management

#### Secrets Management
Production secrets are managed via Kubernetes secrets:

```bash
# Update database password
kubectl create secret generic kowai-secrets \
  --from-literal=DATABASE_URL="mysql+aiomysql://user:newpass@host:3306/db" \
  -n kowai --dry-run=client -o yaml | kubectl apply -f -
```

#### ConfigMaps
Environment-specific configuration:

```bash
# Update configuration
kubectl create configmap kowai-config \
  --from-literal=LOG_LEVEL="WARNING" \
  --from-literal=DEBUG="false" \
  -n kowai --dry-run=client -o yaml | kubectl apply -f -
```

### Scaling and High Availability

#### Horizontal Pod Autoscaling
Automatic scaling based on CPU/memory usage:

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: kowai-backend-hpa
spec:
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

#### Manual Scaling
```bash
# Scale backend pods
kubectl scale deployment kowai-backend --replicas=5 -n kowai

# Scale Prefect workers
kubectl scale deployment prefect-worker --replicas=8 -n kowai
```

#### Pod Disruption Budget
Ensures minimum availability during updates:

```yaml
apiVersion: policy/v1
kind: PodDisruptionBudget
metadata:
  name: kowai-backend-pdb
spec:
  minAvailable: 2
  selector:
    matchLabels:
      app.kubernetes.io/name: kowai-backend
```

### Monitoring and Observability

#### Health Checks
All services include comprehensive health checks:

- **Liveness Probe**: Restart unhealthy containers
- **Readiness Probe**: Route traffic only to ready containers
- **Startup Probe**: Allow extra time for initialization

#### Prometheus Metrics
Automatic metrics collection:

```bash
# Access metrics
kubectl port-forward service/kowai-backend-service 8000:8000 -n kowai
curl http://localhost:8000/metrics
```

#### Log Aggregation
Structured logging with correlation IDs for distributed tracing.

### Security Features

#### Network Policies
Restrict inter-pod communication:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: kowai-backend-netpol
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/name: kowai-backend
  policyTypes:
  - Ingress
  - Egress
```

#### Security Context
Non-root containers with minimal privileges:

```yaml
securityContext:
  allowPrivilegeEscalation: false
  runAsNonRoot: true
  runAsUser: 1000
  readOnlyRootFilesystem: true
```

#### RBAC
Role-based access control for service accounts.

### SSL/TLS Configuration

#### cert-manager Integration
Automatic SSL certificate management:

```yaml
metadata:
  annotations:
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
spec:
  tls:
  - hosts:
    - api.kowai.com
    secretName: kowai-tls
```

### Backup and Disaster Recovery

#### Database Backup
Automated MariaDB backups:

```bash
# Create backup job
kubectl create job --from=cronjob/mariadb-backup mariadb-backup-manual -n kowai
```

#### Persistent Volume Backup
Use your cloud provider's volume snapshot features.

## Management Commands

### Development (Docker Swarm)

```bash
# Deploy stack
./scripts/deployment/deploy-swarm-dev.sh

# View services
docker stack services kowai-dev

# Scale service
docker service scale kowai-dev_kowai-backend=3

# View logs
docker service logs kowai-dev_kowai-backend -f

# Update service
docker service update --image kowai/backend:latest kowai-dev_kowai-backend

# Remove stack
docker stack rm kowai-dev
```

### Production (Kubernetes)

```bash
# Deploy application
./scripts/deployment/deploy-k8s-prod.sh apply

# Check status
./scripts/deployment/deploy-k8s-prod.sh status

# View pods
kubectl get pods -n kowai

# View logs
kubectl logs -f deployment/kowai-backend -n kowai

# Scale deployment
kubectl scale deployment kowai-backend --replicas=5 -n kowai

# Port forward for debugging
kubectl port-forward service/kowai-backend-service 8000:8000 -n kowai

# Execute commands in pod
kubectl exec -it deployment/kowai-backend -n kowai -- /bin/bash

# Destroy deployment
./scripts/deployment/deploy-k8s-prod.sh destroy
```

## Troubleshooting

### Common Issues

#### Docker Swarm

1. **Services not starting**:
   ```bash
   # Check service logs
   docker service logs kowai-dev_kowai-backend
   
   # Check service details
   docker service ps kowai-dev_kowai-backend --no-trunc
   ```

2. **Volume permissions**:
   ```bash
   # Fix volume permissions
   sudo chown -R 999:999 volumes/mariadb
   sudo chown -R 999:999 volumes/redis
   ```

3. **Port conflicts**:
   ```bash
   # Check port usage
   netstat -tulpn | grep :8000
   
   # Kill conflicting processes
   sudo lsof -ti:8000 | xargs kill -9
   ```

#### Kubernetes

1. **Pods not starting**:
   ```bash
   # Describe pod
   kubectl describe pod <pod-name> -n kowai
   
   # Check events
   kubectl get events -n kowai --sort-by='.lastTimestamp'
   ```

2. **Image pull issues**:
   ```bash
   # Check image pull secrets
   kubectl get secrets -n kowai
   
   # Debug image pull
   kubectl describe pod <pod-name> -n kowai
   ```

3. **Resource constraints**:
   ```bash
   # Check node resources
   kubectl top nodes
   
   # Check pod resources
   kubectl top pods -n kowai
   ```

4. **Storage issues**:
   ```bash
   # Check PVCs
   kubectl get pvc -n kowai
   
   # Check storage class
   kubectl get storageclass
   ```

### Debugging Commands

```bash
# Docker Swarm debugging
docker stack ps kowai-dev --no-trunc
docker service inspect kowai-dev_kowai-backend
docker node ls

# Kubernetes debugging
kubectl describe deployment kowai-backend -n kowai
kubectl get events -n kowai
kubectl logs -f deployment/kowai-backend -n kowai --previous
```

## Performance Optimization

### Docker Swarm

1. **Resource allocation**:
   ```yaml
   deploy:
     resources:
       limits:
         memory: 1GB
         cpus: '1.0'
       reservations:
         memory: 512MB
         cpus: '0.5'
   ```

2. **Placement constraints**:
   ```yaml
   deploy:
     placement:
       constraints:
         - node.role == worker
         - node.labels.performance == high
   ```

### Kubernetes

1. **Resource requests and limits**:
   ```yaml
   resources:
     requests:
       memory: "512Mi"
       cpu: "250m"
     limits:
       memory: "1Gi"
       cpu: "1000m"
   ```

2. **Node affinity**:
   ```yaml
   affinity:
     nodeAffinity:
       requiredDuringSchedulingIgnoredDuringExecution:
         nodeSelectorTerms:
         - matchExpressions:
           - key: kubernetes.io/instance-type
             operator: In
             values:
             - c5.xlarge
             - c5.2xlarge
   ```

## Security Best Practices

### Development
- Use development-specific secrets
- Enable debug logging
- Implement basic authentication
- Use HTTP for local development

### Production
- Use strong, unique secrets
- Enable audit logging
- Implement RBAC
- Use HTTPS everywhere
- Regular security updates
- Network policies
- Pod security standards

## Maintenance

### Regular Tasks

1. **Update dependencies**:
   ```bash
   # Update Python packages
   pip-audit
   
   # Update Docker images
   docker pull mariadb:10.11
   docker pull redis:7-alpine
   ```

2. **Monitor logs**:
   ```bash
   # Check error logs
   docker service logs kowai-dev_kowai-backend | grep ERROR
   kubectl logs deployment/kowai-backend -n kowai | grep ERROR
   ```

3. **Backup data**:
   ```bash
   # Database backup
   docker exec $(docker ps -q -f name=mariadb) mysqldump -u root -p kowai > backup.sql
   ```

### Updates and Rollbacks

#### Docker Swarm
```bash
# Update service
docker service update --image kowai/backend:v2.0 kowai-dev_kowai-backend

# Rollback service
docker service rollback kowai-dev_kowai-backend
```

#### Kubernetes
```bash
# Update deployment
kubectl set image deployment/kowai-backend kowai-backend=kowai/backend:v2.0 -n kowai

# Rollback deployment
kubectl rollout undo deployment/kowai-backend -n kowai

# Check rollout status
kubectl rollout status deployment/kowai-backend -n kowai
```

---

*This deployment documentation is maintained by the KowAI development team. For questions or contributions, please refer to our contribution guidelines.*