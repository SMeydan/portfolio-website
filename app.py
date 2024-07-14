from flask import Flask, jsonify, request
from portfoliosude.lnkdn_scrape import scrape_linkedin, get_github_profile, get_google_drive_files

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def api():
    return jsonify({'message': 'Hello, World!'})

@app.route('/api/linkedin', methods=['GET'])
def linkedin_profile():
    try:
        experiences, education_list = scrape_linkedin()
        return jsonify({
            'experiences': experiences,
            'education': education_list
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/github', methods=['GET'])
def github_profile():
    try:
        profile_data, repos = get_github_profile()
        return jsonify({
            'profile': profile_data,
            'repositories': repos
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/google-drive', methods=['GET'])
def google_drive_files():
    try:
        files = get_google_drive_files()
        return jsonify(files)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
