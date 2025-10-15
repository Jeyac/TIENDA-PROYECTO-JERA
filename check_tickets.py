#!/usr/bin/env python3
"""
Script para verificar qué tickets quedan en la base de datos
"""

import sys
import os

# Agregar el directorio backend al path
sys.path.append('backend')

from app import create_app
from funcionalidades.tickets.infrastructure.ticket_model import TicketModel

def check_tickets():
    app = create_app()
    with app.app_context():
        try:
            # Verificar todos los tickets
            tickets = TicketModel.query.all()
            print(f'Tickets totales en la base de datos: {len(tickets)}')
            
            for ticket in tickets:
                print(f'Ticket ID: {ticket.id}, Título: {ticket.title}, Usuario ID: {ticket.user_id}, Estado: {ticket.status}')
                
            # Verificar tickets del usuario 2 específicamente
            user_tickets = TicketModel.query.filter_by(user_id=2).all()
            print(f'\nTickets del usuario 2: {len(user_tickets)}')
            
            for ticket in user_tickets:
                print(f'  - Ticket ID: {ticket.id}, Título: {ticket.title}, Estado: {ticket.status}')
                
        except Exception as e:
            print(f'Error: {e}')
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    check_tickets()







