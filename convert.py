import docx
from typing import List
from pathlib import Path
from docx.shared import Cm


def save_as_docx(docx_filepath: Path, photo_paths: List[Path]):
    """ insert images into .docx file and save it """

    # delete docx file if exists
    if docx_filepath.exists():
        docx_filepath.unlink()

    document = docx.Document()

    # change margins of entire document
    for sect in document.sections:
        sect.left_margin = Cm(0.5)
        sect.right_margin = Cm(0.5)
        sect.top_margin = Cm(0.5)
        sect.bottom_margin = Cm(0.5)

    # insert photo(s)
    for photo_path in photo_paths:
        document.add_picture(str(photo_path), width=Cm(19))

        # delete unnecessary anymore photo
        photo_path.unlink()

    document.save(docx_filepath)
