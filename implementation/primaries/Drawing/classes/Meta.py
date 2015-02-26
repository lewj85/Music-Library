try:
    from classes import BaseClass
except:
    from implementation.primaries.Drawing.classes import BaseClass

class Meta(BaseClass.Base):
    def __init__(self, **kwargs):
        BaseClass.Base.__init__(self)
        if "title" in kwargs:
            if kwargs["title"] is not None:
                self.title = kwargs["title"]
        if "composer" in kwargs:
            if kwargs["composer"] is not None:
                self.composer = kwargs["composer"]

    def EscapeQuotes(self, value):
        list_of_string = list(value)
        output = []
        for item in list_of_string:
            if item == "\"":
                output.append("\\")
            output.append(item)
        return "".join(output)

    def toLily(self):
        val = "\header {\n"
        if hasattr(self, "title") and self.title is not None:
            val += "title = \""+self.EscapeQuotes(self.title)+"\"\n"
        if hasattr(self, "composer") and self.composer is not None:
            val += "composer = \""+self.EscapeQuotes(self.composer) +"\"\n"
        if hasattr(self, "copyright"):
            val += "tagline = \""+self.EscapeQuotes(self.copyright) +"\""
        val += "\n}"
        if hasattr(self, "pageNum"):
            if self.pageNum:
                val += "\n \paper {\n print-page-number = True \n}\n\n"
        if hasattr(self, "credits"):
            val += "\\markuplist {"
            for credit in self.credits:
                val += "\n\\vspace #0.5\n"
                val += "\n"+credit.toLily()
            val += " }"

        return val

    def AddCredit(self, credit):
        if not hasattr(self, "credits"):
            self.credits = []
        self.credits.append(credit)

