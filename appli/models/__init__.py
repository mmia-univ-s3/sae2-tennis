from appli.app import login_manager

@login_manager.user_loader
def load_user(_: str):
    pass
