from fasthtml.common import *

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

upload_dir = Path("filez")
upload_dir.mkdir(exist_ok=True)

def translation_form():
    return Form(
                Div(
                    Label("Source Text:", For="source_text"),
                    Textarea(
                        name="source_text", 
                        id="source_text",
                        placeholder="Enter text to translate...",
                        rows="6",
                        style="width: 100%; margin: 10px 0;"
                    )
                ),
                Button("Continue", type="submit", style="margin: 10px 0; padding: 10px 20px;"),
                Div(id='target_text'),
                action="/translate",
                method="post",
                hx_post="/translate",
                hx_target="#target_text",
                hx_swap="innerHTML"
            )


def Header(title):
    return Div(H1(title, cls="text-2xl font-bold mb-4"), cls="header")

def login_form():
    return Div(
        Form(method="post", action="/login")(
            Fieldset(
                Label('Email', Input(name="user",size='20')),
                Label('Password', Input(name="password", type="password", placeholder='minimum 8 characters with numbers and characters')),
                Details(
                   Summary('Roles'),
                   Ul(
                       Li(A("Contributor", href="#")),
                       Li(A("Validator", href="#")),
                       Li(A("Distributor", href="#"))
                   ),cls="dropdown",Style={'width':'50%'})
            ),
        P(A('Forgot Password',href='#')),
        P(A('Create Account',href='#'))
        )
            
    )

def Footer(info):
    return  Div(P(info, cls="text-sm text-gray-600"), A('home',href='/'), cls="footer")

def login_page():
    return Div(
        Header('Welcome to Good News Boardcaster'),
        login_form(),
        Footer('COPYRIGHT @2025'))

def role_dropdown():
    return Details(
                   Summary('Roles'),
                   Ul(
                       Li(A("Contributor", href="#")),
                       Li(A("Validator", href="#")),
                       Li(A("Distributor", href="#"))
                   ),cls="dropdown",Style={'width':'50%'})

def contributor_form():
    return Html(
        Head(styles),
        Body(
        Form(method="post", action="/contributor_action")(
            H3('I am a contributor, I want to...'),
            Div(
                 Input('create a new document',type='radio', name='create_or_upload', value='create' ),
                Input('upload a file', type='radio', name='create_or_upload', value='upload')
                 ),
            Button('Next'),cls='container'))
    )

def edit_content_page():
    return Div(
    Header('Edit Content'),
    edit_content_form(),
    Footer('COPYRIGHT @2025'))

def edit_content_form():
       return Div(
        Form(method="post", action="/edit_content")(
            Label('Document Name', Input(name='doc_name', placeholder="Document Name")),
            Label('Edit Content', Textarea(name="doc", rows="20", placeholder="Enter content")),
            Group(P(Button("Translate")),P(Button("Discard")))
    ))

def upload_form():
    return Article(
            Form(hx_post='/upload', hx_target="#result-one")(
                Input(type="file", name="file"),
                Button("Upload", type="submit", cls='secondary'),
            ),
            Div(id="result-one")
        )

def upload_page():
    return Div(
    Header('Upload File'),
    upload_form(),
    Footer('COPYRIGHT @2025'),cls='container')

def FileMetaDataCard(file):
    return Article(
        Header(H3(file.filename)),
        Ul(
            Li('Size: ', file.size),            
            Li('Content Type: ', file.content_type),
            Li('Headers: ', file.headers),
        )
    )    

def source_and_target_view():
    return Card(
                    Grid(
                        Form(
                            Label('file name',Input(name='file_name',size='20')),
                            Button('Translate',hx_post='/translate_uploaded_doc',hx_target='#result')
                        )
                    ),Style('{width:80%}'),
                    Div(id='result')
                )

def upload_and_translate_page():
    return Div(
        Header('Upload and translate'),
        Grid(upload_form(),
            source_and_target_view()),
        Footer('Copyright @2025'),
        cls='container')

