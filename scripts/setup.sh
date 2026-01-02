#!/bin/bash

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Setting up Team Task Board project...${NC}\n"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}📝 Creating .env file from .env.example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✅ .env file created!${NC}"
    echo -e "${YELLOW}⚠️  Please update .env with your actual values${NC}\n"
else
    echo -e "${GREEN}✅ .env file already exists${NC}\n"
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed${NC}"
    echo -e "${YELLOW}Please install Docker: https://docs.docker.com/get-docker/${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker is installed${NC}\n"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}❌ Docker Compose is not installed${NC}"
    echo -e "${YELLOW}Please install Docker Compose: https://docs.docker.com/compose/install/${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Docker Compose is installed${NC}\n"

# Ask user if they want to use Docker or local setup
echo -e "${BLUE}How do you want to run the project?${NC}"
echo "1) Docker (Recommended)"
echo "2) Local (Python + Node.js)"
read -p "Enter your choice (1 or 2): " choice

if [ "$choice" = "1" ]; then
    echo -e "\n${BLUE}🐳 Setting up with Docker...${NC}\n"
    
    # Build images
    echo -e "${YELLOW}Building Docker images...${NC}"
    docker-compose build
    
    # Start containers
    echo -e "${YELLOW}Starting containers...${NC}"
    docker-compose up -d
    
    # Wait for database
    echo -e "${YELLOW}Waiting for database to be ready...${NC}"
    sleep 10
    
    # Run migrations
    echo -e "${YELLOW}Running migrations...${NC}"
    docker-compose exec backend python manage.py migrate
    
    echo -e "\n${GREEN}✅ Setup complete!${NC}"
    echo -e "${BLUE}🌐 Application is running at:${NC}"
    echo -e "   Frontend: ${GREEN}http://localhost:5173${NC}"
    echo -e "   Backend:  ${GREEN}http://localhost:8000${NC}"
    echo -e "   Admin:    ${GREEN}http://localhost:8000/admin${NC}"
    echo -e "\n${YELLOW}Create a superuser with:${NC}"
    echo -e "   ${BLUE}docker-compose exec backend python manage.py createsuperuser${NC}"
    
elif [ "$choice" = "2" ]; then
    echo -e "\n${BLUE}💻 Setting up locally...${NC}\n"
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}❌ Python 3 is not installed${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Python 3 is installed${NC}"
    
    # Check Node.js
    if ! command -v node &> /dev/null; then
        echo -e "${RED}❌ Node.js is not installed${NC}"
        exit 1
    fi
    echo -e "${GREEN}✅ Node.js is installed${NC}\n"
    
    # Backend setup
    echo -e "${YELLOW}Setting up backend...${NC}"
    cd backend
    python3 -m venv venv
    source venv/bin/activate 2>/dev/null || venv\\Scripts\\activate
    pip install -r requirements.txt
    python manage.py migrate
    cd ..
    
    # Frontend setup
    echo -e "${YELLOW}Setting up frontend...${NC}"
    cd frontend
    npm install
    cd ..
    
    echo -e "\n${GREEN}✅ Setup complete!${NC}"
    echo -e "${YELLOW}Start the backend with:${NC}"
    echo -e "   ${BLUE}cd backend && source venv/bin/activate && python manage.py runserver${NC}"
    echo -e "${YELLOW}Start the frontend with:${NC}"
    echo -e "   ${BLUE}cd frontend && npm run dev${NC}"
    
else
    echo -e "${RED}Invalid choice${NC}"
    exit 1
fi

echo -e "\n${GREEN}🎉 All done! Happy coding!${NC}\n"
