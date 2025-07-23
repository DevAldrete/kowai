#!/bin/bash
# KowAI Backend - Docker Swarm Development Deployment Script
# Usage: ./scripts/deployment/deploy-swarm-dev.sh

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
STACK_NAME="kowai-dev"
COMPOSE_FILE="docker-swarm-dev.yml"
NETWORK_NAME="kowai-network"

# Functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_prerequisites() {
    log_info "Checking prerequisites..."
    
    # Check if Docker is running
    if ! docker info >/dev/null 2>&1; then
        log_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    
    # Check if Docker Swarm is initialized
    if ! docker node ls >/dev/null 2>&1; then
        log_warning "Docker Swarm is not initialized. Initializing now..."
        docker swarm init
        log_success "Docker Swarm initialized."
    fi
    
    # Check if compose file exists
    if [ ! -f "$COMPOSE_FILE" ]; then
        log_error "Docker Compose file '$COMPOSE_FILE' not found!"
        exit 1
    fi
    
    log_success "Prerequisites check completed."
}

create_volumes() {
    log_info "Creating persistent volumes..."
    
    # Create volume directories
    mkdir -p volumes/{mariadb,redis,prefect}
    
    # Set proper permissions
    sudo chown -R 999:999 volumes/mariadb 2>/dev/null || true
    sudo chown -R 999:999 volumes/redis 2>/dev/null || true
    sudo chown -R 1000:1000 volumes/prefect 2>/dev/null || true
    
    log_success "Volumes created and configured."
}

setup_environment() {
    log_info "Setting up environment..."
    
    # Copy environment file if it doesn't exist
    if [ ! -f .env ]; then
        if [ -f .env.example ]; then
            cp .env.example .env
            log_warning "Created .env file from .env.example. Please update it with your configuration."
        else
            log_warning "No .env file found. Using environment variables from compose file."
        fi
    fi
    
    log_success "Environment setup completed."
}

build_images() {
    log_info "Building Docker images..."
    
    # Build the backend image
    docker build -t kowai/backend:dev .
    
    log_success "Images built successfully."
}

deploy_stack() {
    log_info "Deploying Docker Swarm stack '$STACK_NAME'..."
    
    # Deploy the stack
    docker stack deploy -c "$COMPOSE_FILE" "$STACK_NAME"
    
    log_success "Stack '$STACK_NAME' deployed successfully."
}

wait_for_services() {
    log_info "Waiting for services to become healthy..."
    
    local max_attempts=60
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        local healthy_services=$(docker service ls --filter label=com.docker.stack.namespace="$STACK_NAME" --format "table {{.Name}}\t{{.Replicas}}" | grep -c "1/1" || true)
        local total_services=$(docker service ls --filter label=com.docker.stack.namespace="$STACK_NAME" --format "table {{.Name}}" | wc -l)
        total_services=$((total_services - 1)) # Remove header line
        
        if [ "$healthy_services" -eq "$total_services" ]; then
            log_success "All services are healthy!"
            break
        fi
        
        log_info "Waiting... ($healthy_services/$total_services services healthy)"
        sleep 10
        attempt=$((attempt + 1))
    done
    
    if [ $attempt -eq $max_attempts ]; then
        log_warning "Timeout waiting for all services to become healthy. Check service status manually."
    fi
}

show_status() {
    log_info "Deployment Status:"
    echo
    docker stack services "$STACK_NAME"
    echo
    log_info "Access URLs:"
    echo -e "${GREEN}Backend API:${NC} http://localhost:8000"
    echo -e "${GREEN}API Documentation:${NC} http://localhost:8000/docs"
    echo -e "${GREEN}Prefect UI:${NC} http://localhost:4200"
    echo -e "${GREEN}Traefik Dashboard:${NC} http://localhost:8080"
    echo -e "${GREEN}Redis Commander:${NC} http://localhost:8081"
    echo
    log_info "Useful Commands:"
    echo "  View logs: docker service logs ${STACK_NAME}_kowai-backend -f"
    echo "  Scale service: docker service scale ${STACK_NAME}_kowai-backend=3"
    echo "  Remove stack: docker stack rm $STACK_NAME"
    echo "  List services: docker stack services $STACK_NAME"
}

main() {
    log_info "Starting KowAI Backend Docker Swarm deployment..."
    
    check_prerequisites
    create_volumes
    setup_environment
    build_images
    deploy_stack
    wait_for_services
    show_status
    
    log_success "Deployment completed successfully!"
}

# Handle script interruption
trap 'log_error "Deployment interrupted!"; exit 1' INT TERM

# Run main function
main "$@"