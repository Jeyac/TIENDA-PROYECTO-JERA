#!/usr/bin/env python3
"""
Script para eliminar el ticket duplicado
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.append('.')

from app import create_app
from funcionalidades.tickets.infrastructure.ticket_model import TicketModel
from funcionalidades.core.infraestructura.database import db

def delete_duplicate_ticket():
    app = create_app()
    with app.app_context():
        try:
            # Buscar tickets duplicados
            tickets = TicketModel.query.filter_by(title='Consulta sobre refrigeradoras').all()
            print(f'Tickets con título duplicado: {len(tickets)}')
            
            for ticket in tickets:
                print(f'Ticket ID: {ticket.id}, Creado: {ticket.created_at}')
            
            # Eliminar el ticket más reciente (ID 3)
            ticket_to_delete = TicketModel.query.get(3)
            if ticket_to_delete:
                print(f'Eliminando ticket ID: {ticket_to_delete.id}')
                
                # Primero eliminar todas las actividades del ticket
                from funcionalidades.tickets.infrastructure.ticket_model import TicketActivityModel
                activities = TicketActivityModel.query.filter_by(ticket_id=3).all()
                print(f'Eliminando {len(activities)} actividades del ticket')
                for activity in activities:
                    db.session.delete(activity)
                
                # Luego eliminar el ticket
                db.session.delete(ticket_to_delete)
                db.session.commit()
                print('Ticket duplicado y sus actividades eliminados exitosamente')
            else:
                print('Ticket no encontrado')
                
            # Verificar que solo quede uno
            remaining_tickets = TicketModel.query.filter_by(title='Consulta sobre refrigeradoras').all()
            print(f'Tickets restantes con ese título: {len(remaining_tickets)}')
            
        except Exception as e:
            print(f'Error: {e}')
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    delete_duplicate_ticket()
