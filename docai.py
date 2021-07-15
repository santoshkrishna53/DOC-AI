def process_document_sample():
    project_id = 'springmltraining-316807',
    location = 'us',
    processor_id ='bd79c9b4cddb3b20', 
    file_path ='PMI-474082-2.pdf'
    from google.cloud import documentai_v1 as documentai

    # You must set the api_endpoint if you use a location other than 'us', e.g.:
    opts = {}
    if location == "eu":
        opts = {"api_endpoint": "eu-documentai.googleapis.com"}

    client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor, e.g.:
    # projects/project-id/locations/location/processor/processor-id
    # You must create new processors in the Cloud Console first
    name = f"projects/162814032533/locations/us/processors/488551e889699ece"

    with open(file_path, "rb") as image:
        image_content = image.read()

    # Read the file into memory
    document = {"content": image_content, "mime_type": "application/pdf"}

    # Configure the process request
    request = {"name": name, "raw_document": document}

    # Recognizes text entities in the PDF document
    result = client.process_document(request=request)

    document = result.document


    document_pages = document.pages

    # Read the text recognition output from the processor
    form_dict = {}
    for page in document_pages:
        formFields = page.form_fields
        for formField in formFields:
            fieldName=get_text(formField.field_name,document).strip()
            fieldValue = get_text(formField.field_value,document).strip()
            form_dict[fieldName]=fieldValue
    print('the extracted values fdrom the document are : ')
    print(form_dict)




# Extract shards from the text field
def get_text(doc_element: dict, document: dict):
    """
    Document AI identifies form fields by their offsets
    in document text. This function converts offsets
    to text snippets.
    """
    response = ""
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    for segment in doc_element.text_anchor.text_segments:
        start_index = (
            int(segment.start_index)
            if segment in doc_element.text_anchor.text_segments
            else 0
        )
        end_index = int(segment.end_index)
        response += document.text[start_index:end_index]
    return response

process_document_sample()