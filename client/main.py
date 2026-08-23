import customtkinter as ctk

from client.ui.main_window import MainWindow


class VirtualTryOnApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Virtual Try-On")
        self.geometry("1200x720")

        self.main_window = MainWindow(
            self
        )

        self.main_window.pack(
            fill="both",
            expand=True
        )
