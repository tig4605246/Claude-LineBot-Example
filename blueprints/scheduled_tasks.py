from flask import Blueprint

scheduled_tasks_bp = Blueprint('scheduled_tasks', __name__)

# This blueprint doesn't have routes, but you can add methods here
# that will be used by the scheduler if needed