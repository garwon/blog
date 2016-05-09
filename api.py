from app import api
from models import Comment

api.create_api(Comment, methods=['GET', 'POST'])
