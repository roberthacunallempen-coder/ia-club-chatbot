"""
Agent Configuration API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.agent_config import AgentConfig
from app.schemas.agent_config import (
    AgentConfig as AgentConfigSchema,
    AgentConfigCreate,
    AgentConfigUpdate
)
from app.utils.database import get_db

router = APIRouter(prefix="/api/agents", tags=["agents"])


# Default agent configurations
DEFAULT_AGENTS = [
    {
        "agent_type": "sales",
        "agent_name": "Agente de Ventas",
        "role_description": "Especialista en productos, precios y ventas",
        "instructions": """Eres un especialista en ventas para IA Club.

Tu expertise:
- MEGAPACK: 40+ IAs premium en un solo paquete
- Precios y planes (1, 2, 3 meses)
- Servicios VIP (VIP 1, VIP 2, VIP 3)
- IAs destacadas: ChatGPT Plus, Claude, Sora 2, Veo 3.1 Ultra, Midjourney
- Cuentas personales, uso ilimitado

Siempre sé amigable, profesional y ayuda a los clientes a encontrar la mejor solución para sus necesidades.
Proporciona precios claros cuando estén disponibles, sugiere opciones y guía hacia la compra.""",
        "temperature": 70,
        "max_tokens": 500,
        "is_active": True
    },
    {
        "agent_type": "design",
        "agent_name": "Agente de Diseño",
        "role_description": "Especialista en diseño y personalización con IA",
        "instructions": """Eres un especialista en IAs creativas para IA Club.

Tu expertise:
- IAs de generación de video: Sora 2, Veo 3.1 Ultra, Kling AI
- IAs de generación de imágenes: Midjourney, DALL-E
- Editores de video y audio: CapCut PRO, Runway, Higgsfield
- Asistencia para proyectos creativos
- Recomendaciones de IAs según necesidades del cliente

Ayuda a los clientes a aprovechar al máximo las IAs creativas del MEGAPACK. Sé entusiasta y explica las capacidades de cada IA claramente.""",
        "temperature": 80,
        "max_tokens": 600,
        "is_active": True
    },
    {
        "agent_type": "order_tracking",
        "agent_name": "Agente de Seguimiento",
        "role_description": "Especialista en estado y seguimiento de pedidos",
        "instructions": """Eres un especialista en gestión de pedidos para IA Club.

Tu expertise:
- Proceso de entrega de login/acceso al MEGAPACK
- Tiempos de entrega (rápido, usualmente mismo día)
- Activación de cuentas personales
- Seguimiento de pedidos
- Confirmación de pagos

Sé tranquilizador, proporciona cronogramas claros y mantén a los clientes informados sobre el progreso de sus pedidos.""",
        "temperature": 60,
        "max_tokens": 400,
        "is_active": True
    },
    {
        "agent_type": "support",
        "agent_name": "Agente de Soporte",
        "role_description": "Especialista en resolución de problemas",
        "instructions": """Eres un especialista en soporte al cliente para IA Club.

Tu expertise:
- Problemas técnicos con acceso a IAs
- Dudas sobre funcionamiento de cuentas
- Problemas de login o credenciales
- Dudas sobre características de las IAs
- Manejo de quejas y solución de problemas

Sé empático, orientado a soluciones y profesional. Siempre intenta resolver problemas o escalar apropiadamente.""",
        "temperature": 65,
        "max_tokens": 500,
        "is_active": True
    },
    {
        "agent_type": "general",
        "agent_name": "Agente General",
        "role_description": "Asistente general para consultas diversas",
        "instructions": """Eres un asistente general para IA Club.

Tu rol:
- Responder preguntas generales sobre la empresa
- Proporcionar información básica
- Direccionar consultas complejas a especialistas
- Manejar saludos y conversación casual

Sé amigable, servicial y guía a los usuarios al especialista adecuado cuando sea necesario.""",
        "temperature": 75,
        "max_tokens": 400,
        "is_active": True
    }
]


@router.get("", response_model=List[AgentConfigSchema])
@router.get("/", response_model=List[AgentConfigSchema])
async def list_agents(db: Session = Depends(get_db)):
    """List all agent configurations"""
    agents = db.query(AgentConfig).all()
    
    # If no agents exist, create defaults
    if not agents:
        for agent_data in DEFAULT_AGENTS:
            agent = AgentConfig(**agent_data)
            db.add(agent)
        db.commit()
        agents = db.query(AgentConfig).all()
    
    return agents


@router.get("/{agent_type}", response_model=AgentConfigSchema)
async def get_agent(agent_type: str, db: Session = Depends(get_db)):
    """Get specific agent configuration"""
    agent = db.query(AgentConfig).filter(AgentConfig.agent_type == agent_type).first()
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return agent


@router.post("", response_model=AgentConfigSchema)
@router.post("/", response_model=AgentConfigSchema)
async def create_agent(agent: AgentConfigCreate, db: Session = Depends(get_db)):
    """Create new agent configuration"""
    # Check if agent type already exists
    existing = db.query(AgentConfig).filter(AgentConfig.agent_type == agent.agent_type).first()
    if existing:
        raise HTTPException(status_code=400, detail="Agent type already exists")
    
    db_agent = AgentConfig(**agent.model_dump())
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    return db_agent


@router.put("/{agent_type}", response_model=AgentConfigSchema)
async def update_agent(
    agent_type: str,
    agent_update: AgentConfigUpdate,
    db: Session = Depends(get_db)
):
    """Update agent configuration"""
    db_agent = db.query(AgentConfig).filter(AgentConfig.agent_type == agent_type).first()
    
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Update only provided fields
    update_data = agent_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_agent, field, value)
    
    db.commit()
    db.refresh(db_agent)
    return db_agent


@router.delete("/{agent_type}")
async def delete_agent(agent_type: str, db: Session = Depends(get_db)):
    """Delete agent configuration (resets to default)"""
    db_agent = db.query(AgentConfig).filter(AgentConfig.agent_type == agent_type).first()
    
    if not db_agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    db.delete(db_agent)
    db.commit()
    
    return {"message": f"Agent {agent_type} deleted"}


@router.post("/reset-defaults")
async def reset_to_defaults(db: Session = Depends(get_db)):
    """Reset all agents to default configuration"""
    # Delete all existing
    db.query(AgentConfig).delete()
    
    # Create defaults
    for agent_data in DEFAULT_AGENTS:
        agent = AgentConfig(**agent_data)
        db.add(agent)
    
    db.commit()
    
    return {"message": "All agents reset to defaults"}
