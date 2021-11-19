from rest_framework import throttling


class DemanageBurstThrottle(throttling.UserRateThrottle):
    """
    Throttle for demanage.
    """

    rate = "5/sec"  # max 5 requests per 1 second
    scope = None
