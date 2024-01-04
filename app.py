from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric, func
from datetime import datetime
from sqlalchemy import or_
import os
import mimetypes
from werkzeug.utils import secure_filename
app = Flask(__name__)
# Set a secret key for the Flask app
app.secret_key = 'your_secret_key_here'
ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:nbtc2023@localhost/agendadb'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = 'uploads'
VIDEO_FOLDER = 'video'
IMAGE_FOLDER = 'image'
AUDIO_FOLDER = 'audio'
DOC_FOLDER = 'doc'
EXCEL_FOLDER = 'excel'
POWERPOINT_FOLDER = 'powerpoint'

ALLOWED_EXTENSIONS = {'mp4', 'mkv', 'png', 'jpg', 'jpeg', 'gif', 'mp3', 'wav', 'doc', 'docx', 'pdf', 'csv', 'xls', 'xlsx', 'ppt', 'pptx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['VIDEO_FOLDER'] = os.path.join(UPLOAD_FOLDER, VIDEO_FOLDER)
app.config['IMAGE_FOLDER'] = os.path.join(UPLOAD_FOLDER, IMAGE_FOLDER)
app.config['AUDIO_FOLDER'] = os.path.join(UPLOAD_FOLDER, AUDIO_FOLDER)
app.config['DOC_FOLDER'] = os.path.join(UPLOAD_FOLDER, DOC_FOLDER)
app.config['EXCEL_FOLDER'] = os.path.join(UPLOAD_FOLDER, EXCEL_FOLDER)
app.config['POWERPOINT_FOLDER'] = os.path.join(UPLOAD_FOLDER, POWERPOINT_FOLDER)
app.config['PDF_FOLDER'] = os.path.join(UPLOAD_FOLDER, 'pdf')

saved_filenames = []

db = SQLAlchemy(app)
app.app_context().push()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_folder_for_file(file_type):
    if file_type.startswith('video'):
        return app.config['VIDEO_FOLDER']
    elif file_type.startswith('image'):
        return app.config['IMAGE_FOLDER']
    elif file_type.startswith('audio'):
        return app.config['AUDIO_FOLDER']
    elif file_type.startswith('application/vnd.openxmlformats-officedocument.wordprocessingml.document'):
        return app.config['DOC_FOLDER']
    elif file_type.startswith('application/vnd.ms-excel') or file_type.startswith('text/csv'):
        return app.config['EXCEL_FOLDER']
    elif file_type.startswith('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'):
        return app.config['EXCEL_FOLDER']
    elif file_type.startswith('application/vnd.ms-powerpoint') or file_type.startswith('application/vnd.openxmlformats-officedocument.presentationml.presentation'):
        return app.config['POWERPOINT_FOLDER']
    elif file_type.startswith('application/pdf'):
        return app.config['PDF_FOLDER']
    else:
        return app.config['UPLOAD_FOLDER']

class Agenda(db.Model):
    __tablename__ = 'agenda'
    meeting_id = db.Column(db.Integer, primary_key=True)
    meeting_count = db.Column(db.Integer)
    workyear = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    agenda_number = db.Column(Numeric(precision=3, scale=1))
    purpose = db.Column(db.String(200))
    agenda_name = db.Column(db.String(200))
    resolution = db.Column(db.String(200))
    note = db.Column(db.String(200))
    department = db.Column(db.String(200))
    status = db.Column(db.String(200))
    is_first_time = db.Column(db.Boolean)
    related_meeting = db.Column(db.Integer)
    committee = db.Column(db.String(200))

    def __init__(self, meeting_id, meeting_count, workyear, date, agenda_number, purpose ,agenda_name, resolution, note, department, status, is_first_time, related_meeting, committee):
        self.meeting_id     = meeting_id     
        self.meeting_count  = meeting_count  
        self.workyear       = workyear       
        self.date           = date           
        self.agenda_number  = agenda_number  
        self.purpose        = purpose        
        self.agenda_name    = agenda_name    
        self.resolution     = resolution     
        self.note           = note           
        self.department     = department     
        self.status         = status         
        self.is_first_time  = is_first_time  
        self.related_meeting= related_meeting
        self.committee      = committee          

@app.route('/uploads/<filename>')
def view_file(filename):
    uploads_path = app.config['UPLOAD_FOLDER']
    file_path = os.path.join(uploads_path, filename)
    file_type, _ = mimetypes.guess_type(file_path)

    if file_type:
        if file_type.startswith('video'):
            return render_template('video_preview.html', filename=filename)
        elif file_type.startswith('image'):
            return render_template('image_preview.html', filename=filename)
        elif file_type.startswith('audio'):
            return render_template('audio_preview.html', filename=filename)
        elif file_type.startswith('application/vnd.openxmlformats-officedocument.wordprocessingml.document'):
            return render_template('doc_preview.html', filename=filename)
        elif file_type.startswith('application/vnd.ms-excel') or file_type.startswith('text/csv'):
            return render_template('excel_preview.html', filename=filename)
        elif file_type.startswith('application/vnd.openxmlformats-officedocument.presentationml.presentation'):
            return render_template('powerpoint_preview.html', filename=filename)
        elif file_type.startswith('application/pdf'):
            return render_template('pdf_preview.html', filename=filename)

    # If the file type is not supported for preview, serve it for download
    return send_from_directory(uploads_path, filename, as_attachment=True)


@app.route('/get_meeting_data', methods=['POST'])
def get_meeting_data():
    # Fetch data from the database using SQLAlchemy
    meetings = Agenda.query.all()

    # You can customize the data retrieval logic based on your requirements

    # Convert the meetings data to a list of dictionaries for easy rendering in HTML
    meetings_data = [
        {
            'Meeting ID': meeting.meeting_id,
            'Meeting Count': meeting.meeting_count,
            'Work Year': meeting.workyear,
            'Date': meeting.date,
            'Agenda Number': meeting.agenda_number,
            'Purpose': meeting.purpose,
            'Agenda Name': meeting.agenda_name,
            'Resolution': meeting.resolution,
            'Note': meeting.note,
            'Department': meeting.department,
            'Status': meeting.status,
            'Is First Time': meeting.is_first_time,
            'Related Meeting': meeting.related_meeting,
            'Committee': meeting.committee
        }
        for meeting in meetings
    ]
    # print('Meetings data:', meetings_data)

    # Return the meeting data as JSON
    return jsonify(meetings_data)

@app.route('/')
def index():
    # Get column names from the Feedback model
    columns = Agenda.__table__.columns.keys()

    # Get all rows from the Feedback model
    rows = Agenda.query.all()

    # Convert rows to a list of dictionaries for easier rendering in the template
    # rows_data = [{column: getattr(row, column) for column in columns} for row in rows]

    return render_template('index.html', columns=columns, rows=rows)

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    # Get the row from the database based on the ID
    row = Agenda.query.get(id)

    if row is None:
        return redirect(url_for('index'))

    # Get column names and types
    columns_info = {column.name: (column.name, str(column.type)) for column in Agenda.__table__.columns}

    # Update the row in the database (you need to implement the form and validation)
    if request.method == 'POST':
        for column, (column_name, column_type) in columns_info.items():
            if column_type == 'BOOLEAN':
                setattr(row, column, request.form.get(column) == 'on')
            elif column_type == 'DATETIME':
                date_str = request.form[column]
                setattr(row, column, datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None)
            elif column_type == 'NUMERIC':
                # Handle the case where the numeric field is not provided
                setattr(row, column, float(request.form[column]) if request.form[column] else None)
            elif column_type == 'INTEGER':
                # Handle the case where the integer field is not provided
                setattr(row, column, int(request.form[column]) if request.form[column] else None)
            else:
                setattr(row, column, request.form[column])

        db.session.commit()
        return redirect(url_for('index'))

    return render_template('edit.html', columns_info=columns_info, row=row)

@app.route('/addrelated/<int:id>', methods=['GET', 'POST'])
def addrelated(id):
    # Get the row from the database based on the ID
    row = Agenda.query.get(id)
    max_meeting_id = db.session.query(func.max(Agenda.meeting_id)).scalar()

    if row is None:
        return redirect(url_for('index'))

    # Get column names and types
    columns_info = {column.name: (column.name, str(column.type)) for column in Agenda.__table__.columns}

    # Update the row in the database (you need to implement the form and validation)
    if request.method == 'POST':
        meeting_id      = max_meeting_id + 1
        meeting_count   = request.form['meeting_count']
        workyear        = request.form['workyear']
        date            = request.form['date']
        agenda_number   = request.form['agenda_number']
        purpose         = request.form['purpose']
        agenda_name     = request.form['agenda_name']
        resolution      = request.form['resolution']
        note            = request.form['note']
        department      = request.form['department']
        status          = request.form['status']
        is_first_time   = False
        related_meeting = id
        committee       = request.form['committee']
        # print(customer, dealer, rating, comments)
        if meeting_id == '' or agenda_name == '':
            return render_template('add_related.html', message='Please enter required fields')
        
        # Handle boolean values
        is_first_time = request.form.get('is_first_time') == 'on'
        
        
        # Handle the case where the date is not provided
        date_str = request.form['date']
        date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        data = Agenda(meeting_id, meeting_count, workyear, date, agenda_number, purpose ,agenda_name, resolution, note, department, status, is_first_time, related_meeting, committee)
        db.session.add(data)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('add_related.html', columns_info=columns_info, row=row)

@app.route('/search')
def search():
    search_term = request.args.get('searchTerm', '')
    print(f'search_term: {search_term}')
    
    # Build a list of conditions for each column you want to search
    conditions = [

        Agenda.purpose.ilike(f"%{search_term}%"),
        Agenda.agenda_name.ilike(f"%{search_term}%"),
        Agenda.resolution.ilike(f"%{search_term}%"),
        Agenda.note.ilike(f"%{search_term}%"),
        Agenda.department.ilike(f"%{search_term}%"),
        Agenda.status.ilike(f"%{search_term}%"),
        Agenda.committee.ilike(f"%{search_term}%"),
    ]
    print(f'conditions: {conditions}')
    columns_info = {column.name: (column.name, str(column.type)) for column in Agenda.__table__.columns}
    # Combine conditions with OR to match any of them
    search_filter = or_(*conditions)

    # Use the filter in your query
    filtered_rows = Agenda.query.filter(search_filter).all()

    return render_template('index.html', rows=filtered_rows, columns=columns_info)

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     print("upload called *********")
#     print(request.files)
#     # Check if the 'file' field is in the request files
#     if 'files[]' not in request.files:
#         return 'No file part'
#     print(request.files)
#     # Get the list of files uploaded
#     files = request.files.getlist('files[]')
# 
#     for file in files:
#         if file.filename == '':
#             return 'No selected file'
# 
#         if file and allowed_file(file.filename):
#             file_type = mimetypes.guess_type(file.filename)[0]
#             folder = get_folder_for_file(file_type)
# 
#             if not os.path.exists(folder):
#                 os.makedirs(folder)
# 
#             filename = os.path.join(folder, secure_filename(file.filename))
#             file.save(filename)
# 
#     return 'Files uploaded successfully'


@app.route('/upload', methods=['POST'])
def upload_file():
    print("upload called *********")
    print(request.files)

    global saved_filenames

    # Check if the 'file' field is in the request files
    if 'files[]' not in request.files:
        return 'No file part'
    
    # Get the meeting_id from the request
    # meeting_id = request.form['meeting_id']

    print(request.files)
    # print(f'meeting_id: {meeting_id}')
    
    # Get the list of files uploaded
    files = request.files.getlist('files[]')

    for file in files:
        if file.filename == '':
            return 'No selected file'

        if file and allowed_file(file.filename):
            file_type = mimetypes.guess_type(file.filename)[0]
            folder = get_folder_for_file(file_type)

            if not os.path.exists(folder):
                os.makedirs(folder)

            filename = os.path.join(folder, secure_filename(file.filename))
            file.save(filename)
            saved_filenames.append(filename)
            print(f"upload func saved_filenames: {saved_filenames}")

    return saved_filenames

@app.route('/images')
def list_images():
    image_folder = app.config['IMAGE_FOLDER']
    image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
    return render_template('image_list.html', image_files=image_files)

@app.route('/uploads/image/<filename>')
def view_image(filename):
    return send_from_directory(app.config['IMAGE_FOLDER'], filename)

@app.route('/add', methods=['GET', 'POST'])
def add():
    global saved_filenames
    print(f"add func saved_filenames: {saved_filenames}")
    max_meeting_id = db.session.query(func.max(Agenda.meeting_id)).scalar()
    columns_info = {column.name: (column.name, str(column.type)) for column in Agenda.__table__.columns}

    if request.method == 'POST':
        meeting_id      = max_meeting_id + 1 if max_meeting_id is not None else 1
        meeting_count   = request.form['meeting_count'] if request.form['meeting_count']!= '' else None
        workyear        = request.form['workyear'] if request.form['workyear']!= '' else None
        date            = request.form['date'] if request.form['date']!= '' else None
        agenda_number   = request.form['agenda_number'] if request.form['agenda_number']!= '' else None
        purpose         = request.form['purpose'] if request.form['purpose']!= '' else None
        agenda_name     = request.form['agenda_name'] if request.form['agenda_name']!= '' else None
        resolution      = request.form['resolution'] if request.form['resolution']!= '' else None
        # note            = request.form['note'] if request.form['note']!= '' else None
        note            = saved_filenames
        department      = request.form['department'] if request.form['department']!= '' else None
        status          = request.form['status'] if request.form['status']!= '' else None
        is_first_time   = request.form['is_first_time']  if request.form['is_first_time']!= '' else None
        related_meeting = request.form['related_meeting'] if request.form['related_meeting']!= '' else None
        committee       = request.form['committee'] if request.form['committee']!= '' else None
        # print(customer, dealer, rating, comments)
        if meeting_id is None or agenda_name is None:
            return render_template('add.html', columns_info=columns_info, message='Please enter required fields')
        
        # Handle boolean values
        is_first_time = request.form.get('is_first_time') == 'on'
        
        # Validate is_first_time and related_meeting conditions
        if is_first_time and related_meeting is not None:
            return render_template('add.html', columns_info=columns_info, message='If is_first_time is True, related_meeting must be None.')

        if not is_first_time and related_meeting is None:
            return render_template('add.html', columns_info=columns_info, message='If is_first_time is False, related_meeting must be a number.')        
        
        # Handle the case where the date is not provided
        date_str = request.form['date']
        date = datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

        data = Agenda(meeting_id, meeting_count, workyear, date, agenda_number, purpose ,agenda_name, resolution, note, department, status, is_first_time, related_meeting, committee)
        db.session.add(data)
        db.session.commit()

        # Use the global variable directly
        print("Saved Filenames:", saved_filenames)

        # Clear the saved_filenames variable
        saved_filenames = []
        return redirect(url_for('index'))

    # Get column names and types

    return render_template('add.html', columns_info=columns_info)

def get_related_meetings(meeting_id, related_meetings=[]):
    print(f'related_meetings: {related_meetings}')
    current_meeting = Agenda.query.get(meeting_id)

    if current_meeting:
        related_meetings.append(current_meeting)

        # Recursively get related meetings
        if current_meeting.related_meeting is not None:
            get_related_meetings(current_meeting.related_meeting, related_meetings)

    return related_meetings

def get_related_meetings(meeting_id, related_meetings=[]):
    print(f'related_meetings: {related_meetings}')
    current_meeting = Agenda.query.get(meeting_id)

    if current_meeting:
        related_meetings.append(current_meeting.meeting_id)  # Only store the meeting_id

        # Recursively get related meetings
        if current_meeting.related_meeting is not None:
            get_related_meetings(current_meeting.related_meeting, related_meetings)

    return related_meetings

@app.route('/timeline/<int:id>', methods=['GET'])
def timeline(id):
    related_meetings = []
    # Get related meetings recursively
    related_meetings = get_related_meetings(id, related_meetings)
    print(related_meetings)
    
    # using list comprehension in the query
    related_meetings_2 = [meeting.meeting_id for meeting in Agenda.query.filter(Agenda.related_meeting.in_(related_meetings)).all()]
    print(related_meetings_2)

    merged_list = list(set(related_meetings + related_meetings_2))
    # return render_template('timeline.html', related_meetings=related_meetings)
    
    # Query for meetings with meeting_id in the specified list and sort by date and meeting count
    meetings = Agenda.query.filter(Agenda.meeting_id.in_(merged_list)).order_by(Agenda.date, Agenda.meeting_count).all()
    
    return render_template('sorted_meetings.html', meetings=meetings)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    # Get the row from the database based on the ID
    row = Agenda.query.get(id)

    if row:
        # Delete the row from the database
        db.session.delete(row)
        db.session.commit()
        flash('Row deleted successfully', 'success')
    else:
        flash('Row not found', 'error')

    return redirect(url_for('index'))
# @app.route('/submit', methods=['POST'])
# def submit():
#     if request.method == 'POST':
#         customer = request.form['customer']
#         dealer = request.form['dealer']
#         rating = request.form['rating']
#         comments = request.form['comments']
#         # print(customer, dealer, rating, comments)
#         if customer == '' or dealer == '':
#             return render_template('add.html', message='Please enter required fields')
#         if db.session.query(Feedback).filter(Feedback.customer==customer).count() == 0:
#             data = Feedback(customer, dealer, rating, comments)
#             db.session.add(data)
#             db.session.commit()
#             return render_template('add.html', message='You have already submitted feedback')

if __name__ == '__main__':
    app.debug = True
    app.run()