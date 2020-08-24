from contracts import contract

from .generic import AttachmentField, Message, TextField


@contract
def get_dict_message(channel, source: dict, short_offset=30):
    attachment = AttachmentField()
    for title, value in source.items():
        field = TextField(value=value)
        field.set_title(title).set_short(len(str(value)) < short_offset)
        attachment.append(field)

    return Message(channel).add_attachment(attachment)
