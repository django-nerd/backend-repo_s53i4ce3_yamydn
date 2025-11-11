import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl

app = FastAPI(title="Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Profile(BaseModel):
    name: str
    title: str
    location: str
    bio: str
    avatar: Optional[HttpUrl] = None
    socials: dict


class Skill(BaseModel):
    name: str
    level: Optional[str] = None
    category: Optional[str] = None


class Experience(BaseModel):
    company: str
    role: str
    start: str
    end: str
    location: Optional[str] = None
    achievements: List[str] = []


class Project(BaseModel):
    name: str
    description: str
    tech: List[str]
    repo: Optional[HttpUrl] = None
    live: Optional[HttpUrl] = None
    image: Optional[HttpUrl] = None


class ContactMessage(BaseModel):
    name: str
    email: str
    message: str


@app.get("/")
def read_root():
    return {"message": "Portfolio Backend Running"}


@app.get("/api/profile", response_model=Profile)
def get_profile():
    return Profile(
        name="Your Name",
        title="Software Engineer",
        location="Remote / Worldwide",
        bio=(
            "I craft scalable web apps and delightful developer experiences. "
            "I specialize in React, TypeScript, Node.js, and cloud-native backends."
        ),
        avatar="https://avatars.githubusercontent.com/u/9919?s=200&v=4",
        socials={
            "github": "https://github.com/",
            "linkedin": "https://linkedin.com/in/",
            "twitter": "https://twitter.com/",
            "email": "mailto:you@example.com",
        },
    )


@app.get("/api/skills", response_model=List[Skill])
def get_skills():
    return [
        Skill(name="JavaScript", level="Expert", category="Frontend"),
        Skill(name="TypeScript", level="Advanced", category="Frontend"),
        Skill(name="React", level="Advanced", category="Frontend"),
        Skill(name="Node.js", level="Advanced", category="Backend"),
        Skill(name="Python", level="Advanced", category="Backend"),
        Skill(name="FastAPI", level="Advanced", category="Backend"),
        Skill(name="MongoDB", level="Advanced", category="Database"),
        Skill(name="PostgreSQL", level="Intermediate", category="Database"),
        Skill(name="Docker", level="Intermediate", category="DevOps"),
        Skill(name="AWS", level="Intermediate", category="Cloud"),
    ]


@app.get("/api/experience", response_model=List[Experience])
def get_experience():
    return [
        Experience(
            company="Tech Co.",
            role="Senior Software Engineer",
            start="2022",
            end="Present",
            location="Remote",
            achievements=[
                "Led migration to micro frontends across 5 products",
                "Improved build times by 40% with module federation",
                "Mentored 6 engineers and introduced better code review practices",
            ],
        ),
        Experience(
            company="Startup XYZ",
            role="Full-Stack Engineer",
            start="2020",
            end="2022",
            location="San Francisco, CA",
            achievements=[
                "Shipped real-time collaboration features used by 50k+ users",
                "Designed FastAPI backend with WebSocket event system",
            ],
        ),
    ]


@app.get("/api/projects", response_model=List[Project])
def get_projects():
    return [
        Project(
            name="DevDash",
            description="Developer productivity dashboard with integrations.",
            tech=["React", "Vite", "Tailwind", "FastAPI"],
            repo="https://github.com/",
            live="https://example.com",
            image="https://images.unsplash.com/photo-1555066931-4365d14bab8c?q=80&w=1200&auto=format&fit=crop",
        ),
        Project(
            name="TaskFlow",
            description="Team task management with real-time updates.",
            tech=["TypeScript", "React", "MongoDB", "Socket.io"],
            repo="https://github.com/",
            live="https://example.com",
            image="https://images.unsplash.com/photo-1515879218367-8466d910aaa4?q=80&w=1200&auto=format&fit=crop",
        ),
        Project(
            name="API Kit",
            description="Toolkit for building typed APIs quickly.",
            tech=["Python", "FastAPI", "Pydantic"],
            repo="https://github.com/",
            live="https://example.com",
            image="https://images.unsplash.com/photo-1518770660439-4636190af475?q=80&w=1200&auto=format&fit=crop",
        ),
    ]


@app.post("/api/contact")
def submit_contact(msg: ContactMessage):
    # In a real app, you might send an email or store in DB. Here we just acknowledge.
    if not msg.name or not msg.email or not msg.message:
        raise HTTPException(status_code=400, detail="All fields are required")
    return {"status": "received", "name": msg.name}


@app.get("/test")
def test_database():
    """Test endpoint to check if database is available and accessible"""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    
    try:
        from database import db
        
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
            
    except ImportError:
        response["database"] = "❌ Database module not found (run enable-database first)"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"
    
    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    
    return response


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
