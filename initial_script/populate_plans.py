import traceback
from app.models import Plan
from app.logger import logger


def populate_plans():
    try:
        Plan.objects.create(
            name="Basic",
            plan_type="basic",
            price=9.99,
            features=["Feature 1", "Feature 2"],
        )
        Plan.objects.create(
            name="Pro",
            plan_type="pro",
            price=19.99,
            features=["All Basic features", "Feature 3", "Feature 4"],
        )
        Plan.objects.create(
            name="Enterprise",
            plan_type="enterprise",
            price=49.99,
            features=["All Pro features", "Feature 5", "Premium support"],
        )

        logger.info("Plans populated successfully")

    except Exception as e:
        logger.error(traceback.format_exc())
        logger.error(e)


populate_plans()
