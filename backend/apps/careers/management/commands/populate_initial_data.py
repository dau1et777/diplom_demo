"""
Django management command to populate initial quiz questions and career data.
Run with: python manage.py populate_initial_data
"""

from django.core.management.base import BaseCommand
from apps.quiz.models import QuizQuestion
from apps.careers.models import Career, Course, University
import json


class Command(BaseCommand):
    help = 'Populate database with initial quiz questions and career data'

    def handle(self, *args, **options):
        self.stdout.write('Starting data population...')
        
        # Create quiz questions
        self._create_quiz_questions()
        
        # Create careers and related data
        self._create_careers()
        
        self.stdout.write(self.style.SUCCESS('Data population completed successfully!'))
    
    def _create_quiz_questions(self):
        """Create initial set of quiz questions."""
        
        questions_data = [
            # Logical Thinking
            {'text': 'How would you rate your logical thinking abilities?', 'category': 'logic', 'order': 1},
            {'text': 'How comfortable are you solving complex problems step-by-step?', 'category': 'logic', 'order': 2},
            {'text': 'Do you enjoy debugging and troubleshooting technical issues?', 'category': 'logic', 'order': 3},
            
            # Creativity
            {'text': 'How creative would you consider yourself?', 'category': 'creativity', 'order': 4},
            {'text': 'How often do you come up with original ideas and solutions?', 'category': 'creativity', 'order': 5},
            {'text': 'Do you enjoy artistic or design-related activities?', 'category': 'creativity', 'order': 6},
            
            # Communication
            {'text': 'How strong are your communication and presentation skills?', 'category': 'communication', 'order': 7},
            {'text': 'Are you comfortable working with and leading people?', 'category': 'communication', 'order': 8},
            {'text': 'How well do you express your ideas to others?', 'category': 'communication', 'order': 9},
            
            # Academic Performance
            {'text': 'How would you rate your performance in Mathematics?', 'category': 'academic', 'order': 10},
            {'text': 'How would you rate your performance in Science subjects?', 'category': 'academic', 'order': 11},
            {'text': 'How would you rate your performance in Language/English?', 'category': 'academic', 'order': 12},
            {'text': 'How would you rate your performance in Art/Creative subjects?', 'category': 'academic', 'order': 13},
            
            # Interests
            {'text': 'How interested are you in Technology and Programming?', 'category': 'interests', 'order': 14},
            {'text': 'How interested are you in Business and Management?', 'category': 'interests', 'order': 15},
            {'text': 'How interested are you in Creative fields (Design, Arts)?', 'category': 'interests', 'order': 16},
            {'text': 'How interested are you in Social and People-related work?', 'category': 'interests', 'order': 17},
            
            # Work Style
            {'text': 'Do you prefer working independently?', 'category': 'work_style', 'order': 18},
            {'text': 'Do you prefer working in teams and collaboratively?', 'category': 'work_style', 'order': 19},
        ]
        
        created_count = 0
        for q_data in questions_data:
            question, created = QuizQuestion.objects.get_or_create(
                question_text=q_data['text'],
                defaults={
                    'category': q_data['category'],
                    'order': q_data['order'],
                    'is_active': True,
                    'description': f"Question {q_data['order']}"
                }
            )
            if created:
                created_count += 1
        
        self.stdout.write(f'Created {created_count} quiz questions')
    
    def _create_careers(self):
        """Create initial set of careers with courses and universities."""
        
        careers_data = [
            {
                'name': 'Software Developer',
                'description': 'Develops applications and systems using programming languages and frameworks.',
                'skills': ['Python', 'JavaScript', 'Problem-solving', 'System Design'],
                'suitable_for': 'Strong logical thinking, tech interest, good math skills',
                'salary': '$80k - $150k',
                'growth': '15% annual',
                'companies': ['Google', 'Microsoft', 'Apple', 'Amazon'],
                'education': 'Bachelor in Computer Science'
            },
            {
                'name': 'Data Scientist',
                'description': 'Analyzes complex datasets to inform business decisions using ML and statistical methods.',
                'skills': ['Python', 'Statistics', 'ML', 'Data Visualization'],
                'suitable_for': 'Excellent math, problem-solving, tech-savvy individuals',
                'salary': '$100k - $180k',
                'growth': '36% annual',
                'companies': ['Google', 'Facebook', 'Amazon', 'IBM'],
                'education': 'Master in Data Science or CS'
            },
            {
                'name': 'AI/ML Engineer',
                'description': 'Designs and implements machine learning and AI solutions.',
                'skills': ['Python', 'TensorFlow', 'Mathematics', 'System Design'],
                'suitable_for': 'High logical thinking, math background, innovation-oriented',
                'salary': '$120k - $200k',
                'growth': '44% annual',
                'companies': ['Google', 'OpenAI', 'Meta', 'Tesla'],
                'education': 'Master in AI/ML or related field'
            },
            {
                'name': 'Graphic Designer',
                'description': 'Creates visual content for digital and print media.',
                'skills': ['Adobe Creative Suite', 'Design Thinking', 'Visual Layout', 'Color Theory'],
                'suitable_for': 'High creativity, visual thinking, good art skills',
                'salary': '$50k - $100k',
                'growth': '3% annual',
                'companies': ['Adobe', 'Design Agencies', 'Tech Companies'],
                'education': 'Bachelor in Graphic Design'
            },
            {
                'name': 'Business Manager',
                'description': 'Oversees business operations and manages teams effectively.',
                'skills': ['Leadership', 'Communication', 'Strategic Planning', 'Team Management'],
                'suitable_for': 'Strong leadership, communication skills, collaborative',
                'salary': '$70k - $130k',
                'growth': '8% annual',
                'companies': ['Fortune 500 Companies', 'Startups', 'Consulting Firms'],
                'education': 'MBA or Bachelor in Business'
            },
            {
                'name': 'Product Manager',
                'description': 'Leads product development and strategy for digital products.',
                'skills': ['Leadership', 'Communication', 'Analytics', 'User Research'],
                'suitable_for': 'Balanced skills, innovation-focused, collaborative',
                'salary': '$90k - $160k',
                'growth': '10% annual',
                'companies': ['Tech companies', 'Startups', 'Product-focused firms'],
                'education': 'Bachelor in any field + relevant experience'
            },
            {
                'name': 'Human Resources Manager',
                'description': 'Manages human resources, recruitment, and employee development.',
                'skills': ['Communication', 'Empathy', 'Leadership', 'Conflict Resolution'],
                'suitable_for': 'People-oriented, strong communication, empathetic',
                'salary': '$60k - $120k',
                'growth': '7% annual',
                'companies': ['All industries', 'HR Consulting firms'],
                'education': 'Bachelor in HR or Business'
            },
            {
                'name': 'UX Designer',
                'description': 'Designs user interfaces and experiences for digital products.',
                'skills': ['UI/UX Design', 'Figma', 'User Research', 'Communication'],
                'suitable_for': 'Creativity, user empathy, balancedbetween art and logic',
                'salary': '$70k - $140k',
                'growth': '13% annual',
                'companies': ['Tech companies', 'Design firms'],
                'education': 'Bachelor in Design or HCI'
            },
        ]
        
        created_count = 0
        for career_data in careers_data:
            career, created = Career.objects.get_or_create(
                name=career_data['name'],
                defaults={
                    'description': career_data['description'],
                    'required_skills': career_data['skills'],
                    'suitable_for': career_data['suitable_for'],
                    'average_salary_range': career_data['salary'],
                    'job_growth': career_data['growth'],
                    'typical_companies': career_data['companies'],
                    'required_education': career_data['education'],
                    'is_active': True
                }
            )
            if created:
                created_count += 1
        
        self.stdout.write(f'Created {created_count} careers')
