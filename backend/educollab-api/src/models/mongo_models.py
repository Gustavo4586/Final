from pymongo import MongoClient
from datetime import datetime
import os
from bson import ObjectId

class MongoConnection:
    """Classe para gerenciar a conexão com MongoDB"""
    
    def __init__(self):
        # Para desenvolvimento local, usaremos uma instância local do MongoDB
        # Para produção, isso seria configurado via variáveis de ambiente
        self.mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
        self.db_name = os.getenv('MONGO_DB_NAME', 'educollab_nosql')
        self.client = None
        self.db = None
        
    def connect(self):
        """Conecta ao MongoDB"""
        try:
            self.client = MongoClient(self.mongo_uri)
            self.db = self.client[self.db_name]
            # Teste de conexão
            self.client.admin.command('ping')
            print(f"Conectado ao MongoDB: {self.db_name}")
            return True
        except Exception as e:
            print(f"Erro ao conectar ao MongoDB: {e}")
            # Para desenvolvimento, vamos usar um mock se não conseguir conectar
            self.db = MockMongoDB()
            return False
    
    def get_database(self):
        """Retorna a instância do banco de dados"""
        if self.db is None:
            self.connect()
        return self.db

class MockMongoDB:
    """Mock do MongoDB para desenvolvimento quando o MongoDB não está disponível"""
    
    def __init__(self):
        self.data = {
            'user_activities': [],
            'course_analytics': [],
            'forum_interactions': []
        }
    
    def __getitem__(self, collection_name):
        return MockCollection(collection_name, self.data.get(collection_name, []))

class MockCollection:
    """Mock de uma coleção do MongoDB"""
    
    def __init__(self, name, data):
        self.name = name
        self.data = data
    
    def insert_one(self, document):
        document['_id'] = ObjectId()
        self.data.append(document)
        return MockInsertResult(document['_id'])
    
    def find(self, query=None, limit=None):
        results = self.data
        if query:
            # Implementação simples de filtro
            results = [doc for doc in results if self._match_query(doc, query)]
        if limit:
            results = results[:limit]
        return results
    
    def find_one(self, query):
        for doc in self.data:
            if self._match_query(doc, query):
                return doc
        return None
    
    def update_one(self, query, update):
        for doc in self.data:
            if self._match_query(doc, query):
                if '$set' in update:
                    doc.update(update['$set'])
                return MockUpdateResult(1)
        return MockUpdateResult(0)
    
    def delete_one(self, query):
        for i, doc in enumerate(self.data):
            if self._match_query(doc, query):
                del self.data[i]
                return MockDeleteResult(1)
        return MockDeleteResult(0)
    
    def _match_query(self, doc, query):
        """Implementação simples de matching de query"""
        for key, value in query.items():
            if key not in doc or doc[key] != value:
                return False
        return True

class MockInsertResult:
    def __init__(self, inserted_id):
        self.inserted_id = inserted_id

class MockUpdateResult:
    def __init__(self, modified_count):
        self.modified_count = modified_count

class MockDeleteResult:
    def __init__(self, deleted_count):
        self.deleted_count = deleted_count

# Instância global da conexão
mongo_connection = MongoConnection()

class UserActivity:
    """Modelo para atividades do usuário no MongoDB"""
    
    @staticmethod
    def create_activity(user_id, activity_type, details, course_id=None):
        """Cria uma nova atividade do usuário"""
        db = mongo_connection.get_database()
        
        activity = {
            'user_id': user_id,
            'activity_type': activity_type,  # 'login', 'course_access', 'note_created', 'forum_post', etc.
            'details': details,
            'course_id': course_id,
            'timestamp': datetime.utcnow(),
            'created_at': datetime.utcnow()
        }
        
        result = db['user_activities'].insert_one(activity)
        return str(result.inserted_id)
    
    @staticmethod
    def get_user_activities(user_id, limit=50):
        """Obtém as atividades de um usuário"""
        db = mongo_connection.get_database()
        
        activities = list(db['user_activities'].find(
            {'user_id': user_id},
            limit=limit
        ))
        
        # Converter ObjectId para string para serialização JSON
        for activity in activities:
            activity['_id'] = str(activity['_id'])
        
        return activities

class CourseAnalytics:
    """Modelo para analytics de cursos no MongoDB"""
    
    @staticmethod
    def update_course_stats(course_id, metric, value):
        """Atualiza estatísticas do curso"""
        db = mongo_connection.get_database()
        
        # Busca documento existente ou cria um novo
        existing = db['course_analytics'].find_one({'course_id': course_id})
        
        if existing:
            # Atualiza métrica existente
            update_data = {f'metrics.{metric}': value, 'updated_at': datetime.utcnow()}
            db['course_analytics'].update_one(
                {'course_id': course_id},
                {'$set': update_data}
            )
        else:
            # Cria novo documento
            analytics = {
                'course_id': course_id,
                'metrics': {metric: value},
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow()
            }
            db['course_analytics'].insert_one(analytics)
    
    @staticmethod
    def get_course_analytics(course_id):
        """Obtém analytics de um curso"""
        db = mongo_connection.get_database()
        
        analytics = db['course_analytics'].find_one({'course_id': course_id})
        if analytics:
            analytics['_id'] = str(analytics['_id'])
        
        return analytics

class ForumInteraction:
    """Modelo para interações do fórum no MongoDB"""
    
    @staticmethod
    def record_interaction(user_id, post_id, interaction_type, details=None):
        """Registra uma interação no fórum"""
        db = mongo_connection.get_database()
        
        interaction = {
            'user_id': user_id,
            'post_id': post_id,
            'interaction_type': interaction_type,  # 'view', 'vote', 'comment', 'share'
            'details': details or {},
            'timestamp': datetime.utcnow(),
            'created_at': datetime.utcnow()
        }
        
        result = db['forum_interactions'].insert_one(interaction)
        return str(result.inserted_id)
    
    @staticmethod
    def get_post_interactions(post_id):
        """Obtém interações de um post"""
        db = mongo_connection.get_database()
        
        interactions = list(db['forum_interactions'].find({'post_id': post_id}))
        
        # Converter ObjectId para string
        for interaction in interactions:
            interaction['_id'] = str(interaction['_id'])
        
        return interactions
    
    @staticmethod
    def get_user_forum_stats(user_id):
        """Obtém estatísticas do usuário no fórum"""
        db = mongo_connection.get_database()
        
        interactions = list(db['forum_interactions'].find({'user_id': user_id}))
        
        stats = {
            'total_interactions': len(interactions),
            'views': len([i for i in interactions if i['interaction_type'] == 'view']),
            'votes': len([i for i in interactions if i['interaction_type'] == 'vote']),
            'comments': len([i for i in interactions if i['interaction_type'] == 'comment']),
            'shares': len([i for i in interactions if i['interaction_type'] == 'share'])
        }
        
        return stats

# Inicializar conexão ao importar o módulo
mongo_connection.connect()

