from rest_framework import throttling


class InvitationBurstThrottle(throttling.UserRateThrottle):
    """
    Throttle for invitation.
    """

    scope = None
    rate = "5/hour"
