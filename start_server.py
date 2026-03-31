from weddindInvitation import initialize_csv, app

if __name__ == '__main__':
    initialize_csv()
    # Run without the Flask debug reloader so the server runs in a single process
    app.run(debug=False, use_reloader=False, host='127.0.0.1', port=5001)
