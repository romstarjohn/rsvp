# api/views.py (or wherever your RSVP endpoint is)
from emails.models import EmailQueue

def enqueue_rsvp_emails(participation):
    """Enqueue emails for the user and admin after RSVP."""
    # Email to the user
    EmailQueue.objects.create(
        to_email=participation.email,
        subject="Confirmation de votre présence au mariage",
        body=f"""
        Bonjour {participation.first_name},<br><br>
        Merci pour votre réponse. Nous avons bien enregistré votre participation : 
        <b>{participation.participation}</b>.<br><br>
        💖 À très bientôt !
        """,
        is_html=True,
    )

    # Notification to admin
    EmailQueue.objects.create(
        to_email="mystirool@yahoo.fr",
        subject=f"Nouveau RSVP: {participation.first_name} {participation.last_name}",
        body=f"{participation.first_name} {participation.last_name} a soumis sa réponse : {participation.participation}",
        is_html=True,
    )
