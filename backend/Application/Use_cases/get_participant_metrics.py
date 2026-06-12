from Application.Ports.participant_repository import ParticipantRepository


class GetParticipantMetrics:
    def __init__(self, repo: ParticipantRepository):
        self._repo = repo

    async def execute(self) -> dict:
        participants = await self._repo.get_all()
        total = len(participants)
        if total == 0:
            return {
                "total_participants": 0,
                "study_groups": {"treatment": 0, "control": 0},
                "statuses": {"active": 0, "completed": 0, "withdrawn": 0},
                "genders": {"F": 0, "M": 0, "Other": 0},
                "average_age": 0.0,
            }

        treatment_count = sum(1 for p in participants if p.study_group == "treatment")
        control_count = sum(1 for p in participants if p.study_group == "control")

        active_count = sum(1 for p in participants if p.status == "active")
        completed_count = sum(1 for p in participants if p.status == "completed")
        withdrawn_count = sum(1 for p in participants if p.status == "withdrawn")

        f_count = sum(1 for p in participants if p.gender == "F")
        m_count = sum(1 for p in participants if p.gender == "M")
        other_count = sum(1 for p in participants if p.gender == "Other")

        avg_age = sum(p.age for p in participants) / total

        return {
            "total_participants": total,
            "study_groups": {
                "treatment": treatment_count,
                "control": control_count,
            },
            "statuses": {
                "active": active_count,
                "completed": completed_count,
                "withdrawn": withdrawn_count,
            },
            "genders": {
                "F": f_count,
                "M": m_count,
                "Other": other_count,
            },
            "average_age": round(avg_age, 2),
        }
