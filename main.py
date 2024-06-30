from flet import Page, app
from src.auth.login import LoginScreen
from src.auth.register import RegisterScreen
from src.auth.reset_password import ResetPasswordScreen
from src.home.home import HomeScreen
from src.upload.upload import UploadScreen
from src.results.results import ResultsScreen

def main(page: Page):
    page.title = "Multi-Platform App"
    page.window_width = 800
    page.window_height = 600
    
    login_screen = LoginScreen(page)
    register_screen = RegisterScreen(page)
    reset_password_screen = ResetPasswordScreen(page)
    home_screen = HomeScreen(page)
    upload_screen = UploadScreen(page)
    results_screen = ResultsScreen(page)

    # # 初期画面はログイン画面
    # page.go("/login")

    # DEBUG: ログイン画面をスキップしてホーム画面に遷移
    page.go("/home")

    # ルートを設定
    page.routes = {
        "/login": login_screen,
        "/register": register_screen,
        "/reset_password": reset_password_screen,
        "/home": home_screen,
        "/upload": upload_screen,
        "/results": results_screen
    }

if __name__ == "__main__":
    app(target=main)
