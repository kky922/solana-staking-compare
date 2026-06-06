from unittest.mock import patch

import sol_staking_compare as staking


def test_effective_apy_prefers_live_value():
    option = staking.get_staking_options()[0]
    option.real_apy = 7.75
    assert staking.effective_apy(option) == 7.75


def test_sort_by_effective_apy_descending():
    options = staking.get_staking_options()[:2]
    options[0].real_apy = 1.0
    options[1].real_apy = 9.0
    assert staking.sort_by_effective_apy(options)[0] is options[1]


def test_price_api_failure_returns_none():
    with patch.object(staking, "HAS_REQUESTS", True), patch.object(
        staking.requests, "get", side_effect=RuntimeError("offline")
    ):
        assert staking.get_sol_price() is None
