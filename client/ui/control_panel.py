import customtkinter as ctk


class ControlPanel(ctk.CTkFrame):
    """Control panel of the application."""

    def __init__(
        self,
        master,
        on_start_camera=None,
        on_stop_camera=None,
        on_accessory_selected=None,
        on_save_try_on=None
    ) -> None:
        super().__init__(master)

        self.selected_category = "Glasses"

        self.on_start_camera = on_start_camera
        self.on_stop_camera = on_stop_camera
        self.on_accessory_selected = on_accessory_selected
        self.on_save_try_on = on_save_try_on

        self._create_widgets()

    def _create_widgets(self) -> None:
        self.accessory_label = ctk.CTkLabel(
            self,
            text="Accessories"
        )

        self.accessory_label.pack(
            padx=20,
            pady=(20, 10)
        )

        self.glasses_button = ctk.CTkButton(
            self,
            text="Glasses",
            command=lambda: self.select_category("Glasses")
        )

        self.glasses_button.pack(
            padx=20,
            pady=5
        )

        self.hats_button = ctk.CTkButton(
            self,
            text="Hats",
            command=lambda: self.select_category("Hats")
        )

        self.hats_button.pack(
            padx=20,
            pady=5
        )

        self.masks_button = ctk.CTkButton(
            self,
            text="Masks",
            command=lambda: self.select_category("Masks")
        )

        self.masks_button.pack(
            padx=20,
            pady=5
        )

        self.selected_label = ctk.CTkLabel(
            self,
            text=f"Selected: {self.selected_category}"
        )

        self.selected_label.pack(
            padx=20,
            pady=(15, 5)
        )

        self.camera_label = ctk.CTkLabel(
            self,
            text="Camera"
        )

        self.camera_label.pack(
            padx=20,
            pady=(30, 10)
        )

        self.start_button = ctk.CTkButton(
            self,
            text="Start Camera",
            command=self._start_camera
        )

        self.start_button.pack(
            padx=20,
            pady=5
        )

        self.stop_button = ctk.CTkButton(
            self,
            text="Stop Camera",
            command=self._stop_camera
        )

        self.stop_button.pack(
            padx=20,
            pady=5
        )

        self.additional_label = ctk.CTkLabel(
            self,
            text="Additional"
        )

        self.additional_label.pack(
            padx=20,
            pady=(30, 10)
        )

        self.save_try_on_button = ctk.CTkButton(
            self,
            text="Save Try-On",
            command=self.on_save_try_on
        )

        self.save_try_on_button.pack(
            padx=10,
            pady=10
        )

        self.capture_button = ctk.CTkButton(
            self,
            text="Capture"
        )

        self.capture_button.pack(
            padx=20,
            pady=5
        )

        self.record_button = ctk.CTkButton(
            self,
            text="Record"
        )

        self.record_button.pack(
            padx=20,
            pady=5
        )

    def select_category(self, category: str) -> None:
        """Select an accessory category."""

        self.selected_category = category

        self.selected_label.configure(
            text=f"Selected: {category}"
        )

        if self.on_accessory_selected is not None:
            self.on_accessory_selected(category)

    def _start_camera(self) -> None:
        if self.on_start_camera is not None:
            self.on_start_camera()

    def _stop_camera(self) -> None:
        if self.on_stop_camera is not None:
            self.on_stop_camera()
