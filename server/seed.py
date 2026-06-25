#!/usr/bin/env python3

from app import app
from models import db, Exercise, Workout, WorkoutExercise
from datetime import date, timedelta

print("Seeding database...")

with app.app_context():
    print("Dropping existing tables...")
    db.drop_all()
    
    print("Creating tables...")
    db.create_all()

    # Seed Exercises
    print("Seeding exercises...")
    e1 = Exercise(name="Pushups", category="Strength", equipment_needed=False)
    e2 = Exercise(name="Running", category="Cardio", equipment_needed=False)
    e3 = Exercise(name="Deadlift", category="Strength", equipment_needed=True)
    e4 = Exercise(name="Yoga Stretch", category="Flexibility", equipment_needed=False)
    e5 = Exercise(name="Bicep Curls", category="Strength", equipment_needed=True)
    
    db.session.add_all([e1, e2, e3, e4, e5])
    db.session.commit()

    # Seed Workouts
    print("Seeding workouts...")
    w1 = Workout(date=date.today() - timedelta(days=2), duration_minutes=45, notes="Focus on upper body strength.")
    w2 = Workout(date=date.today() - timedelta(days=1), duration_minutes=30, notes="Morning cardio session.")
    w3 = Workout(date=date.today(), duration_minutes=60, notes="Full body workout.")
    
    db.session.add_all([w1, w2, w3])
    db.session.commit()

    # Seed Workout Exercises
    print("Seeding workout exercises...")
    
    # Workout 1: Pushups and Bicep Curls
    we1 = WorkoutExercise(workout=w1, exercise=e1, reps=15, sets=3, duration_seconds=120)
    we2 = WorkoutExercise(workout=w1, exercise=e5, reps=12, sets=3, duration_seconds=180)
    
    # Workout 2: Running
    we3 = WorkoutExercise(workout=w2, exercise=e2, reps=1, sets=1, duration_seconds=1800)
    
    # Workout 3: Deadlifts and Yoga Stretch
    we4 = WorkoutExercise(workout=w3, exercise=e3, reps=8, sets=4, duration_seconds=240)
    we5 = WorkoutExercise(workout=w3, exercise=e4, reps=10, sets=2, duration_seconds=600)
    
    db.session.add_all([we1, we2, we3, we4, we5])
    db.session.commit()

    print("Database seeding completed successfully!")
