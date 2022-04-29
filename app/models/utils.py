from app import db


class ModelMixin(object):

    def save(self):
        # Save this model to the database.
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        # Delete model from the database.
        db.session.delete(self)
        db.session.commit()
        return self

    @classmethod
    def clean(cls):
        # Delete all the models from the database
        count = 0
        for model in cls.query.all():
            count += 1
            model.delete()
        return count
# Add your own utility classes and functions here.
