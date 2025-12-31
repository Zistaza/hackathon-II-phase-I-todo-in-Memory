import pytest
from src.services.validation import validate_priority, validate_tags, validate_tag, validate_search_keyword
from src.exceptions import TaskValidationError


class TestValidationService:
    """Unit tests for the validation service functions."""

    def test_validate_priority_valid_values(self):
        """Test that valid priority values pass validation."""
        valid_priorities = ["high", "medium", "low"]

        for priority in valid_priorities:
            # Should not raise an exception
            validate_priority(priority)

    def test_validate_priority_invalid_values(self):
        """Test that invalid priority values raise TaskValidationError."""
        invalid_priorities = ["HIGH", "HIGH", "invalid", "urgent", "", "h", "med", "low123"]

        for priority in invalid_priorities:
            with pytest.raises(TaskValidationError) as exc_info:
                validate_priority(priority)
            assert "Priority must be one of: high, medium, low" in str(exc_info.value)

    def test_validate_tags_valid_list(self):
        """Test that valid tag lists pass validation."""
        valid_tag_lists = [
            [],
            ["work"],
            ["work", "home"],
            ["tag-with-hyphens"],
            ["tag_with_underscores"],
            ["tag123"]
        ]

        for tag_list in valid_tag_lists:
            # Should not raise an exception
            validate_tags(tag_list)

    def test_validate_tags_invalid_cases(self):
        """Test that invalid tag lists raise TaskValidationError."""
        # Test empty tag
        with pytest.raises(TaskValidationError) as exc_info:
            validate_tags(["", "valid"])
        assert "Tag cannot be empty" in str(exc_info.value)

        # Test whitespace-only tag
        with pytest.raises(TaskValidationError) as exc_info:
            validate_tags(["   ", "valid"])
        assert "Tag cannot be empty" in str(exc_info.value)

        # Test tag with spaces
        with pytest.raises(TaskValidationError) as exc_info:
            validate_tags(["valid", "with spaces"])
        assert "Tag cannot contain spaces" in str(exc_info.value)

        # Test multiple invalid tags
        with pytest.raises(TaskValidationError) as exc_info:
            validate_tags(["", "with spaces", "valid"])
        assert "Tag cannot be empty" in str(exc_info.value) or "Tag cannot contain spaces" in str(exc_info.value)

    def test_validate_single_tag_valid(self):
        """Test that valid single tags pass validation."""
        valid_tags = ["work", "home", "study", "tag-with-hyphens", "tag_with_underscores", "tag123"]

        for tag in valid_tags:
            # Should not raise an exception
            validate_tag(tag)

    def test_validate_single_tag_invalid_cases(self):
        """Test that invalid single tags raise TaskValidationError."""
        # Test empty tag
        with pytest.raises(TaskValidationError) as exc_info:
            validate_tag("")
        assert "Tag cannot be empty" in str(exc_info.value)

        # Test whitespace-only tag
        with pytest.raises(TaskValidationError) as exc_info:
            validate_tag("   ")
        assert "Tag cannot be empty" in str(exc_info.value)

        # Test tag with spaces
        with pytest.raises(TaskValidationError) as exc_info:
            validate_tag("with spaces")
        assert "Tag cannot contain spaces" in str(exc_info.value)

        # Test tab character in middle (this should NOT raise error since validation only checks for ' ' space)
        # Based on the actual implementation, only ' ' (space) is checked for, not other whitespace
        # So tab in middle should pass validation
        validate_tag("with\ttabs")  # Should pass since validation only checks for ' ' space

        # Test newline character in middle (should pass validation as well)
        validate_tag("with\nnewlines")  # Should pass since validation only checks for ' ' space

        # Test space at beginning - should be caught by space check
        with pytest.raises(TaskValidationError) as exc_info:
            validate_tag(" space-at-start")
        assert "Tag cannot contain spaces" in str(exc_info.value)

        # Test space at end - should be caught by space check
        with pytest.raises(TaskValidationError) as exc_info:
            validate_tag("space-at-end ")
        assert "Tag cannot contain spaces" in str(exc_info.value)

        # Test tab character in middle - should pass validation (no space, not empty after strip)
        validate_tag("with\ttabs")  # Should pass since validation only checks for ' ' space, not other whitespace

        # Test newline character in middle - should pass validation (no space, not empty after strip)
        validate_tag("with\nnewlines")  # Should pass since validation only checks for ' ' space, not other whitespace

        # Test just tab character - should fail empty check after strip
        with pytest.raises(TaskValidationError) as exc_info:
            validate_tag("\t")
        assert "Tag cannot be empty" in str(exc_info.value)

        # Test just newline character - should fail empty check after strip
        with pytest.raises(TaskValidationError) as exc_info:
            validate_tag("\n")
        assert "Tag cannot be empty" in str(exc_info.value)

        # Test mixed whitespace that becomes empty - should fail empty check after strip
        with pytest.raises(TaskValidationError) as exc_info:
            validate_tag("  \t  \n  ")
        assert "Tag cannot be empty" in str(exc_info.value)

    def test_validate_search_keyword_valid(self):
        """Test that valid search keywords pass validation."""
        valid_keywords = ["test", "word", "multiple words", "TeSt", "123", "test-with-special!@#"]

        for keyword in valid_keywords:
            # Should not raise an exception
            validate_search_keyword(keyword)

    def test_validate_search_keyword_invalid_cases(self):
        """Test that invalid search keywords raise TaskValidationError."""
        # Test empty keyword
        with pytest.raises(TaskValidationError) as exc_info:
            validate_search_keyword("")
        assert "Search keyword cannot be empty" in str(exc_info.value)

        # Test whitespace-only keyword
        with pytest.raises(TaskValidationError) as exc_info:
            validate_search_keyword("   ")
        assert "Search keyword cannot be empty" in str(exc_info.value)

        # Test tab-only keyword
        with pytest.raises(TaskValidationError) as exc_info:
            validate_search_keyword("\t\t")
        assert "Search keyword cannot be empty" in str(exc_info.value)

        # Test newline-only keyword
        with pytest.raises(TaskValidationError) as exc_info:
            validate_search_keyword("\n\n")
        assert "Search keyword cannot be empty" in str(exc_info.value)

    def test_validate_search_keyword_edge_cases(self):
        """Test edge cases for search keyword validation."""
        # Test single character
        validate_search_keyword("a")  # Should pass

        # Test single whitespace character
        with pytest.raises(TaskValidationError) as exc_info:
            validate_search_keyword(" ")
        assert "Search keyword cannot be empty" in str(exc_info.value)

    def test_validate_priority_case_sensitive(self):
        """Test that priority validation is case sensitive."""
        # These should fail (wrong case)
        with pytest.raises(TaskValidationError):
            validate_priority("High")
        with pytest.raises(TaskValidationError):
            validate_priority("HIGH")
        with pytest.raises(TaskValidationError):
            validate_priority("Medium")
        with pytest.raises(TaskValidationError):
            validate_priority("MEDIUM")
        with pytest.raises(TaskValidationError):
            validate_priority("Low")
        with pytest.raises(TaskValidationError):
            validate_priority("LOW")

    def test_validate_tags_with_special_characters(self):
        """Test tag validation with various special characters (should pass)."""
        # Special characters other than spaces should be allowed
        special_tags = ["tag!", "tag@", "tag#", "tag$", "tag%", "tag^", "tag&", "tag*",
                       "tag(", "tag)", "tag_", "tag-", "tag+", "tag=", "tag[", "tag]",
                       "tag{", "tag}", "tag|", "tag\\", "tag:", "tag;", "tag'", "tag\"",
                       "tag<", "tag>", "tag,", "tag.", "tag?", "tag/"]

        for tag in special_tags:
            # Should not raise an exception
            validate_tag(tag)

    def test_validate_tags_does_not_allow_spaces_anywhere(self):
        """Test that tags cannot contain space characters (but may allow other whitespace)."""
        # Only actual space ' ' characters should raise an error
        space_tags = [
            "tag with space",
        ]

        for tag in space_tags:
            with pytest.raises(TaskValidationError) as exc_info:
                validate_tag(tag)
            assert "Tag cannot contain spaces" in str(exc_info.value)

        # Other whitespace characters in the middle (like tabs, newlines) are only caught by the ' ' check
        # so "with\ttabs" would pass the space check but might fail the empty check if at start/end
        other_whitespace_tags = [
            "tag\twith-tab",  # Should pass the space check
            "tag\nwith-newline",  # Should pass the space check
            "tag\rwith-return",  # Should pass the space check
        ]

        for tag in other_whitespace_tags:
            # These should not raise an error for the space validation
            # They may raise an error for the empty check if they're just whitespace, but not for space check
            try:
                validate_tag(tag)
                # If no exception, that's fine
            except TaskValidationError as e:
                # If there's an exception, it should not be about spaces since these don't contain ' ' space
                assert "Tag cannot contain spaces" not in str(e)

        # Whitespace at the beginning or end should be caught by the space check for actual spaces
        # and by the empty check for other whitespace after stripping
        whitespace_at_edges = [
            " tag-at-start",  # Should fail space check
            "tag-at-end ",   # Should fail space check
        ]

        for tag in whitespace_at_edges:
            with pytest.raises(TaskValidationError) as exc_info:
                validate_tag(tag)
            assert "Tag cannot contain spaces" in str(exc_info.value)

        # Other whitespace at edges should pass validation if they have content after stripping
        # Only pure whitespace or whitespace that becomes empty after stripping should fail
        other_whitespace_with_content = [
            "\ttag-with-tab-at-start",
            "tag-with-tab-at-end\t",
            "\ntag-with-newline-at-start",
            "tag-with-newline-at-end\n",
        ]

        for tag in other_whitespace_with_content:
            # These should pass validation since they have content after stripping
            # and don't contain space characters
            validate_tag(tag)  # Should not raise an exception

        # Pure whitespace or whitespace that becomes empty after stripping should fail
        pure_whitespace = [
            "\t",
            "\n",
            "\r",
            "\f",
            "\u00A0",  # Non-breaking space
            "  \t  \n  ",
        ]

        for tag in pure_whitespace:
            with pytest.raises(TaskValidationError) as exc_info:
                validate_tag(tag)
            assert "Tag cannot be empty" in str(exc_info.value)