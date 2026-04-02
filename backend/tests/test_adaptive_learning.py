import time
import unittest

from app.database import SessionLocal
from app.models.user import User
from app.services.adaptive_learning import build_adaptive_context, record_feedback
from app.services.auth import hash_password


class AdaptiveLearningTests(unittest.TestCase):
    def _unique_email(self) -> str:
        return f"adaptive.{time.time_ns()}@boaforma.ai"

    def _create_user(self, db) -> User:
        user = User(
            name="Adaptive User",
            email=self._unique_email(),
            hashed_password=hash_password("SenhaForte@123"),
            age=30,
            weight_kg=80,
            height_cm=176,
            goal="hipertrofia",
            level="intermediario",
            restrictions="nenhuma",
            provider="email",
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def test_feedback_profile_prefers_lighter_when_many_hard_feedbacks(self) -> None:
        db = SessionLocal()
        try:
            user = self._create_user(db)
            record_feedback(db, user_id=user.id, feedback="dificil")
            record_feedback(db, user_id=user.id, feedback="dificil")
            record_feedback(db, user_id=user.id, feedback="dificil")
            profile_context = build_adaptive_context(db, user_id=user.id)
            self.assertIn("lighter", profile_context)
            self.assertIn("difícil: 3", profile_context)
        finally:
            db.close()

    def test_feedback_profile_prefers_stronger_when_many_easy_feedbacks(self) -> None:
        db = SessionLocal()
        try:
            user = self._create_user(db)
            record_feedback(db, user_id=user.id, feedback="facil")
            record_feedback(db, user_id=user.id, feedback="facil")
            record_feedback(db, user_id=user.id, feedback="facil")
            profile_context = build_adaptive_context(db, user_id=user.id)
            self.assertIn("stronger", profile_context)
            self.assertIn("fácil: 3", profile_context)
        finally:
            db.close()


if __name__ == "__main__":
    unittest.main()
