from unittest.mock import patch

import app as app_module


class TestThemeToCardColors:
    def test_with_all_optional_keys(self):
        theme = {
            "bgColor": "#111",
            "textColor": "#eee",
            "mainColor": "#f00",
            "subColor": "#888",
            "subAltColor": "#222",
            "caretColor": "#0f0",
        }
        colors = app_module.theme_to_card_colors(theme)
        assert colors["page_bg"] == "#222"
        assert colors["card_bg"] == "#111"
        assert colors["border"] == "#888"
        assert colors["fg"] == "#eee"
        assert colors["muted"] == "#888"
        assert colors["accent"] == "#f00"
        assert colors["accent2"] == "#0f0"

    def test_with_missing_optional_keys(self):
        theme = {
            "bgColor": "#111",
            "textColor": "#eee",
            "mainColor": "#f00",
        }
        colors = app_module.theme_to_card_colors(theme)
        assert colors["page_bg"] == "#111"  # fallback to bgColor
        assert colors["border"] == "#2b3340"  # fallback
        assert colors["muted"] == "#7b8494"  # fallback
        assert colors["accent2"] == "#f00"  # fallback to mainColor


class TestRenderErrorSvg:
    THEME = {
        "page_bg": "#111",
        "card_bg": "#222",
        "border": "#333",
        "fg": "#eee",
        "muted": "#888",
        "accent": "#f00",
        "accent2": "#0f0",
    }

    def test_returns_valid_svg(self):
        svg = app_module.render_error_svg("something broke", self.THEME)
        assert svg.strip().startswith("<svg")
        assert "something broke" in svg

    def test_escapes_html_entities(self):
        svg = app_module.render_error_svg("<script>alert('xss')</script>", self.THEME)
        assert "<script>" not in svg
        assert "&lt;script&gt;" in svg

    def test_uses_theme_colors(self):
        svg = app_module.render_error_svg("err", self.THEME)
        assert "#111" in svg  # page_bg
        assert "#222" in svg  # card_bg
        assert "#888" in svg  # muted
        assert "#f00" in svg  # accent


class TestIsRateLimited:
    def test_under_limit_returns_false(self):
        assert app_module._is_rate_limited("1.2.3.4") is False

    def test_at_limit_returns_true(self):
        ip = "1.2.3.4"
        for _ in range(30):
            app_module._is_rate_limited(ip)
        assert app_module._is_rate_limited(ip) is True

    def test_window_expiry(self):
        ip = "1.2.3.4"
        base_time = 1000000.0

        with patch("app.time_mod.time") as mock_time:
            # Fill up 30 requests at base_time
            mock_time.return_value = base_time
            for _ in range(30):
                app_module._is_rate_limited(ip)

            # 30th+ call should be limited
            mock_time.return_value = base_time
            assert app_module._is_rate_limited(ip) is True

            # Advance past the window
            mock_time.return_value = base_time + 61
            assert app_module._is_rate_limited(ip) is False

    def test_ip_eviction(self):
        original_max = app_module.RATE_LIMIT_MAX_IPS
        try:
            # Eviction happens before the new entry is appended, so we need
            # MAX+2 IPs to ensure the oldest gets evicted.
            app_module.RATE_LIMIT_MAX_IPS = 2
            for i in range(4):
                app_module._is_rate_limited(f"10.0.0.{i}")

            # Oldest IPs should have been evicted, only 2 remain + the new one
            assert "10.0.0.0" not in app_module._rate_limits
            assert "10.0.0.3" in app_module._rate_limits
        finally:
            app_module.RATE_LIMIT_MAX_IPS = original_max
