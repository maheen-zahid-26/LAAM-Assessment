from services.matching import CandidateProduct, find_alternatives

ORIGINAL_ID = "p1"


def make_candidate(id, category="lawn", price=1000, in_stock=True):
    return CandidateProduct(
        id=id,
        title=f"Product {id}",
        brand="Brand",
        category=category,
        price=price,
        image_url=None,
        has_requested_size_in_stock=in_stock,
    )


def test_matches_same_category_within_price_tolerance():
    candidates = [make_candidate("p2", price=1050), make_candidate("p3", price=900)]
    result = find_alternatives(ORIGINAL_ID, "lawn", 1000, candidates)
    assert {c.id for c in result} == {"p2", "p3"}


def test_excludes_different_category():
    candidates = [make_candidate("p2", category="footwear", price=1000)]
    result = find_alternatives(ORIGINAL_ID, "lawn", 1000, candidates)
    assert result == []


def test_excludes_price_outside_tolerance():
    candidates = [make_candidate("p2", price=1500)]  
    result = find_alternatives(ORIGINAL_ID, "lawn", 1000, candidates)
    assert result == []


def test_excludes_candidate_without_requested_size_in_stock():
    candidates = [make_candidate("p2", price=1000, in_stock=False)]
    result = find_alternatives(ORIGINAL_ID, "lawn", 1000, candidates)
    assert result == []


def test_excludes_the_original_product_itself():
    candidates = [make_candidate(ORIGINAL_ID, price=1000)]
    result = find_alternatives(ORIGINAL_ID, "lawn", 1000, candidates)
    assert result == []


def test_no_candidates_returns_empty_list_not_error():
    result = find_alternatives(ORIGINAL_ID, "lawn", 1000, [])
    assert result == []


def test_respects_limit_and_sorts_by_price_proximity():
    candidates = [
        make_candidate("far", price=1180),
        make_candidate("close", price=1010),
        make_candidate("mid", price=1080),
    ]
    result = find_alternatives(ORIGINAL_ID, "lawn", 1000, candidates, limit=2)
    assert [c.id for c in result] == ["close", "mid"]
