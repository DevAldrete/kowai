#!/usr/bin/env python3
"""
KowAI Universal Build System
Implements --api --persona-backend --c7 --seq build configuration
"""

import os
import sys
import subprocess
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import argparse


class KowAIBuildSystem:
    """Universal build system for KowAI project"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.backend_dir = project_root / "backend"
        self.frontend_dir = project_root / "frontend"
        self.dist_dir = project_root / "dist"
        self.build_dir = project_root / "build"
        
        # Build configuration
        self.config = {
            "api": True,
            "persona_backend": True,
            "c7_compression": True,
            "sequential_processing": True,
            "timestamp": datetime.utcnow().isoformat(),
            "features": []
        }
    
    def setup_directories(self):
        """Setup build directories"""
        print("📁 Setting up build directories...")
        
        # Remove existing build artifacts
        if self.dist_dir.exists():
            shutil.rmtree(self.dist_dir)
        if self.build_dir.exists():
            shutil.rmtree(self.build_dir)
        
        # Create fresh directories
        self.dist_dir.mkdir(exist_ok=True)
        self.build_dir.mkdir(exist_ok=True)
        
        print("  ✅ Build directories ready")
    
    def validate_environment(self):
        """Validate build environment"""
        print("🔍 Validating build environment...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version < (3, 12):
            raise RuntimeError("Python 3.12+ required")
        
        # Check uv
        if not shutil.which("uv"):
            raise RuntimeError("uv package manager not found. Install it with: curl -LsSf https://astral.sh/uv/install.sh | sh")
        else:
            try:
                result = subprocess.run(["uv", "--version"], capture_output=True, text=True)
                uv_version = result.stdout.strip()
                print(f"  ✅ uv: {uv_version}")
            except:
                print(f"  ⚠️ uv version check failed")
        
        # Check Node.js version (for frontend)
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            node_version = result.stdout.strip()
            print(f"  ✅ Node.js: {node_version}")
        except FileNotFoundError:
            print("  ⚠️ Node.js not found (frontend build will be skipped)")
        
        # Check required tools
        tools = ["git"]
        for tool in tools:
            if not shutil.which(tool):
                print(f"  ⚠️ {tool} not found")
            else:
                print(f"  ✅ {tool} available")
        
        print("  ✅ Environment validation complete")
    
    def build_backend(self):
        """Build backend with API and persona architecture"""
        print("🏗️ Building backend (API + Persona Backend + C7 + Sequential)...")
        
        # Change to backend directory
        original_cwd = os.getcwd()
        os.chdir(self.backend_dir)
        
        try:
            # Run backend build script
            result = subprocess.run(
                ["./scripts/build.sh", "production"],
                check=True,
                capture_output=True,
                text=True
            )
            
            print("  ✅ Backend build completed")
            
            # Copy build artifacts
            backend_dist = self.backend_dir / "dist"
            if backend_dist.exists():
                shutil.copytree(
                    backend_dist,
                    self.dist_dir / "backend",
                    dirs_exist_ok=True
                )
            
            self.config["features"].append("api")
            self.config["features"].append("persona_backend")
            self.config["features"].append("c7_compression")
            self.config["features"].append("sequential_processing")
            
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Backend build failed: {e}")
            print(f"  Error output: {e.stderr}")
            raise
        finally:
            os.chdir(original_cwd)
    
    def build_frontend(self):
        """Build frontend"""
        print("🎨 Building frontend...")
        
        # Check if frontend exists and has package.json
        if not (self.frontend_dir / "package.json").exists():
            print("  ⚠️ No frontend package.json found, skipping frontend build")
            return
        
        # Change to frontend directory
        original_cwd = os.getcwd()
        os.chdir(self.frontend_dir)
        
        try:
            # Install dependencies
            print("  📦 Installing frontend dependencies...")
            subprocess.run(["npm", "install"], check=True, capture_output=True)
            
            # Build frontend
            print("  🏗️ Building frontend...")
            subprocess.run(["npm", "run", "build"], check=True, capture_output=True)
            
            # Copy build artifacts
            frontend_build = self.frontend_dir / "build"
            if frontend_build.exists():
                shutil.copytree(
                    frontend_build,
                    self.dist_dir / "frontend",
                    dirs_exist_ok=True
                )
            
            print("  ✅ Frontend build completed")
            self.config["features"].append("frontend")
            
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Frontend build failed: {e}")
            print(f"  Error output: {e.stderr}")
            # Don't raise - frontend build failure shouldn't stop backend
        finally:
            os.chdir(original_cwd)
    
    def apply_c7_optimizations(self):
        """Apply C7 compression optimizations"""
        print("🗜️ Applying C7 compression optimizations...")
        
        # Compress static assets
        for root, dirs, files in os.walk(self.dist_dir):
            for file in files:
                file_path = Path(root) / file
                
                # Compress text-based files
                if file_path.suffix in ['.js', '.css', '.json', '.html', '.xml', '.txt']:
                    try:
                        # Use gzip compression level 7
                        subprocess.run([
                            "gzip", "-7", "-k", str(file_path)
                        ], check=True, capture_output=True)
                        
                        # Keep both compressed and uncompressed versions
                        print(f"    ✅ Compressed: {file_path.name}")
                        
                    except subprocess.CalledProcessError:
                        print(f"    ⚠️ Failed to compress: {file_path.name}")
        
        print("  ✅ C7 compression applied")
    
    def create_deployment_package(self):
        """Create deployment package"""
        print("📦 Creating deployment package...")
        
        # Create deployment structure
        deployment_dir = self.dist_dir / "deployment"
        deployment_dir.mkdir(exist_ok=True)
        
        # Copy backend
        if (self.dist_dir / "backend").exists():
            shutil.copytree(
                self.dist_dir / "backend",
                deployment_dir / "backend",
                dirs_exist_ok=True
            )
        
        # Copy frontend
        if (self.dist_dir / "frontend").exists():
            shutil.copytree(
                self.dist_dir / "frontend",
                deployment_dir / "frontend",
                dirs_exist_ok=True
            )
        
        # Create Docker configuration
        self.create_docker_config(deployment_dir)
        
        # Create deployment scripts
        self.create_deployment_scripts(deployment_dir)
        
        # Create archive
        archive_name = f"kowai-deployment-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}"
        shutil.make_archive(
            str(self.dist_dir / archive_name),
            'gztar',
            str(deployment_dir)
        )
        
        print(f"  ✅ Deployment package created: {archive_name}.tar.gz")
    
    def create_docker_config(self, deployment_dir: Path):
        """Create Docker configuration"""
        docker_dir = deployment_dir / "docker"
        docker_dir.mkdir(exist_ok=True)
        
        # Docker Compose
        compose_content = """version: '3.8'

services:
  backend:
    build:
      context: ../backend
      dockerfile: ../docker/Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql+aiomysql://user:password@mariadb:3306/kowai
      - COMPRESSION_ENABLED=true
      - COMPRESSION_LEVEL=7
    depends_on:
      - mariadb
      - redis
    networks:
      - kowai-network

  frontend:
    build:
      context: ../frontend
      dockerfile: ../docker/Dockerfile.frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    networks:
      - kowai-network

  mariadb:
    image: mariadb:10.11
    environment:
      - MYSQL_ROOT_PASSWORD=rootpassword
      - MYSQL_DATABASE=kowai
      - MYSQL_USER=user
      - MYSQL_PASSWORD=password
    volumes:
      - mariadb_data:/var/lib/mysql
    networks:
      - kowai-network

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    networks:
      - kowai-network

volumes:
  mariadb_data:
  redis_data:

networks:
  kowai-network:
    driver: bridge
"""
        
        with open(docker_dir / "docker-compose.yml", "w") as f:
            f.write(compose_content)
    
    def create_deployment_scripts(self, deployment_dir: Path):
        """Create deployment scripts"""
        scripts_dir = deployment_dir / "scripts"
        scripts_dir.mkdir(exist_ok=True)
        
        # Deploy script
        deploy_script = """#!/bin/bash
set -e

echo "🚀 Deploying KowAI..."

# Load environment variables
if [ -f ".env" ]; then
    source .env
fi

# Start services
docker-compose -f docker/docker-compose.yml up -d

echo "✅ KowAI deployed successfully!"
echo "🌍 Backend: http://localhost:8000"
echo "🎨 Frontend: http://localhost:3000"
echo "📖 API Docs: http://localhost:8000/docs"
echo "🔍 Health: http://localhost:8000/health"
"""
        
        with open(scripts_dir / "deploy.sh", "w") as f:
            f.write(deploy_script)
        
        # Make executable
        os.chmod(scripts_dir / "deploy.sh", 0o755)
    
    def generate_build_manifest(self):
        """Generate build manifest"""
        print("📋 Generating build manifest...")
        
        # Calculate build statistics
        build_size = self._calculate_directory_size(self.dist_dir)
        
        # Create manifest
        manifest = {
            "project": "KowAI",
            "build_configuration": self.config,
            "build_statistics": {
                "total_size_mb": round(build_size / (1024 * 1024), 2),
                "build_time": datetime.utcnow().isoformat(),
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "platform": sys.platform
            },
            "features": {
                "api": "FastAPI with OpenAPI documentation",
                "persona_backend": "DSPy-powered AI personas with routing",
                "c7_compression": "Level 7 compression for optimal performance",
                "sequential_processing": "Prefect-based workflow orchestration",
                "health_monitoring": "Comprehensive health checks and metrics",
                "structured_logging": "JSON-based logging with correlation tracking"
            },
            "deployment": {
                "backend_port": 8000,
                "frontend_port": 3000,
                "health_endpoint": "/health",
                "api_docs": "/docs",
                "metrics_endpoint": "/health/metrics"
            }
        }
        
        # Write manifest
        with open(self.dist_dir / "build-manifest.json", "w") as f:
            json.dump(manifest, f, indent=2)
        
        print("  ✅ Build manifest generated")
        return manifest
    
    def _calculate_directory_size(self, directory: Path) -> int:
        """Calculate total size of directory"""
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                file_path = Path(dirpath) / filename
                if file_path.exists():
                    total_size += file_path.stat().st_size
        return total_size
    
    def print_build_summary(self, manifest: Dict[str, Any]):
        """Print build summary"""
        print("\n" + "="*60)
        print("🎉 KowAI BUILD COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"📊 Build Statistics:")
        print(f"  • Total Size: {manifest['build_statistics']['total_size_mb']} MB")
        print(f"  • Features: {len(manifest['config']['features'])}")
        print(f"  • Python: {manifest['build_statistics']['python_version']}")
        print(f"  • Platform: {manifest['build_statistics']['platform']}")
        
        print(f"\n🚀 Deployment:")
        print(f"  • Backend: http://localhost:{manifest['deployment']['backend_port']}")
        print(f"  • API Docs: http://localhost:{manifest['deployment']['backend_port']}{manifest['deployment']['api_docs']}")
        print(f"  • Health: http://localhost:{manifest['deployment']['backend_port']}{manifest['deployment']['health_endpoint']}")
        
        print(f"\n✨ Features:")
        for feature, description in manifest['features'].items():
            print(f"  • {feature}: {description}")
        
        print(f"\n📦 Artifacts:")
        print(f"  • Build directory: {self.dist_dir}")
        print(f"  • Deployment package: dist/kowai-deployment-*.tar.gz")
        print(f"  • Build manifest: dist/build-manifest.json")
        
        print("\n" + "="*60)
    
    def build(self):
        """Execute complete build process"""
        print("🏗️ Starting KowAI Build System")
        print("Configuration: --api --persona-backend --c7 --seq")
        print("")
        
        try:
            self.setup_directories()
            self.validate_environment()
            self.build_backend()
            self.build_frontend()
            self.apply_c7_optimizations()
            self.create_deployment_package()
            manifest = self.generate_build_manifest()
            self.print_build_summary(manifest)
            
        except Exception as e:
            print(f"\n❌ Build failed: {e}")
            sys.exit(1)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="KowAI Universal Build System")
    parser.add_argument("--project-root", type=Path, default=Path.cwd(),
                      help="Project root directory")
    parser.add_argument("--api", action="store_true", default=True,
                      help="Build API components")
    parser.add_argument("--persona-backend", action="store_true", default=True,
                      help="Build persona backend")
    parser.add_argument("--c7", action="store_true", default=True,
                      help="Apply C7 compression")
    parser.add_argument("--seq", action="store_true", default=True,
                      help="Enable sequential processing")
    
    args = parser.parse_args()
    
    # Initialize build system
    build_system = KowAIBuildSystem(args.project_root)
    
    # Execute build
    build_system.build()


if __name__ == "__main__":
    main()