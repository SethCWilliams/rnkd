#!/usr/bin/env python3
"""
Test script to verify Rnkd Phase 1 setup
"""

import os
import sys

def test_project_structure():
    """Test that all required files and directories exist"""
    print("🔍 Testing project structure...")
    
    required_files = [
        "backend/requirements.txt",
        "backend/app/main.py",
        "backend/app/core/config.py",
        "backend/app/api/v1/api.py",
        "backend/app/api/v1/endpoints/auth.py",
        "backend/app/api/v1/endpoints/users.py",
        "backend/app/api/v1/endpoints/groups.py",
        "backend/app/api/v1/endpoints/movies.py",
        "backend/app/api/v1/endpoints/voting.py",
        "backend/Dockerfile",
        "backend/env.example",
        "frontend/package.json",
        "frontend/tailwind.config.js",
        "frontend/src/App.tsx",
        "frontend/src/index.tsx",
        "frontend/src/index.css",
        "frontend/Dockerfile",
        "docker-compose.yml",
        "README.md"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"  ✅ {file_path}")
    
    if missing_files:
        print(f"  ❌ Missing files: {missing_files}")
        return False
    
    print("  ✅ All required files exist!")
    return True

def test_python_syntax():
    """Test that Python files have valid syntax"""
    print("\n🐍 Testing Python syntax...")
    
    python_files = [
        "backend/app/main.py",
        "backend/app/core/config.py",
        "backend/app/api/v1/api.py",
        "backend/app/api/v1/endpoints/auth.py",
        "backend/app/api/v1/endpoints/users.py",
        "backend/app/api/v1/endpoints/groups.py",
        "backend/app/api/v1/endpoints/movies.py",
        "backend/app/api/v1/endpoints/voting.py"
    ]
    
    for file_path in python_files:
        try:
            with open(file_path, 'r') as f:
                compile(f.read(), file_path, 'exec')
            print(f"  ✅ {file_path}")
        except SyntaxError as e:
            print(f"  ❌ {file_path}: {e}")
            return False
    
    print("  ✅ All Python files have valid syntax!")
    return True

def test_docker_compose():
    """Test that docker-compose.yml is valid"""
    print("\n🐳 Testing Docker Compose...")
    
    try:
        with open("docker-compose.yml", 'r') as f:
            content = f.read()
            # Basic validation - check for required services
            required_services = ["postgres", "redis", "backend", "frontend"]
            for service in required_services:
                if service not in content:
                    print(f"  ❌ Missing service: {service}")
                    return False
        print("  ✅ Docker Compose file looks valid!")
        return True
    except Exception as e:
        print(f"  ❌ Error reading docker-compose.yml: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Rnkd Phase 1 Setup Test\n")
    
    tests = [
        test_project_structure,
        test_python_syntax,
        test_docker_compose
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Phase 1 setup is complete.")
        print("\n📋 Next steps:")
        print("1. Install dependencies: pip install -r backend/requirements.txt")
        print("2. Start services: docker-compose up -d")
        print("3. Access frontend: http://localhost:3000")
        print("4. Access backend: http://localhost:8000")
        print("5. View API docs: http://localhost:8000/docs")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main() 