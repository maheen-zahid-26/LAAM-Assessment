from datetime import date

from services.delivery import DeliveryZone, estimate_delivery

LAHORE = DeliveryZone(pincode_prefix="54", min_days=2, max_days=4, is_serviceable=True)
KARACHI = DeliveryZone(pincode_prefix="75", min_days=3, max_days=5, is_serviceable=True)
GILGIT_UNSERVICEABLE = DeliveryZone(pincode_prefix="15", min_days=5, max_days=9, is_serviceable=False)
LAHORE_SPECIFIC = DeliveryZone(pincode_prefix="540", min_days=1, max_days=2, is_serviceable=True)

ZONES = [LAHORE, KARACHI, GILGIT_UNSERVICEABLE]


def test_matching_prefix_returns_serviceable_estimate():
    result = estimate_delivery("54000", ZONES, today=date(2026, 7, 23))
    assert result.serviceable is True
    assert result.min_days == 2
    assert result.max_days == 4
    assert result.estimated_date == "2026-07-27"


def test_no_matching_prefix_returns_unavailable():
    result = estimate_delivery("99999", ZONES)
    assert result.serviceable is False
    assert result.message is not None


def test_explicitly_unserviceable_zone_returns_unavailable():
    result = estimate_delivery("15100", ZONES)
    assert result.serviceable is False


def test_longest_matching_prefix_wins():
    zones = [LAHORE, LAHORE_SPECIFIC]
    result = estimate_delivery("54000", zones, today=date(2026, 7, 23))
    assert result.min_days == 1
    assert result.max_days == 2
