import customtkinter as ctk


class VideoPreview(ctk.CTkFrame):
    """Video preview area."""

    def __init__(self, master) -> None:
        super().__init__(master)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self._create_widgets()

    def _create_widgets(self) -> None:
        self.title_label = ctk.CTkLabel(
            self,
            text="Virtual Try-On Preview",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        self.title_label.pack(
            padx=20,
            pady=(20, 10)
        )

        self.video_label = ctk.CTkLabel(
            self,
            text="Camera Frame",
            width=800,
            height=500
        )

        self.video_label.pack(
            padx=20,
            pady=20,
            expand=True
        )

    def show_frame(self, image) -> None:
        """Display a processed video frame."""

        self.video_label.configure(
            image=image,
            text=""
        )

        self.video_label.image = image

