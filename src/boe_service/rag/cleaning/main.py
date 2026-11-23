from boe_service.config import EXTRACTED_FOLDER_PATH, INDEXED_JSON_PATH
from boe_service.rag.cleaning.date_extractor import extract_date
from boe_service.rag.cleaning.helpers import (
    check_doc_type,
    create_meta_field,
    cut_text_start,
    get_summary,
    remove_footer,
    split_into_paragraphs,
    split_pages,
)
from boe_service.utils.json_utils import save_to_json


# Extract Text From All Reports And Save Them As JSON File
def clean_data_in_text_files():
    all_data = []
    for i in EXTRACTED_FOLDER_PATH.iterdir():
        # Work Only With MPS - Which Start From May 2022
        if check_doc_type(i.stem) != "mps":
            continue

        # Split Into Pages, Use First Page To Extract Dates, Join The Pages Into One Single Text
        pages = split_pages(i)
        dates = extract_date(pages[0], doc_type=check_doc_type(i.stem))
        whole_text = "".join([text for text, _ in (remove_footer(p) for p in pages)])
        whole_text = cut_text_start(whole_text)

        # Splitting Text Into Summary And Minutes Paragraphs.
        summary, minutes = get_summary(whole_text)

        # Append Summary Data
        data = create_meta_field(
            i.stem,
            dates["meeting_date"],
            dates["published_date"],
            "summary",
            summary,
            0,
        )
        if data:
            all_data.append(data)

        # Seperate Minutes Into Chunks Based On Paragraph Numbers, Append Them.
        chuncks = split_into_paragraphs(minutes)
        if len(chuncks) > 0:
            for c in chuncks:
                data = create_meta_field(
                    i.stem,
                    dates["meeting_date"],
                    dates["published_date"],
                    "minutes",
                    c[1],
                    c[0],
                )
                if data:
                    all_data.append(data)

    # Save Json
    save_to_json(all_data, INDEXED_JSON_PATH)


# Main Function
def main():
    clean_data_in_text_files()


if __name__ == "__main__":
    main()
