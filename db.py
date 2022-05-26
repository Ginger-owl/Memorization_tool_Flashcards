"""File with db class and all methods used to work with data in database"""


from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class MyFlashcards(Base):
    """Class describing table, created in database"""
    __tablename__ = 'flashcard'

    id = Column(Integer, primary_key=True)
    question = Column(String(50))
    answer = Column(String(50))
    # In this column we store number box_number from 1 to 3, where '1' means 'new', 2 means 'in the process of learning', '3' means 'known' - and should not be stored anymore.
    box_number = Column(Integer)

    @staticmethod
    def find_all():
        """Returns all values, that are stored in the table"""
        return session.query(MyFlashcards).all()

    @staticmethod
    def add_new_row(question, answer, box=1):
        """Adds new values into the table. Values for 'question' and 'answer' must be specified. 'Box_number' is defaulted to 1"""
        new_row = MyFlashcards(question=question, answer=answer, box_number=box)
        session.add(new_row)
        session.commit()

    @staticmethod
    def delete_flashcard(id_value):
        """Deletes all data for the row with specified id"""
        query = session.query(MyFlashcards)
        query.filter(MyFlashcards.id == id_value).delete()
        session.commit()

    @staticmethod
    def edit_flashcard(id_value):
        """Updates data in cells 'question' and 'answer' with values specified by user, if they are provided"""
        query = session.query(MyFlashcards.question, MyFlashcards.answer).filter(MyFlashcards.id == id_value)
        for row in query:
            print(f'current question: {row.question}')
            new_question = input("please write a new question:")
            if new_question.strip():
                query.update({'question': new_question})
            print(f'current answer: {row.answer}')
            new_answer = input("please write a new answer:")
            if new_answer.strip():
                query.update({'answer': new_answer})
        session.commit()

    @staticmethod
    def update_box_value(id_value, box_change):
        """Updates data in the cell 'box_number' when user revises the card - either adds or subsctract 1. Values of box_number may not be less than 1"""
        query = session.query(MyFlashcards.box_number).filter(MyFlashcards.id == id_value)
        for row in query:
            if row.box_number == 1 and box_change == -1:
                query.update({'box_number': 1})
            else:
                query.update({'box_number': row.box_number + box_change})
        session.commit()

    @staticmethod
    def delete_learnt():
        """Deletes data for rows where box_number == 3, i.e. information is well-learnt"""
        query = session.query(MyFlashcards)
        query.filter(MyFlashcards.box_number == 3).delete()
        session.commit()


engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
