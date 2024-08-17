from flask import Blueprint, request, jsonify, send_file
import pandas as pd
import matplotlib.pyplot as plt
import io

# Create a Blueprint instance
main = Blueprint('main', __name__)

# Route to upload CSV and generate image
@main.route('/upload-csv', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        try:
            # Read CSV file into DataFrame
            df = pd.read_csv(file)

            # Process the DataFrame and generate an image
            img = process_csv_and_generate_image(df)

            # Create an in-memory file object for the image
            img_io = io.BytesIO()
            img.save(img_io, format='PNG')
            img_io.seek(0)

            # Send the image file as response
            return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='output.png')

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'Invalid file type'}), 400

# Helper function to check if file type is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'csv'}

# Function to process CSV and generate image
def process_csv_and_generate_image(df):
    # Example processing: Create a bar plot from the DataFrame
    plt.figure()
    df.plot(kind='bar')
    plt.title('CSV Data Plot')
    plt.xlabel('Index')
    plt.ylabel('Values')

    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)

    return img
