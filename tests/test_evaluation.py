import pytest

from evaluate_benchmark import (
    ndcg_at_k,
    precision_at_k,
    reciprocal_rank,
)


def test_precision_at_k():
    labels = [1, 1, 0, 1, 0]

    assert precision_at_k(labels, 5) == pytest.approx(0.6)


def test_precision_empty_results():
    assert precision_at_k([], 5) == 0.0


def test_reciprocal_rank_first_result():
    labels = [1, 0, 0, 0, 0]

    assert reciprocal_rank(labels) == 1.0


def test_reciprocal_rank_third_result():
    labels = [0, 0, 1, 0, 0]

    assert reciprocal_rank(labels) == pytest.approx(1 / 3)


def test_reciprocal_rank_no_relevant_results():
    labels = [0, 0, 0, 0, 0]

    assert reciprocal_rank(labels) == 0.0


def test_ndcg_perfect_ranking():
    labels = [1, 1, 1, 0, 0]

    assert ndcg_at_k(labels, 5) == pytest.approx(1.0)


def test_ndcg_penalizes_bad_order():
    ideal = [1, 1, 0, 0, 0]
    worse = [0, 0, 0, 1, 1]

    assert ndcg_at_k(worse, 5) < ndcg_at_k(ideal, 5)


def test_ndcg_no_relevant_results():
    labels = [0, 0, 0, 0, 0]

    assert ndcg_at_k(labels, 5) == 0.0