#!/bin/bash
# KowAI Backend - Kubernetes Production Deployment Script
# Usage: ./scripts/deployment/deploy-k8s-prod.sh [apply|destroy|status]

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
NAMESPACE="kowai"
KUSTOMIZE_DIR="k8s/production"
TIMEOUT="600s"

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
    
    # Check if kubectl is available
    if ! command -v kubectl &> /dev/null; then
        log_error "kubectl is not installed or not in PATH"
        exit 1
    fi
    
    # Check if kustomize is available
    if ! command -v kustomize &> /dev/null; then
        log_error "kustomize is not installed or not in PATH"
        exit 1
    fi
    
    # Check cluster connection
    if ! kubectl cluster-info &> /dev/null; then
        log_error "Cannot connect to Kubernetes cluster"
        exit 1
    fi
    
    # Check if kustomization file exists
    if [ ! -f "$KUSTOMIZE_DIR/kustomization.yaml" ]; then
        log_error "Kustomization file not found in $KUSTOMIZE_DIR"
        exit 1
    fi
    
    log_success "Prerequisites check completed."
}

create_namespace() {
    log_info "Creating namespace '$NAMESPACE'..."
    
    if kubectl get namespace "$NAMESPACE" &> /dev/null; then
        log_info "Namespace '$NAMESPACE' already exists."
    else
        kubectl create namespace "$NAMESPACE"
        log_success "Namespace '$NAMESPACE' created."
    fi
}

setup_secrets() {
    log_info "Setting up secrets..."
    
    # Check if secrets directory exists
    local secrets_dir="$KUSTOMIZE_DIR/secrets"
    if [ ! -d "$secrets_dir" ]; then
        log_error "Secrets directory '$secrets_dir' not found!"
        log_error "Please create the secrets directory and add your secret files."
        exit 1
    fi
    
    # Warn about placeholder values
    if grep -r "CHANGE_ME" "$secrets_dir" &> /dev/null; then
        log_warning "Found placeholder values in secrets. Please update with actual values."
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi
    
    log_success "Secrets setup completed."
}

validate_manifests() {
    log_info "Validating Kubernetes manifests..."
    
    # Build and validate manifests
    if ! kustomize build "$KUSTOMIZE_DIR" | kubectl apply --dry-run=client -f - &> /dev/null; then
        log_error "Manifest validation failed!"
        exit 1
    fi
    
    log_success "Manifests validated successfully."
}

deploy_application() {
    log_info "Deploying KowAI Backend to Kubernetes..."
    
    # Apply manifests
    kustomize build "$KUSTOMIZE_DIR" | kubectl apply -f -
    
    log_success "Application deployed successfully."
}

wait_for_deployment() {
    log_info "Waiting for deployment to complete..."
    
    # Wait for deployments
    local deployments=("mariadb" "redis" "prefect-server" "kowai-backend")
    
    for deployment in "${deployments[@]}"; do
        log_info "Waiting for deployment '$deployment'..."
        if kubectl wait --for=condition=available --timeout="$TIMEOUT" "deployment/$deployment" -n "$NAMESPACE"; then
            log_success "Deployment '$deployment' is ready."
        else
            log_error "Deployment '$deployment' failed to become ready within timeout."
            return 1
        fi
    done
    
    log_success "All deployments are ready!"
}

check_health() {
    log_info "Checking application health..."
    
    # Get backend service endpoint
    local backend_port=$(kubectl get service kowai-backend-service -n "$NAMESPACE" -o jsonpath='{.spec.ports[0].port}')
    
    # Port forward to check health (temporary)
    kubectl port-forward service/kowai-backend-service "$backend_port:$backend_port" -n "$NAMESPACE" &
    local port_forward_pid=$!
    
    # Wait a moment for port forward to establish
    sleep 5
    
    # Check health endpoint
    if curl -f "http://localhost:$backend_port/health" &> /dev/null; then
        log_success "Application health check passed!"
    else
        log_warning "Application health check failed. Check logs for details."
    fi
    
    # Kill port forward
    kill $port_forward_pid 2>/dev/null || true
}

show_status() {
    log_info "Deployment Status:"
    echo
    kubectl get all -n "$NAMESPACE"
    echo
    log_info "Ingress Status:"
    kubectl get ingress -n "$NAMESPACE"
    echo
    log_info "Useful Commands:"
    echo "  View pods: kubectl get pods -n $NAMESPACE"
    echo "  View logs: kubectl logs -f deployment/kowai-backend -n $NAMESPACE"
    echo "  Scale deployment: kubectl scale deployment kowai-backend --replicas=5 -n $NAMESPACE"
    echo "  Port forward: kubectl port-forward service/kowai-backend-service 8000:8000 -n $NAMESPACE"
    echo "  Delete deployment: kubectl delete -k $KUSTOMIZE_DIR"
}

destroy_application() {
    log_info "Destroying KowAI Backend deployment..."
    
    # Delete application
    kustomize build "$KUSTOMIZE_DIR" | kubectl delete -f - --ignore-not-found=true
    
    # Wait for pods to terminate
    log_info "Waiting for pods to terminate..."
    kubectl wait --for=delete pods --all -n "$NAMESPACE" --timeout="$TIMEOUT" || true
    
    # Delete namespace
    read -p "Delete namespace '$NAMESPACE'? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        kubectl delete namespace "$NAMESPACE" --ignore-not-found=true
        log_success "Namespace '$NAMESPACE' deleted."
    fi
    
    log_success "Application destroyed successfully."
}

show_help() {
    echo "Usage: $0 [COMMAND]"
    echo
    echo "Commands:"
    echo "  apply    Deploy the application to Kubernetes (default)"
    echo "  destroy  Remove the application from Kubernetes"
    echo "  status   Show current deployment status"
    echo "  help     Show this help message"
    echo
    echo "Examples:"
    echo "  $0 apply     # Deploy application"
    echo "  $0 status    # Show status"
    echo "  $0 destroy   # Remove application"
}

main() {
    local action="${1:-apply}"
    
    case "$action" in
        apply)
            log_info "Starting KowAI Backend Kubernetes deployment..."
            check_prerequisites
            create_namespace
            setup_secrets
            validate_manifests
            deploy_application
            wait_for_deployment
            check_health
            show_status
            log_success "Deployment completed successfully!"
            ;;
        destroy)
            log_warning "This will destroy the KowAI Backend deployment!"
            read -p "Are you sure? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                destroy_application
            else
                log_info "Deployment destruction cancelled."
            fi
            ;;
        status)
            check_prerequisites
            show_status
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            log_error "Unknown command: $action"
            show_help
            exit 1
            ;;
    esac
}

# Handle script interruption
trap 'log_error "Script interrupted!"; exit 1' INT TERM

# Run main function
main "$@"