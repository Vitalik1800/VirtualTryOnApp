import customtkinter as ctk


class VirtualTryOnApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.title("Virtual Try-On")
        self.geometry("1200x720")

        self.label = ctk.CTkLabel(
            self,
            text="Virtual Try-On"
        )

        self.label.pack(
            padx=20,
            pady=20
        )
