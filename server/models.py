from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, default=False, nullable=False)

    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')

    # Validates
    @validates('name')
    def validate_name(self, key, value):
        if not value or len(value.strip()) < 3:
            raise ValueError("Exercise name must be at least 3 characters long.")
        return value

    @validates('category')
    def validate_category(self, key, value):
        valid_categories = ["Strength", "Cardio", "Flexibility", "Balance"]
        if value not in valid_categories:
            raise ValueError(f"Category must be one of {valid_categories}.")
        return value

    def __repr__(self):
        return f"<Exercise id={self.id} name={self.name} category={self.category}>"


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='check_duration_minutes_positive'),
    )

    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')

    @validates('duration_minutes')
    def validate_duration(self, key, value):
        if value is None or value <= 0:
            raise ValueError("Workout duration must be greater than 0 minutes.")
        return value

    @validates('date')
    def validate_date(self, key, value):
        from datetime import date, datetime
        if isinstance(value, str):
            try:
                return datetime.strptime(value, "%Y-%m-%d").date()
            except ValueError:
                raise ValueError("Date must be in YYYY-MM-DD format.")
        elif not isinstance(value, (date, datetime)):
            raise ValueError("Date must be a date object or a string in YYYY-MM-DD format.")
        return value

    def __repr__(self):
        return f"<Workout id={self.id} date={self.date} duration_minutes={self.duration_minutes}>"


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    __table_args__ = (
        CheckConstraint('reps >= 0', name='check_reps_non_negative'),
        CheckConstraint('sets >= 0', name='check_sets_non_negative'),
        CheckConstraint('duration_seconds >= 0', name='check_duration_seconds_non_negative'),
    )

    # Relationships
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    @validates('reps')
    def validate_reps(self, key, value):
        if value is not None and value < 0:
            raise ValueError("Reps must be non-negative.")
        return value

    @validates('sets')
    def validate_sets(self, key, value):
        if value is not None and value < 0:
            raise ValueError("Sets must be non-negative.")
        return value

    @validates('duration_seconds')
    def validate_duration_seconds(self, key, value):
        if value is not None and value < 0:
            raise ValueError("Duration seconds must be non-negative.")
        return value

    def __repr__(self):
        return f"<WorkoutExercise id={self.id} workout_id={self.workout_id} exercise_id={self.exercise_id}>"
