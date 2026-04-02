from sqlalchemy.orm import Session

from app.models.adaptive_feedback import UserAdaptiveProfile


def record_feedback(db: Session, *, user_id: int, feedback: str) -> UserAdaptiveProfile:
    profile = db.query(UserAdaptiveProfile).filter(UserAdaptiveProfile.user_id == user_id).first()
    if profile is None:
        profile = UserAdaptiveProfile(user_id=user_id)
        db.add(profile)
        db.flush()

    profile.total_feedbacks += 1
    profile.last_feedback = feedback
    if feedback == "facil":
        profile.easy_count += 1
    elif feedback == "dificil":
        profile.hard_count += 1
    else:
        profile.ok_count += 1

    profile.preferred_intensity = _infer_preferred_intensity(profile)
    db.commit()
    db.refresh(profile)
    return profile


def build_adaptive_context(db: Session, *, user_id: int) -> str:
    profile = db.query(UserAdaptiveProfile).filter(UserAdaptiveProfile.user_id == user_id).first()
    if profile is None or profile.total_feedbacks == 0:
        return "Sem perfil adaptativo ainda. Use feedback dos treinos para personalização progressiva."
    return (
        f"Perfil adaptativo: {profile.preferred_intensity}. "
        f"Feedbacks acumulados -> fácil: {profile.easy_count}, ok: {profile.ok_count}, difícil: {profile.hard_count}. "
        f"Último feedback: {profile.last_feedback}."
    )


def _infer_preferred_intensity(profile: UserAdaptiveProfile) -> str:
    if profile.hard_count >= profile.easy_count + 2:
        return "lighter"
    if profile.easy_count >= profile.hard_count + 2:
        return "stronger"
    return "balanced"
