"""
API endpoints para gestión de flujos conversacionales
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from app.utils.database import get_db
from app.bot.conversation_flows import flow_manager

router = APIRouter(prefix="/api/flows", tags=["flows"])


class StartFlowRequest(BaseModel):
    flow_id: str
    conversation_id: int


class FlowMessageRequest(BaseModel):
    conversation_id: int
    message: str


@router.post("/start")
async def start_flow(request: StartFlowRequest):
    """Inicia un flujo conversacional"""
    result = flow_manager.start_flow(request.conversation_id, request.flow_id)
    return result


@router.post("/message")
async def process_flow_message(request: FlowMessageRequest):
    """Procesa un mensaje dentro de un flujo activo"""
    result = flow_manager.process_message(request.conversation_id, request.message)
    if not result:
        return {"error": "No active flow for this conversation"}
    return result


@router.get("/active/{conversation_id}")
async def get_active_flow(conversation_id: int):
    """Obtiene información del flujo activo"""
    flow = flow_manager.get_active_flow(conversation_id)
    if not flow:
        return {"active": False}
    
    return {
        "active": True,
        "flow_id": flow.flow_id,
        "flow_name": flow.name,
        "progress": flow.get_progress()
    }


@router.delete("/abandon/{conversation_id}")
async def abandon_flow(conversation_id: int):
    """Abandona el flujo activo"""
    flow_manager.abandon_flow(conversation_id)
    return {"abandoned": True}


@router.get("/available")
async def list_available_flows():
    """Lista todos los flujos disponibles"""
    return {
        "flows": [
            {
                "id": "onboarding",
                "name": "Onboarding IA Club",
                "description": "Flujo de bienvenida y selección de plan"
            },
            {
                "id": "recovery",
                "name": "Recuperación de Abandono",
                "description": "Recupera clientes que abandonaron el proceso"
            }
        ]
    }
