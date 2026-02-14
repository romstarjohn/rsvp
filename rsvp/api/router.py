import logging
from typing import Optional

from ninja import NinjaAPI, Schema

from api.models import Participation
from api.logging_utils import log_api_exceptions
from api.api_key_utils import api_key_security

from api.services import enqueue_rsvp_emails

logger = logging.getLogger("rsvp.custom")
api = NinjaAPI(version='1.0.0')

class RSVPSchema(Schema):
    first_name: str
    last_name: str
    email: str
    phone: Optional[str]
    participation: str
    relation: str
    message: Optional[str]



@api.post("/rsvp", auth=api_key_security)
@log_api_exceptions
def create_rsvp(request, data: RSVPSchema):
    participation, created = Participation.objects.update_or_create(
        email=data.email,
        defaults={
            "first_name": data.first_name,
            "last_name": data.last_name,
            "phone_number": data.phone,
            "participation" : data.participation,
            "relation": data.relation,
            "message": data.message,
        }
    )
    participation.save()
    enqueue_rsvp_emails(participation)
    if created:
        message = "Nouvelle confirmation de présence enregistrée avec succès 💖"
    else:
        message = "Vous aviez déjà confirmé votre présence. Votre réponse a été mise à jour ✅"


    return {
        "success": True,
        "message": message,
        "email": participation.email,
    }


