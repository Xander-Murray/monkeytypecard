import services.monkeytype as mt_service


class TestBestResult:
    def test_empty_list_returns_none(self):
        assert mt_service.best_result([]) is None

    def test_single_item(self):
        items = [{"wpm": 100, "acc": 95}]
        assert mt_service.best_result(items) == items[0]

    def test_picks_max_wpm(self):
        items = [
            {"wpm": 80, "acc": 99},
            {"wpm": 120, "acc": 90},
            {"wpm": 100, "acc": 95},
        ]
        assert mt_service.best_result(items) == {"wpm": 120, "acc": 90}


class TestNormalizeTime:
    def test_zero(self):
        assert mt_service.normalize_time(0) == "00:00:00"

    def test_3661(self):
        assert mt_service.normalize_time(3661) == "01:01:01"

    def test_negative(self):
        # timedelta(-5) produces "-1 day, 23:59:55" which rounds to "23:59:55"
        result = mt_service.normalize_time(-5)
        # Implementation uses timedelta, so negative values wrap; just verify it returns a string
        assert isinstance(result, str)
        assert len(result) == 8

    def test_non_numeric_string(self):
        assert mt_service.normalize_time("abc") == "00:00:00"

    def test_none(self):
        assert mt_service.normalize_time(None) == "00:00:00"


class TestIsProfilePrivate:
    def test_empty_personal_bests(self):
        profile = {"data": {"personalBests": {}}}
        assert mt_service.is_profile_private(profile) is True

    def test_missing_personal_bests(self):
        profile = {"data": {}}
        assert mt_service.is_profile_private(profile) is True

    def test_populated_personal_bests(self):
        profile = {
            "data": {
                "personalBests": {
                    "time": {"15": [{"wpm": 100, "acc": 95}]},
                }
            }
        }
        assert mt_service.is_profile_private(profile) is False


class TestIsValidUsername:
    def test_valid_alphanumeric(self):
        assert mt_service.is_valid_username("user123") is True

    def test_valid_special_chars(self):
        assert mt_service.is_valid_username("a.b-c_d") is True

    def test_valid_max_length(self):
        assert mt_service.is_valid_username("x" * 20) is True

    def test_invalid_empty(self):
        assert mt_service.is_valid_username("") is False

    def test_invalid_space(self):
        assert mt_service.is_valid_username("a b") is False

    def test_invalid_at_sign(self):
        assert mt_service.is_valid_username("user@name") is False

    def test_invalid_too_long(self):
        assert mt_service.is_valid_username("x" * 21) is False


class TestGetCardStatsFromProfile:
    FULL_PROFILE = {
        "data": {
            "name": "testuser",
            "personalBests": {
                "time": {
                    "15": [{"wpm": 120, "acc": 97, "language": "english"}],
                    "30": [{"wpm": 115, "acc": 96, "language": "english"}],
                },
                "words": {
                    "10": [{"wpm": 130, "acc": 98, "language": "english"}],
                    "50": [{"wpm": 125, "acc": 95, "language": "english"}],
                },
            },
            "typingStats": {"timeTyping": 3661},
        }
    }

    def test_full_data(self):
        stats = mt_service.get_card_stats_from_profile(self.FULL_PROFILE, 15, 10)
        assert stats["time_wpm"] == 120
        assert stats["time_acc"] == 97
        assert stats["words_wpm"] == 130
        assert stats["words_acc"] == 98
        assert stats["time_typing"] == "01:01:01"

    def test_missing_time_bucket(self):
        profile = {
            "data": {
                "personalBests": {
                    "time": {},
                    "words": {
                        "10": [{"wpm": 130, "acc": 98}],
                    },
                },
                "typingStats": {"timeTyping": 0},
            }
        }
        stats = mt_service.get_card_stats_from_profile(profile, 15, 10)
        assert stats["time_wpm"] == "--"
        assert stats["time_acc"] == "--"
        assert stats["words_wpm"] == 130
        assert stats["words_acc"] == 98

    def test_missing_word_bucket(self):
        profile = {
            "data": {
                "personalBests": {
                    "time": {
                        "15": [{"wpm": 120, "acc": 97}],
                    },
                    "words": {},
                },
                "typingStats": {"timeTyping": 0},
            }
        }
        stats = mt_service.get_card_stats_from_profile(profile, 15, 10)
        assert stats["time_wpm"] == 120
        assert stats["time_acc"] == 97
        assert stats["words_wpm"] == "--"
        assert stats["words_acc"] == "--"

    def test_both_missing(self):
        profile = {
            "data": {
                "personalBests": {"time": {}, "words": {}},
                "typingStats": {"timeTyping": 0},
            }
        }
        stats = mt_service.get_card_stats_from_profile(profile, 15, 10)
        assert stats["time_wpm"] == "--"
        assert stats["time_acc"] == "--"
        assert stats["words_wpm"] == "--"
        assert stats["words_acc"] == "--"
