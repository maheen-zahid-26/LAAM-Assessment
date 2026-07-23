from dataclasses import dataclass


@dataclass
class Adjustment:
    label: str
    type: str  # "discount" | "fee"
    amount: float
    is_percentage: bool = False


@dataclass
class PriceLine:
    label: str
    amount: float


@dataclass
class PriceBreakdown:
    base_price: float
    discounts: list[PriceLine]
    fees: list[PriceLine]
    final_price: float


def compute_price(base_price: float, adjustments: list[Adjustment]) -> PriceBreakdown:
    """
    Applies discounts to the base price first, then fees on the discounted
    subtotal. This ordering matters: a fee calculated before a discount would
    overstate what the customer actually pays, which defeats the point of
    showing a transparent breakdown.

    Adjustments with a non-positive amount are skipped defensively rather
    than allowed to corrupt the total — bad data shouldn't silently produce
    a wrong price.
    """
    discounts: list[PriceLine] = []
    fees: list[PriceLine] = []

    subtotal = base_price

    # Discounts first: percentage discounts computed off the original base price,
    # flat discounts applied directly.
    for adj in adjustments:
        if adj.type != "discount" or adj.amount <= 0:
            continue
        amount = base_price * (adj.amount / 100) if adj.is_percentage else adj.amount
        amount = min(amount, subtotal)  # never discount past zero
        discounts.append(PriceLine(label=adj.label, amount=round(amount, 2)))
        subtotal -= amount

    # Fees second, computed on the discounted subtotal.
    for adj in adjustments:
        if adj.type != "fee" or adj.amount <= 0:
            continue
        amount = subtotal * (adj.amount / 100) if adj.is_percentage else adj.amount
        fees.append(PriceLine(label=adj.label, amount=round(amount, 2)))
        subtotal += amount

    return PriceBreakdown(
        base_price=round(base_price, 2),
        discounts=discounts,
        fees=fees,
        final_price=round(subtotal, 2),
    )
