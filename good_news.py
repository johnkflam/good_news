from fasthtml.common import *
import good_news_views as gvw
from translator import DocumentTranslator

styles = Style("""
.container {
    width: 80%;
    margin: 20px ; /* optional: centers the container */             
}
               
form {
    width: 80%;
    margin: 20px;
               }
               
""")


port = 8001
app, rt = fast_app(pico=True,live=True,
                   hdrs=[gvw.styles])

uploaded_filename=''
translator=None



upload_dir = Path("filez")
upload_dir.mkdir(exist_ok=True)

@rt('/upload',methods=['POST'])
async def upload(file: UploadFile):
    card = FileMetaDataCard(file)
    filebuffer = await file.read()
    (upload_dir / file.filename).write_bytes(filebuffer)
    return card


@rt('/translate',methods=['POST'])
def translate(source_text:str):
    trn = DocumentTranslator()
    processed_text = trn.translate_text(source_text)
    # processed_text = source_text
    return Div(
        P(f"Original: {source_text}", style="margin-bottom: 10px;"),
        P(f"Result: {processed_text}", style="font-weight: bold; color: green;"),
        style="padding: 10px;"
    )

@rt
async def upload(file: UploadFile):
    global uploaded_filename
    card = FileMetaDataCard(file)
    filebuffer = await file.read()
    (upload_dir / file.filename).write_bytes(filebuffer)
    uploaded_filename=file.filename
    return card

def upload_page():
    return Div(
    gvw.Header('Upload File'),
    gvw.upload_form(),
    gvw.Footer('COPYRIGHT @2025'))
      
def FileMetaDataCard(file):
    return Article(
        gvw.Header(H3(file.filename)),
        Ul(
            Li('Size: ', file.size),            
            Li('Content Type: ', file.content_type),
            Li('Headers: ', file.headers),
        )
    )    

# @rt('/')
# def index():
#     return Titled('Click to test',
#                      Button('click', hx_get='/click', hx_target='#dest'),
#                      Div(id='dest'))

@rt('/')
def click():
    # return login_page()
    return gvw.contributor_form()

@rt('/contributor_action')
def contributor_action(create_or_upload:str):
    if create_or_upload=='create':
        return Redirect("/contributor_create")
    elif create_or_upload=='upload':
        return Redirect("/contributor_upload")
    
@rt('/contributor_create')
def contributor_create():
    return Titled("Translation Page",
           A('back',href='/'),
           gvw.translation_form())
    

@rt('/contributor_upload')
def contributor_upload():
    # return gvw.upload_page()
    return gvw.upload_and_translate_page()

def get_hendi_name(file_name):
    lst=file_name.split('.')
    return lst[0] + '_hendai.' + lst[1]

@rt('/translate_uploaded_doc',methods=['POST'])
def translate_uploaded_doc(file_name:str):
    global translator
    in_path = os.path.join(upload_dir,file_name)
    out_path = os.path.join(upload_dir,get_hendi_name(file_name))
    if translator is None:
        translator = DocumentTranslator()

    processed_text = translator.translate_document(in_path,out_path)
    return Div(
        # P(f"Original: {source_text}", style="margin-bottom: 10px;"),
        P(f"Result: {processed_text}", style="font-weight: bold; color: green;"),
        style="padding: 10px;"
    )

serve()