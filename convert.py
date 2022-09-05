import docx
from docx.shared import Cm
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MEDIA_FOLDER = BASE_DIR / 'media'
DOCX_FOLDER = BASE_DIR / 'documents'


def save_as_docx(user_name):
    """ insert image in .docx file and save it """
    document_path = DOCX_FOLDER / (user_name + '.docx')

    if document_path.exists():
        document_path.unlink()
        print('file deleted')

    photo_path = MEDIA_FOLDER / '1.jpg'

    document = docx.Document()
    document.add_picture(photo_path, width=Cm(19))

    # change margins of entire document
    for sect in document.sections:
        sect.left_margin = Cm(0.5)
        sect.right_margin = Cm(0.5)
        sect.top_margin = Cm(0.5)
        sect.bottom_margin = Cm(0.5)

    document.save(document_path)
    print('file saved')


if __name__ == '__main__':
    username = 'Думанський Дмитро'
    save_as_docx(username)
