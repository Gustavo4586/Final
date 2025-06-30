from flask import Blueprint, jsonify, request
from src.models.mongo_models import UserActivity, CourseAnalytics, ForumInteraction
from src.models.user import User, Course, ForumPost
from datetime import datetime, timedelta

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics/user/<int:user_id>/activities', methods=['GET'])
def get_user_activities(user_id):
    """Obtém atividades do usuário"""
    try:
        limit = request.args.get('limit', 50, type=int)
        activities = UserActivity.get_user_activities(user_id, limit)
        
        return jsonify({
            'success': True,
            'data': activities,
            'total': len(activities)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar atividades: {str(e)}'
        }), 500

@analytics_bp.route('/analytics/user/<int:user_id>/activity', methods=['POST'])
def create_user_activity(user_id):
    """Cria uma nova atividade do usuário"""
    try:
        data = request.get_json()
        
        if not data or 'activity_type' not in data:
            return jsonify({
                'success': False,
                'message': 'Tipo de atividade é obrigatório'
            }), 400
        
        activity_id = UserActivity.create_activity(
            user_id=user_id,
            activity_type=data['activity_type'],
            details=data.get('details', {}),
            course_id=data.get('course_id')
        )
        
        return jsonify({
            'success': True,
            'message': 'Atividade registrada com sucesso',
            'activity_id': activity_id
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao registrar atividade: {str(e)}'
        }), 500

@analytics_bp.route('/analytics/course/<int:course_id>', methods=['GET'])
def get_course_analytics(course_id):
    """Obtém analytics de um curso"""
    try:
        # Verificar se o curso existe
        course = Course.query.get(course_id)
        if not course:
            return jsonify({
                'success': False,
                'message': 'Curso não encontrado'
            }), 404
        
        analytics = CourseAnalytics.get_course_analytics(course_id)
        
        return jsonify({
            'success': True,
            'data': analytics or {'course_id': course_id, 'metrics': {}}
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar analytics: {str(e)}'
        }), 500

@analytics_bp.route('/analytics/course/<int:course_id>/stats', methods=['POST'])
def update_course_stats(course_id):
    """Atualiza estatísticas do curso"""
    try:
        data = request.get_json()
        
        if not data or 'metric' not in data or 'value' not in data:
            return jsonify({
                'success': False,
                'message': 'Métrica e valor são obrigatórios'
            }), 400
        
        # Verificar se o curso existe
        course = Course.query.get(course_id)
        if not course:
            return jsonify({
                'success': False,
                'message': 'Curso não encontrado'
            }), 404
        
        CourseAnalytics.update_course_stats(
            course_id=course_id,
            metric=data['metric'],
            value=data['value']
        )
        
        return jsonify({
            'success': True,
            'message': 'Estatísticas atualizadas com sucesso'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao atualizar estatísticas: {str(e)}'
        }), 500

@analytics_bp.route('/analytics/forum/post/<int:post_id>/interactions', methods=['GET'])
def get_post_interactions(post_id):
    """Obtém interações de um post do fórum"""
    try:
        # Verificar se o post existe
        post = ForumPost.query.get(post_id)
        if not post:
            return jsonify({
                'success': False,
                'message': 'Post não encontrado'
            }), 404
        
        interactions = ForumInteraction.get_post_interactions(post_id)
        
        return jsonify({
            'success': True,
            'data': interactions,
            'total': len(interactions)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar interações: {str(e)}'
        }), 500

@analytics_bp.route('/analytics/forum/interaction', methods=['POST'])
def record_forum_interaction():
    """Registra uma interação no fórum"""
    try:
        data = request.get_json()
        
        required_fields = ['user_id', 'post_id', 'interaction_type']
        if not data or not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'message': 'user_id, post_id e interaction_type são obrigatórios'
            }), 400
        
        # Verificar se o usuário e post existem
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({
                'success': False,
                'message': 'Usuário não encontrado'
            }), 404
        
        post = ForumPost.query.get(data['post_id'])
        if not post:
            return jsonify({
                'success': False,
                'message': 'Post não encontrado'
            }), 404
        
        interaction_id = ForumInteraction.record_interaction(
            user_id=data['user_id'],
            post_id=data['post_id'],
            interaction_type=data['interaction_type'],
            details=data.get('details', {})
        )
        
        return jsonify({
            'success': True,
            'message': 'Interação registrada com sucesso',
            'interaction_id': interaction_id
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao registrar interação: {str(e)}'
        }), 500

@analytics_bp.route('/analytics/user/<int:user_id>/forum-stats', methods=['GET'])
def get_user_forum_stats(user_id):
    """Obtém estatísticas do usuário no fórum"""
    try:
        # Verificar se o usuário existe
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'message': 'Usuário não encontrado'
            }), 404
        
        stats = ForumInteraction.get_user_forum_stats(user_id)
        
        return jsonify({
            'success': True,
            'data': stats
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar estatísticas: {str(e)}'
        }), 500

@analytics_bp.route('/analytics/dashboard/<int:user_id>', methods=['GET'])
def get_user_dashboard(user_id):
    """Obtém dados do dashboard do usuário combinando SQL e MongoDB"""
    try:
        # Verificar se o usuário existe
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'message': 'Usuário não encontrado'
            }), 404
        
        # Dados do SQL (dados principais)
        from src.models.user import Enrollment, Note, ForumPost
        
        enrollments = Enrollment.query.filter_by(user_id=user_id, is_active=True).all()
        notes = Note.query.filter_by(author_id=user_id, is_active=True).all()
        forum_posts = ForumPost.query.filter_by(author_id=user_id, is_active=True).all()
        
        # Dados do MongoDB (analytics e atividades)
        recent_activities = UserActivity.get_user_activities(user_id, 10)
        forum_stats = ForumInteraction.get_user_forum_stats(user_id)
        
        dashboard_data = {
            'user_info': {
                'id': user.id,
                'name': user.name,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'level': user.level
            },
            'sql_data': {
                'enrollments_count': len(enrollments),
                'notes_count': len(notes),
                'forum_posts_count': len(forum_posts),
                'enrollments': [
                    {
                        'id': e.id,
                        'course_id': e.course_id,
                        'progress_percentage': e.progress_percentage,
                        'enrolled_at': e.enrolled_at.isoformat() if e.enrolled_at else None
                    } for e in enrollments
                ]
            },
            'mongodb_data': {
                'recent_activities': recent_activities,
                'forum_stats': forum_stats
            }
        }
        
        return jsonify({
            'success': True,
            'data': dashboard_data
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao buscar dados do dashboard: {str(e)}'
        }), 500

