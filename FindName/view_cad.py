# def on_file_selected(self, current, previous=None):
        # self.info.setTextInteractionFlags(self.info.textInteractionFlags() | Qt.TextSelectableByMouse)
        # fm = QFontMetrics(self.info.font())
        # """Routing: decide how to preview a selected file and whether to show media controls."""
        # try:
        #     if current is None:
        #         return
        #     file_index = self.file_list.currentRow()
        #     # get absolute path from item data if present
        #     filename = current.data(Qt.UserRole) or current.text()
        #     if not filename:
        #         filename = current.text()
        #     file_path = os.path.dirname(self.found_files[file_index]).lower()
        #     file_path = file_path.removeprefix(self.search_path).removeprefix(os.path.sep)
        #     foundFolders =[i.text().lower() for i in self.folder_list.findItems("",Qt.MatchContains)]
        #     index = list(filter(lambda i:foundFolders[i] in file_path,range(len(foundFolders))))
        #     if index:
        #         self.folder_list.setCurrentRow(index[0])
                    
            # # try to resolve relative path against search_path
            # if not os.path.isabs(filename) and getattr(self, "search_path", None):
            #     candidate = os.path.join(self.search_path, filepath)
            #     if os.path.exists(candidate):
            #         filepath = candidate

            # if not os.path.exists(filepath):
            #     self.text_view.setText("[File not found]")
            #     self.preview_top.setCurrentWidget(self.text_view)
            #     self.preview_bottom.setVisible(False)
            #     return
            #Get selected file folder path
            # file_path = file_path.removeprefix(self.search_path).removeprefix(os.path.sep)
            # foundFolders =[i.text().lower() for i in self.folder_list.findItems("",Qt.MatchContains)]
            # index = list(filter(lambda i:foundFolders[i] in file_path,range(len(foundFolders))))
            # if index:
            #     self.folder_list.setCurrentRow(index[0])
            
            # print(filepath)
            # fpath, ext = os.path.splitext(file_path)
            # ext = ext.lower()
            # print(fpath,ext)

            # Media: audio/video -> thumbnail top + enable bottom controls
        #     if ext in getattr(self, "audio_exts", set()) or ext in getattr(self, "video_exts", set()):
        #         media_view.show_media_thumbnail(self, filepath)
        #         media_view.prepare_media_player(self, filepath)
        #         # media_view.prepare_media_player will show preview_bottom
        #         return

        #     # Text/document/images handled by txt_view functions
        #     if ext in getattr(self, "readable_text_ext", set()) or ext in (".txt", ".md", ".py", ".log", ".json"):
        #         txt_view.preview_text_file(self, filepath)
        #         self.preview_bottom.setVisible(False)
        #         return

        #     # images (use QImageReader supported formats)
        #     try:
        #         from PySide6.QtGui import QImageReader
        #         supported_exts = {("." + bytes(fmt).decode()).lower() for fmt in QImageReader.supportedImageFormats()}
        #     except Exception:
        #         supported_exts = {".png", ".jpg", ".jpeg", ".bmp", ".gif"}

        #     if ext in supported_exts:
        #         txt_view.preview_image_file(self, filepath)
        #         self.preview_bottom.setVisible(False)
        #         return

        #     # docx / xlsx
        #     if ext == ".docx" or ext == ".xlsx":
        #         txt_view.preview_document_file(self, filepath)
        #         self.preview_bottom.setVisible(False)
        #         return

        #     # CAD placeholder
        #     if ext in getattr(self, "readable_cad_ext", set()):
        #         self.cad_view.setText(f"CAD preview not available for {os.path.basename(filepath)}")
        #         self.preview_top.setCurrentWidget(self.cad_view)
        #         self.preview_bottom.setVisible(False)
        #         return

        #     # fallback
        #     self.text_view.setText("[Unsupported file type]")
        #     self.preview_top.setCurrentWidget(self.text_view)
        #     self.preview_bottom.setVisible(False)

        # except Exception as e:
        #     print("Preview routing error:", e)
        #     self.text_view.setText("[Preview error]")
        #     self.preview_top.setCurrentWidget(self.text_view)
        #     self.preview_bottom.setVisible(False)

    # -- preview & search routing -----------------------
    # def _on_file_selected(self, current, previous=None):
    #     """Routing: decide how to preview a selected file and whether to show media controls."""
    #     try:
    #         if current is None:
    #             return

    
    #         # CAD placeholder
    #         if ext in getattr(self, "readable_cad_ext", set()):
    #             self.cad_view.setText(f"CAD preview not available for {os.path.basename(filepath)}")
    #             self.preview_top.setCurrentWidget(self.cad_view)
    #             self.preview_bottom.setVisible(False)
    #             return

    #         # fallback
    #         self.text_view.setText("[Unsupported file type]")
    #         self.preview_top.setCurrentWidget(self.text_view)
    #         self.preview_bottom.setVisible(False)

    #     except Exception as e:
    #         print("Preview routing error:", e)
    #         self.text_view.setText("[Preview error]")
    #         self.preview_top.setCurrentWidget(self.text_view)
    #         self.preview_bottom.setVisible(False)
