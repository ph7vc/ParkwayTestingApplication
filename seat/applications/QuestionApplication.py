import logging
from seat.models.exam import Choice, Question, Exam

logger = logging.getLogger("applications")

class QuestionApplication(object):

    """complex functionality for dealing with question objects"""

    def create_choice(self, text):
        new_choice = Choice.objects.create(text=text)
        new_choice.save()
        return new_choice

    def upsert_question(self, exam_id, question_json):
        question = {} # init question variable

        #optionals
        points = question_json.get('points')
        points = points if points and points != '' else 1

        number = question_json.get('number') 
        number = number if number and number != '' else 0 # TODO: handle ordering properly
        
        text = question_json.get('prompt') or ''
        
        #required
        if 'type' not in question_json:
            return [False, "no type given"]

        type = question_json['type']

        id = question_json.get('question_id')

        #update
        if id and id.strip() != '':
            #update
            questions = Question.objects.filter(id=question_json['question_id'], exam__id = exam_id)
            if not questions.exists():
                return [False, "question does not exist"]
            question = questions.all()[0]
        #create
        else:
            question = Question.objects.create(
                points = points,
                number = number,
                text = text,
                category = type,
                exam = Exam.objects.get(id=exam_id)
                )
        # delete every answer and choice
        #map(lambda c: c.delete(), question.choices.all())
        #map(lambda a: a.delete(), question.answers.all())
        question.choices.all().delete()
        question.answers.all().delete()
        
        if 'options' in question_json:
            map(lambda choice_text: question.choices.add(Choice.create(choice_text)), question_json['options'])
        
        if 'answers' in question_json:
            map(lambda answer_text: question.answers.add(Choice.create(choice_text)), question_json['answers'])

        question.save()

        return [question, "succcess"]