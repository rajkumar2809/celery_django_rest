class DemoRouter:
    """
    A router to control all database operations on models in the
    user application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read user models go to secondary.
        """
        if model._meta.app_label == 'eappeal_bse':
            return 'secondary'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write user models go to secondary.
        """
        if model._meta.app_label == 'eappeal_bse':
            return 'secondary'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the user app is involved.
        """
        if obj1._meta.app_label == 'eappeal_bse' or \
           obj2._meta.app_label == 'eappeal_bse':
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'secondary'
        database.
        """
        if app_label == 'eappeal_bse':
            return db == 'secondary'
        return None