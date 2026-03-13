def get_label_text(el):

    try:

        label = el.evaluate(
            """e => {
                if (e.labels && e.labels.length > 0)
                    return e.labels[0].innerText
                return null
            }"""
        )

        return label

    except:
        return None