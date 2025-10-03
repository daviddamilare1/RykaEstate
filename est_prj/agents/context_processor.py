from agents.models import *



def default(request):
    noti = None
    if request.user.is_authenticated:
        try:
            # Get the Agent instance for the user
            agent = request.user.agents
            noti = Notification.objects.filter(agent=agent, seen=False)
        except Agent.DoesNotExist:
            # Handle case where user has no associated Agent
            pass
        except Exception as e:
            # Log other potential errors for debugging
            print(f"Error fetching notifications: {e}")
    return {
        "noti": noti,
    }