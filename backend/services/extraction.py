
import pymupdf


def extract_pages(pdf_bytes: bytes) -> list[dict]:
    """
    Extract text from a PDF, preserving page numbers.

    Args:
        pdf_bytes: Raw PDF file content.

    Returns:
        A list of dictionaries containing page numbers and text.

    Raises:
        ValueError: If the PDF is invalid, encrypted,
                    or contains no extractable text.
    """

    if not pdf_bytes:
        raise ValueError("The uploaded PDF is empty.")

    try:
        document = pymupdf.open(
            stream=pdf_bytes,
            filetype="pdf"
        )

        if document.needs_pass:
            document.close()
            raise ValueError("Password-protected PDFs are not supported.")

        pages = []

        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text").strip()

            if text:
                pages.append({
                    "page_number": page_number,
                    "text": text
                })

        document.close()

        if not pages:
            raise ValueError(
                "No extractable text found in the PDF."
            )

        return pages

    except ValueError:
        raise

    except Exception as exc:
        raise ValueError(
            "Unable to read the uploaded PDF."
        ) from exc
