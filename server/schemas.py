from marshmallow import Schema, fields, validate, validates, ValidationError

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=3, error="Exercise name must be at least 3 characters long."))
    category = fields.Str(required=True, validate=validate.OneOf(["Strength", "Cardio", "Flexibility", "Balance"], error="Category must be one of Strength, Cardio, Flexibility, or Balance."))
    equipment_needed = fields.Bool(load_default=False)

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    reps = fields.Int(validate=validate.Range(min=0, error="Reps must be non-negative."))
    sets = fields.Int(validate=validate.Range(min=0, error="Sets must be non-negative."))
    duration_seconds = fields.Int(validate=validate.Range(min=0, error="Duration seconds must be non-negative."))

class WorkoutExerciseWithDetailSchema(Schema):
    id = fields.Int(dump_only=True)
    reps = fields.Int()
    sets = fields.Int()
    duration_seconds = fields.Int()
    exercise = fields.Nested(ExerciseSchema)

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True, error_messages={"invalid": "Date must be in YYYY-MM-DD format."})
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, error="Workout duration must be greater than 0 minutes."))
    notes = fields.Str(allow_none=True)
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseWithDetailSchema), dump_only=True)

class WorkoutDetailSchema(Schema):
    id = fields.Int()
    date = fields.Date()
    duration_minutes = fields.Int()
    notes = fields.Str()

class WorkoutExerciseWithWorkoutDetailSchema(Schema):
    id = fields.Int(dump_only=True)
    reps = fields.Int()
    sets = fields.Int()
    duration_seconds = fields.Int()
    workout = fields.Nested(WorkoutDetailSchema)

class ExerciseWithWorkoutsSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool()
    workout_exercises = fields.List(fields.Nested(WorkoutExerciseWithWorkoutDetailSchema), dump_only=True)
