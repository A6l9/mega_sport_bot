from database import models
from config import proj_settings


CHALLENGES_CONFIG = {
    "terfit": {
        "model_comments": models.TerfitComments,
        "model_challenges": models.TerfitChallenges,
        "admin_group": proj_settings.terfit_admins_group_id,
        "discussion_group": proj_settings.terfit_discussion_group_id,
        "assistant_id": proj_settings.terfit_assistant_id,
        "headers_list": ["club_name", "role", "execution_time"]
    },
    "athletx": {
        "model_comments": models.AthletxComments,
        "model_challenges": models.AthletxChallenges,
        "admin_group": proj_settings.athletx_admins_group_id,
        "discussion_group": proj_settings.athletx_discussion_group_id,
        "assistant_id": proj_settings.athletx_assistant_id,
        "headers_list": ["phone_number"]
    }
}
