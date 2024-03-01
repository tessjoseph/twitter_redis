from website import create_app, views, auth, create_dashboard

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
