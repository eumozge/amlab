class ColorDictFieldMixin:
    info = "#d6dbdf"
    success = "#2eb886"
    warning = "#cb4335"

    def set_color_info(self):
        return self.set_value('color', self.info)

    def set_color_success(self):
        return self.set_value('color', self.success)

    def set_color_warning(self):
        return self.set_value('color', self.warning)


class TitleDictFieldMixin:
    def set_title(self, value):
        return self.set_value('title', value)

    def set_title_link(self, value):
        return self.set_value('title_link', value)


class TextDictFieldMixin:
    def set_pretext(self, value):
        return self.set_value('pretext', value)

    def set_text(self, value):
        return self.set_value('text', value)


class AuthorDictFieldMixin:
    def set_author(self, value):
        return self.set_value('author_name', value)
