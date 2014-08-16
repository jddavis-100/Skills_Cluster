admin.add_view(sqla.ModelView(Tag, db.session))
admin.add_view(PostAdmin(db.session))
admin.add_view(TreeView(Tree, db.session))

def build_sample_db():
    """
    Populate a small db with some example entries.
    """

    import random
    import datetime

    db.drop_all()
    db.create_all()

    # Create sample Users
    primary_term = [
        'C++', 'C++', 'C++', 'Java', 'Java' 
    ]
    secondary_term = [
        'SQL Server', 'MVC', 'ASP.NET', 'Spring', 'Hibernate'
    ]

    number_of_times = [1, 10, 50, 60, 1000]
    for i in range(len(first_names)):
        skillspair = SkillsPair()
        skillspair.primary_term = primary_term[i]
        skillspair.primary_term = primary_term[i].lower()
        skillspair.secondary_term = secondary_term[i]
        skillspair.secondary_term = secondary_term[i].lower()
        skillspair.number_of_times = number_of_times[i]
        db.session.add(skillspair)


    db.session.commit()
    return

if __name__ == '__main__':
    # Build a sample db on the fly, if one does not exist yet.
    app_dir = op.realpath(os.path.dirname(__file__))
    database_path = op.join(app_dir, app.config['DATABASE_FILE'])
    if not os.path.exists(database_path):
        build_sample_db()

    # Start app
    app.run(debug=True)
