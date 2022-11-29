from collections.abc import Sequence, Iterable

import string


class RegexToolkit:
    _alpha_chars: set[str] = set(string.ascii_letters)
    _digit_chars: set[str] = set(string.digits)

    _safe_chars: set[str] = _alpha_chars.union(_digit_chars).union(set(string.whitespace))
    _escapable_chars: set[str] = set(string.punctuation)

    @staticmethod
    def iter_sort_by_len(
        texts: Iterable[str],
        *,
        reverse: bool = True,
    ) -> Iterable[str]:
        """Iterate Texts Sorted by Length

        Args:
            texts (Iterable[str]): Strings to sort.
            reverse (bool, optional): Sort in descending order (longest to shortest). Defaults to True.

        Yields:
            str: Strings sorted by length.
        """
        for text in sorted(texts, key=len, reverse=reverse):
            yield text

    @staticmethod
    def sort_by_len(
        texts: Iterable[str],
        *,
        reverse: bool = True,
    ) -> tuple[str, ...]:
        """Strings Sorted by Length

        Args:
            texts (Iterable[str]): Strings to sort.
            reverse (bool, optional): Sort in descending order (longest to shortest). Defaults to True.

        Returns:
            tuple[str]: Strings sorted by length.
        """
        return tuple(RegexToolkit.iter_sort_by_len(texts, reverse=reverse))

    @staticmethod
    def ord_to_codepoint(ordinal: int) -> str:
        """Character Codepoint from Character Ordinal

        Args:
            ordinal (int): Character ordinal.

        Returns:
            str: Character codepoint.
        """
        return format(ordinal, "x").zfill(8)

    @staticmethod
    def codepoint_to_ord(codepoint: str) -> int:
        """Character Ordinal from Character Codepoint

        Args:
            codepoint (str): Character codepoint.

        Returns:
            int: Character ordinal.
        """
        return int(codepoint, 16)

    @staticmethod
    def char_to_codepoint(char: str) -> str:
        """Character Codepoint from Character

        Args:
            char (str): Character.

        Returns:
            str: Character codepoint.
        """
        return RegexToolkit.ord_to_codepoint(ord(char))

    @staticmethod
    def char_as_exp(char: str) -> str:
        """Create a re Regex Expression that Exactly Matches a Character

        Escape to avoid reserved character classes (i.e. \s, \S, \d, \D, \1, etc.).

        Args:
            char (str): Character to match.

        Returns:
            str: re expression that exactly matches the original character.
        """
        # Safe as-is
        if char in RegexToolkit._safe_chars:
            return char

        # Escape with backslash
        return f"\\{char}"

    @staticmethod
    def char_as_exp2(char: str) -> str:
        """Create a re2 Regex Expression that Exactly Matches a Character

        Args:
            char (str): Character to match.

        Returns:
            str: re2 expression that exactly matches the original character.
        """
        # Safe as-is
        if char in RegexToolkit._safe_chars:
            return char

        # Safe to escape with backslash
        if char in RegexToolkit._escapable_chars:
            return f"\\{char}"

        # Otherwise escape using the codepoint
        return "\\x{" + RegexToolkit.char_to_codepoint(char) + "}"

    @staticmethod
    def string_as_exp(text: str) -> str:
        """Create a re Regex Expression that Exactly Matches a String

        Args:
            text (str): String to match.

        Returns:
            str: re expression that exactly matches the original string.
        """
        return r"".join(map(RegexToolkit.char_as_exp, text))

    @staticmethod
    def string_as_exp2(text: str) -> str:
        """Create a re2 Regex Expression that Exactly Matches a String

        Args:
            text (str): String to match.

        Returns:
            str: re2 expression that exactly matches the original string.
        """
        return r"".join(map(RegexToolkit.char_as_exp2, text))

    @staticmethod
    def strings_as_exp(texts: Iterable[str]) -> str:
        """Create a re Regex expression that Exactly Matches Any One String

        Args:
            texts (Iterable[str]): Strings to match.

        Returns:
            str: re expression that exactly matches any one of the original strings.
        """
        return r"|".join(
            map(
                RegexToolkit.string_as_exp,
                RegexToolkit.iter_sort_by_len(texts, reverse=True),
            )
        )

    @staticmethod
    def strings_as_exp2(texts: Iterable[str]) -> str:
        """Create a re2 Regex expression that Exactly Matches Any One String

        Args:
            texts (Iterable[str]): Strings to match.

        Returns:
            str: re2 expression that exactly matches any one of the original strings.
        """
        return r"|".join(
            map(
                RegexToolkit.string_as_exp2,
                RegexToolkit.iter_sort_by_len(texts, reverse=True),
            )
        )

    @staticmethod
    def iter_char_range(first_codepoint: int, last_codepoint: int) -> Iterable[str]:
        """Iterate All Characters within a Range of Codepoints (Inclusive)

        Args:
            first_codepoint (int): Starting (first) codepoint.
            last_codepoint (int): Ending (last) codepoint.

        Yields:
            str: Character from within a range of codepoints.
        """
        for i in range(ord(first_codepoint), ord(last_codepoint) + 1):
            yield chr(i)

    @staticmethod
    def char_range(first_codepoint: int, last_codepoint: int) -> tuple[str, ...]:
        """Tuple of All Characters within a Range of Codepoints (Inclusive)

        Args:
            first_codepoint (int): Starting (first) codepoint.
            last_codepoint (int): Ending (last) codepoint.

        Returns:
            tuple[str, ...]: Characters within a range of codepoints.
        """
        return tuple(RegexToolkit.iter_char_range(first_codepoint, last_codepoint))

    @staticmethod
    def mask_span(text: str, span: Sequence, mask: str | None = None) -> str:
        """Slice and Mask a String using a Span

        Args:
            text (str): Text to slice.
            span (Sequence[int]): Domain of index positions (x1, x2) to mask from the text.
            mask (str, optional): Mask to insert when slicing. Defaults to None.

        Returns:
            str: Text with span replaced with the mask text.
        """
        # if mask is None:
        #     mask = ""
        #
        # return text[: span[0]] + mask + text[span[1] :]
        if mask is None:
            return text[: span[0]] + text[span[1] :]
        else:
            return text[: span[0]] + mask + text[span[1] :]

    @staticmethod
    def mask_spans(
        text: str,
        spans: Iterable[Sequence[int]],
        masks: Iterable[str] | None = None,
    ) -> str:
        """Slice and Mask a String using Multiple Spans

        Args:
            text (str): Text to slice.
            spans (Iterable[Sequence[int]]): Domains of index positions (x1, x2) to mask from the text.
            masks (Iterable[str], optional): Masks to insert when slicing. Defaults to None.

        Returns:
            str: Text with all spans replaced with the mask text.
        """
        if masks is None:
            # No masks
            for span in reversed(spans):
                text = RegexToolkit.mask_span(text, span, mask=None)
        else:
            # Has mask
            for span, mask in zip(reversed(spans), reversed(masks)):
                text = RegexToolkit.mask_span(text, span, mask=mask)

        return text

    @staticmethod
    def to_utf8(text: str) -> str:
        """Force UTF-8 Text Encoding

        Args:
            text (str): Text to encode.

        Returns:
            str: Encoded text.
        """
        return text.encode("utf-8").decode("utf-8")
